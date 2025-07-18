#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.services.front_end_service import FrontEndService


router = APIRouter(tags=['frontend'])


async def get_front_end_service():
    return FrontEndService()


@router.get('/', response_class=HTMLResponse)
async def root(request: Request, service: FrontEndService = Depends(get_front_end_service)):
    try:
        return service.get_index_page(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get('/event/{event_id}', response_class=HTMLResponse)
async def users(request: Request, event_id: int, service: FrontEndService = Depends(get_front_end_service)):
    try:
        return service.get_event_page(request, event_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))