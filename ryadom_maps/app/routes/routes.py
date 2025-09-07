#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing

import ryadom_schemas.maps as schemas_maps

from fastapi import APIRouter, Depends, HTTPException, Request, Query

from app.services.maps_service import MapsService


router = APIRouter(tags=['maps'])


async def get_maps_service():
    return MapsService()


@router.get('/geocode',
            summary='Получение координат по адресу',
            description='Преобразует текстовый адрес в географические координаты (широта и долгота)',
            response_model=schemas_maps.GeocodeResponse)
async def geocode(
    request: Request, 
    address: str | None = Query(
        None, 
        description='Адрес для преобразования в координаты',
        min_length=3
    ), 
    service: MapsService = Depends(get_maps_service)
) -> typing.Dict | None:
    try:
        return await service.get_coordinates_by_address(address)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get('/static-map',
            summary='Генерация URL статической карты',
            description='Генерирует URL для отображения статической карты с указанной меткой',
            response_model=schemas_maps.StaticMapResponse)
async def static_map(
    request: Request, 
    lat: float = Query(
        None,
        description='Широта точки',
        ge=-90,
        le=90
    ),
    lon: float = Query(
        None,
        description='Долгота точки',
        ge=-180,
        le=180
    ),
    zoom: int = Query (
        None,
        description='Уровень масштабирования карты',
    ),
    size: str = Query (
        None,
        description='Размер карты в формате \'ширина,высота\'',
        regex=r'^\d+,\d+$'
    ), 
    service: MapsService = Depends(get_maps_service)
):
    try:
        return await service.get_static_map_url_by_coordinates(lat, lon, zoom, size)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))