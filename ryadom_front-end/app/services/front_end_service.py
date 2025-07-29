#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import httpx

from datetime import datetime, timedelta
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
    
    async def get_event_data(self, event_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.edge_router_service_url}/api/events/{event_id}')
            
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Event not found")
            response.raise_for_status()
            
            return response.json() 

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

        active_category = category if category in self._get_allowed_categories() else None

        context = {
            'title': 'Ryadom | Главная',
            'date_list': date_list,
            'events': events,
            'active_category': active_category,
            'allowed_categories': self._get_allowed_categories(),
        }

        return self.render_template(
            request=request, 
            template_name='index.html', 
            context=context
        )
    
    def get_event_page(self, request: Request, event_id: int):

        event_data = {
            'id': event_id,
            'name': 'Мероприятие',
        }

        context = {
            'title': f'Ryadom | {event_data['name']}',
            'event_data': event_data
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

        one_event = await self.get_event_data(1)

        all_events = [
            one_event
        ]

        filtered_events = all_events

        # if category and category in [category_['id'] for category_ in self._get_allowed_categories()]:
        #     filtered_events = [event for event in filtered_events if event['category'] == category]
        
        # if date:
        #     filtered_events = [event for event in filtered_events if event['date'] == date]
        
        return filtered_events
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime.date]:
        """
        Парсит строку даты в объект date
        """
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
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
                'iso_date': target_date.strftime('%Y-%m-%d'),
                'month_day': month_day,
                'week_day': week_day,
                'is_weekend': week_day in ['сб', 'вс']
            })

        return date_list