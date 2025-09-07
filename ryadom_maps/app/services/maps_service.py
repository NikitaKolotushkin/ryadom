#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import httpx

import ryadom_schemas.maps as schemas_maps

from cachetools import TTLCache
from fastapi import HTTPException
from typing import *


class MapsService:

    def __init__(self):
        self.edge_router_service_url = os.getenv("EDGE_ROUTER_SERVICE_URL")

        self.geocode_cache = TTLCache(maxsize=1000, ttl=86400)

        self.maps_api_key = os.getenv("MAPS_API")
        self.geocoder_api_key = os.getenv("GEOCODER_API")

    async def get_coordinates_by_address(self, address: Optional[str] = None):
        """
        Получить координаты по адресу
        
        Returns:
            GeocodeResponse: 
        """

        if not address:
            raise ValueError(f'Адрес не должен быть пустым')
        
        if address in self.geocode_cache:
            return self.geocode_cache[address]
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    'https://geocode-maps.yandex.ru/v1/',
                    params={
                        "apikey": self.geocoder_api_key,
                        "geocode": address,
                        "format": "json",
                        "results": 1
                    }
                )

                response.raise_for_status()
                data = response.json()
                
                feature_members = data["response"]["GeoObjectCollection"]["featureMember"]

                if not feature_members:
                    raise ValueError(f'Адрес {address} не найден')
                
                pos = feature_members[0]["GeoObject"]["Point"]["pos"]
                lon, lat = pos.split()

                try:
                    lat = float(lat)
                    lon = float(lon)

                except (TypeError, ValueError) as e:
                    raise ValueError('Некорректный формат координат от сервиса геокодирования')
                
                result = {
                    "lat": lat,
                    "lon": lon,
                    "address": address
                }

                self.geocode_cache[address] = result

                print(result)
                print(result)
                print(result)
                print(result)
                print(result)

                return schemas_maps.GeocodeResponse.model_validate(result, from_attributes=True)

        
        except httpx.HTTPStatusError as e:
            raise ValueError(f'{e}')
        
        except httpx.RequestError as e:
            raise ValueError(f'{e}')
        
        except Exception as e:
            raise ValueError(f'{e}')

    async def get_static_map_url_by_coordinates(
            self, 
            lat: Optional[int] = None,
            lon: Optional[int] = None,
            zoom: Optional[int] = 13,
            size: Optional[str] = '640,450'
        ):
        """
        Получить URL статической карты по координатам
        
        Args:
            lat: Широта точки
            lon: Долгота точки
            zoom: Уровень масштабирования (по умолчанию 13)
            size: Размер карты в формате "ширина,высота" (по умолчанию "650,450")
        
        Returns:
            StaticMapResponse: URL статической карты

        Raises:
            ValueError: если событие не было найдено
        """

        try:
            map_url = (
                f"https://static-maps.yandex.ru/v1?ll={lon},{lat}"
                f"&z={zoom}&size={size}"
                f"&pt={lon},{lat},pmwtm1&lang=ru_RU"
                f"&apikey={self.maps_api_key}"
            )
        
            return schemas_maps.StaticMapResponse.model_validate(map_url, from_attributes=True)
        
        except Exception as e:
            raise ValueError(f'Ошибка генерации URL карты: {str(e)}')