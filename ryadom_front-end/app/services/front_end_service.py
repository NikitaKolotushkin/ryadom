#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from datetime import datetime, timedelta
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import *

from app.utils.url import update_query_params


router = APIRouter()


class FrontEndService:
    
    def __init__(self):
        self.templates = Jinja2Templates(directory='app/templates')
        self.edge_router_service_url = os.getenv("EDGE_ROUTER_SERVICE_URL")

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
        pass

    def get_index_page(self, request: Request):
        """
        Получение главной страницы

        Args:
            request: объект запроса

        Returns:
            TemplateResponse: ответ с отрендеренным шаблоном
        """

        date_list = self._generate_date_list()

        context = {
            'date_list': date_list,
        }

        return self.render_template(
            request=request, 
            template_name='index.html', 
            context=context
        )
    
    def get_event_page(self, request: Request, event_id: int):

        context = {
            'event_id': event_id
        }

        return self.render_template(
            request=request, 
            template_name='event.html', 
            context=context
        )
    
    def get_login_page(self, request: Request):
        return self.render_template(
            request=request, 
            template_name='login.html'
        )
    
    def get_register_page(self, request: Request):
        return self.render_template(
            request=request, 
            template_name='register.html'
        )
    
    def _generate_date_list(self) -> List[dict]:
        """
        Генерирует 21 день для афиши с подсветкой активной даты и выходных.
        """
        WEEKDAY_ABBREVIATIONS = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
        DAYS_TO_DISPLAY = 21

        current_date = datetime.now().date()
        calendar_dates = []

        for day_offset in range(DAYS_TO_DISPLAY):
            target_date = current_date + timedelta(days=day_offset)

            month_day = target_date.strftime('%d').lstrip('0')
            week_day = WEEKDAY_ABBREVIATIONS[target_date.weekday()]

            calendar_dates.append([month_day, week_day])

        return calendar_dates