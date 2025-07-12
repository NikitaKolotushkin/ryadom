#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from datetime import datetime, timedelta
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()


class FrontEndService:
    
    def __init__(self):
        self.templates = Jinja2Templates(directory='app/templates')
        self.edge_router_service_url = os.getenv("EDGE_ROUTER_SERVICE_URL")

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

        WEEKDAY_ABBREVIATIONS = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
        DAYS_TO_DISPLAY = 21

        current_date = datetime.now().date()
        calendar_dates = []

        for day_offset in range(DAYS_TO_DISPLAY):
            target_date = current_date + timedelta(days=day_offset)

            month_day = target_date.strftime('%d').lstrip('0')
            week_day = WEEKDAY_ABBREVIATIONS[target_date.weekday()]

            calendar_dates.append([month_day, week_day])

        return self.render_template(
            request=request, 
            template_name='index.html', 
            context={'date_list': calendar_dates}
        )
    
    def get_event_page(self, request: Request, event_id: int):
        return self.render_template(
            request=request, 
            template_name='event.html', 
            context={'event_id': event_id}
        )