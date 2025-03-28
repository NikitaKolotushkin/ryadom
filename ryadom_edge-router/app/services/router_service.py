import httpx
import typing


class RouterService:

    def __init__(self):
        self.users_service_url = 'http://127.0.0.1:8082'
        self.events_service_url = 'http://127.0.0.1:8083'

    # USERS

    async def get_all_users_from_user_service(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.users_service_url}/users/')
            return response.json()

    async def get_user_from_user_service(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.users_service_url}/users/{user_id}')
            return response.json()
        
    # EVENTS

    async def get_all_events_from_event_service(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.events_service_url}/events/')
            return response.json()
        
    async def get_event_from_event_service(self, event_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.events_service_url}/events/{event_id}')
            return response.json()

    async def post_event_to_event_service(self, event_data: typing.Dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{self.events_service_url}/events/', json=event_data)
            return response.json()

    async def delete_event_from_event_service(self, event_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.delete(f'{self.events_service_url}/events/{event_id}')
            return response
        
    async def update_event_from_event_service(self, event_id: int, event_data: typing.Dict):
        async with httpx.AsyncClient() as client:
            response = await client.put(f'{self.events_service_url}/events/{event_id}', json=event_data)
            return response