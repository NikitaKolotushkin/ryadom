import os
import httpx
import typing

import ryadom_schemas.events as schemas_events
import ryadom_schemas.members as schemas_members
import ryadom_schemas.users as schemas_users
from fastapi import HTTPException


class RouterService:

    def __init__(self):
        self.front_end_service_url = os.getenv("FRONT_END_SERVICE_URL")
        self.users_service_url = os.getenv("USERS_SERVICE_URL")
        self.events_service_url = os.getenv("EVENTS_SERVICE_URL")

    # USERS

    async def post_user_to_user_service(self, user_data: schemas_users.UserCreate):
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{self.users_service_url}/users/', json=user_data.model_dump())

            response.raise_for_status()

            return response.json()

    async def get_all_users_from_user_service(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.users_service_url}/users/')

            return response.json()

    async def get_user_from_user_service(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.users_service_url}/users/{user_id}')

            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="User not found")
            
            response.raise_for_status()

            return response.json()
        
    async def update_user_from_user_service(self, user_id: int, user_data: schemas_users.UserCreate):
        async with httpx.AsyncClient() as client:
            response = await client.put(f'{self.users_service_url}/users/{user_id}', json=user_data.model_dump())
            
            response.raise_for_status()
            
            return response.json()

    async def delete_user_from_user_service(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.delete(f'{self.users_service_url}/users/{user_id}')

            response.raise_for_status()

            return response.json()
        
    # EVENTS

    async def post_event_to_event_service(self, event_data: schemas_events.EventCreate):
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{self.events_service_url}/events/', json=event_data.model_dump())

            response.raise_for_status()

            return response.json()

    async def get_all_events_from_event_service(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.events_service_url}/events/')
            
            return response.json()
        
    async def get_event_from_event_service(self, event_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.events_service_url}/events/{event_id}')

            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Event not found")
            
            response.raise_for_status()

            return response.json()
        
    async def update_event_from_event_service(self, event_id: int, event_data: schemas_events.EventCreate):
        async with httpx.AsyncClient() as client:
            response = await client.put(f'{self.events_service_url}/events/{event_id}', json=event_data.model_dump())
            
            response.raise_for_status()
            
            return response.json()

    async def delete_event_from_event_service(self, event_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.delete(f'{self.events_service_url}/events/{event_id}')

            response.raise_for_status()

            return response.json()

    async def add_member_to_event(self, event_id: int, member_data: schemas_members.MemberCreate):
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{self.events_service_url}/events/{event_id}/members/', json=member_data.model_dump())

            response.raise_for_status()

            return response.json()
        
    async def get_members_by_event_id_from_event_service(self, event_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.events_service_url}/events/{event_id}/members/')

            response.raise_for_status()

            return response.json()