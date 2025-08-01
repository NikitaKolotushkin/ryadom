#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import httpx

from datetime import date, datetime, timedelta
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import *

from app.utils.url import update_query_params


router = APIRouter()


class FrontEndService:
    
    def __init__(self):
        self.edge_router_service_url = os.getenv("EDGE_ROUTER_SERVICE_URL")
        
        self.templates = Jinja2Templates(directory='app/templates')
        self.templates.env.globals["request_context"] = self.request_context

    def request_context(self, request: Request):
        return {
            "update_query_params": lambda **kwargs: update_query_params(
                str(request.url), 
                **kwargs
            )
        }

    def render_template(self, request: Request, template_name: str, context: dict = None):
        """
        Рендер шаблона с контекстом

        Args:
            template_name: имя шаблона
            context: данные для шаблона

        Returns:
            TemplateResponse: ответ с отрендеренным шаблоном
        """

        if context is None:
            context = {}

        context.setdefault('request', request)

        return self.templates.TemplateResponse(
            name=template_name, 
            context=context
        )
    
    async def get_event_data(self, event_id: int) -> dict:
        
        """
        Получить данные события по id
        
        Args:
            event_id: id события
        
        Returns:
            dict: данные события
        
        Raises:
            HTTPException: 404 - Event not found
            HTTPException: 504 - Service unavailable, request timed out
            HTTPException: 503 - Service unavailable, request error
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f'{self.edge_router_service_url}/api/events/{event_id}')
                
                if response.status_code == 404:
                    raise HTTPException(status_code=404, detail="Event not found")
                
                response.raise_for_status()
                
                return response.json()

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504, 
                detail="Service unavailable, request timed out"
            )

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, 
                detail="Service unavailable, request error"
            )

    async def get_all_events(self) -> List[dict]:
        """
        Получение списка всех событий

        Returns:
            List[dict]: список событий

        Raises:
            HTTPException: 404 - Events not found
            HTTPException: 500 - Internal server error
            HTTPException: 503 - Service unavailable, request error
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f'{self.edge_router_service_url}/api/events/')
                
                if response.status_code == 404:
                    return []

                response.raise_for_status()

                data = response.json()

                if 'events' not in data:
                    raise HTTPException(
                        status_code=500, detail="Invalid response format from events service"
                    )

                return data['events']

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, 
                detail=str(e)
            )

        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail='Internal server error'
            )

    async def get_index_page(self, request: Request, category: Optional[str] = None, date: Optional[str] = None):
        """
        Получение главной страницы с поддержкой фильтрации

        Args:
            request: объект запроса
            category: категория для фильтрации
            date: дата для фильтрации (YYYY-MM-DD)

        Returns:
            TemplateResponse: ответ с отрендеренным шаблоном
        """

        selected_date = self._parse_date(date)

        date_list = self._generate_date_list(selected_date)

        events = await self._get_filtered_events(category, selected_date)

        for event in events:
            event['human_date'] = ' '.join(self._get_human_date(event['date']).split()[:2])

        active_category = category if category in [el.get('id') for el in self._get_allowed_categories()] else None

        events = self._sort_events(events)

        context = {
            'title': 'Ryadom | Главная',
            'date_list': date_list,
            'events': events,
            'active_category': active_category,
            'allowed_categories': self._get_allowed_categories(),
            'slides': events.get('upcoming')[:3]
        }

        return self.render_template(
            request=request, 
            template_name='index.html', 
            context=context
        )
    
    async def get_event_page(self, request: Request, event_id: int):

        event_data = await self.get_event_data(event_id)
        category = self._get_allowed_categories()

        is_past = date.fromisoformat(event_data['date']) < date.today()

        context = {
            'title': f'Ryadom | {event_data['name']}',
            'event_data': event_data,
            'category': self._get_russian_category_name(event_data['category']),
            'human_date': self._get_human_date(event_data['date']),
            'is_past': is_past
        }

        return self.render_template(
            request=request, 
            template_name='event.html', 
            context=context
        )
    
    def get_login_page(self, request: Request):
        
        context = {
            'title': 'Ryadom | Вход'
        }

        return self.render_template(
            request=request, 
            template_name='login.html',
            context=context
        )
    
    def get_register_page(self, request: Request):
        
        context = {
            'title': 'Ryadom | Регистрация'
        }
        
        return self.render_template(
            request=request, 
            template_name='register.html',
            context=context
        )
    
    def _get_allowed_categories(self) -> List[Dict]:
        
        """
        Получение доступных категорий мероприятий.

        Returns:
            List[Dict]: Список категорий с полями 'id' и 'name'.
        """
        return [
            {"id": "science", "name": "Наука"},
            {"id": "education", "name": "Образование"},
            {"id": "volunteering", "name": "Волонтерство"},
            {"id": "business", "name": "Бизнес"},
            {"id": "career", "name": "Карьера"},
            {"id": "culture", "name": "Культура"},
            {"id": "sport", "name": "Спорт"}
        ]

    def _get_russian_category_name(self, en_id: str):
        category_map = {category["id"]: category["name"] for category in self._get_allowed_categories()}
        
        return category_map.get(en_id, None)

    async def _get_filtered_events(
            self, 
            category: Optional[str], 
            date: Optional[datetime.date]
    ) -> List[dict]:

        """
        Возвращает список событий, отфильтрованных по категории и дате
        
        Args:
            category: категория для фильтрации
            date: дата для фильтрации
        
        Returns:
            List[dict]: список событий
        """

        all_events = await self.get_all_events()

        filtered_events = all_events

        if category and category in [category_['id'] for category_ in self._get_allowed_categories()]:
            filtered_events = [event for event in filtered_events if event['category'] == category]
        
        if date:
            filtered_events = [event for event in filtered_events if str(event['date']) == str(date)]
        
        return filtered_events
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime.date]:
        """
        Парсит строку даты в объект date
        """
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%d-%m-%Y").date()
        except (TypeError, ValueError):
            return None
    
    def _generate_date_list(self, active_date: Optional[datetime.date]) -> List[dict]:
        """
        Генерирует 21 день для афиши с подсветкой активной даты и выходных.
        """
        WEEKDAY_ABBREVIATIONS = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
        DAYS_TO_DISPLAY = 21

        today = datetime.now().date()
        active_date = active_date or today

        date_list = []

        for day_offset in range(DAYS_TO_DISPLAY):
            target_date = today + timedelta(days=day_offset)

            month_day = target_date.strftime('%d').lstrip('0')
            week_day = WEEKDAY_ABBREVIATIONS[target_date.weekday()]

            date_list.append({
                'iso_date': target_date.strftime('%d-%m-%Y'),
                'month_day': month_day,
                'week_day': week_day,
                'is_weekend': week_day in ['сб', 'вс']
            })

        return date_list

    def _get_human_date(self, date_str: str):
        dt = datetime.strptime(date_str, "%Y-%m-%d")

        MONTHS_RU = {
            1: "января",
            2: "февраля",
            3: "марта",
            4: "апреля",
            5: "мая",
            6: "июня",
            7: "июля",
            8: "августа",
            9: "сентября",
            10: "октября",
            11: "ноября",
            12: "декабря"
        }

        return f"{dt.day} {MONTHS_RU[dt.month]} {dt.year}"

    def _sort_events(self, events):
        today = date.today()
    
        upcoming = []
        past = []
        
        for event in events:
            event_date = date.fromisoformat(event['date'])
            
            if event_date >= today:
                upcoming.append(event)
            else:
                past.append(event)
        
        return {
            'upcoming': upcoming,
            'past': past
        }