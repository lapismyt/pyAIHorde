import msgspec
import aiohttp
from aihorde import models
from aihorde import __version__ as version
import time
import asyncio
from typing import Optional, Literal, Union


class AIHordeClient:
    def __init__(
        self,
        api_key: str = "0000000000",
        base_url: str = "https://aihorde.net/api",
        client_agent: str = "pyAIHorde:{0}:https://github.com/lapismyt/pyAIHorde".format(
            version
        ),
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.client_agent = client_agent
        self.version = version

    async def _run(
        self,
        method: str,
        path: str,
        data: Optional[Union[dict, models.AIHordeModel]] = None, # data is not AIHordeModel, but idk how i supposed to figure out 'subclass of AIHordeModel'
        additional_headers: dict = {}
    ) -> Union[list, dict]:
        if not isinstance(data, dict):
            data = data.to_dict() if data is not None else {}
        headers = {"apikey": self.api_key}
        if len(additional_headers) > 0:
            for header, value in additional_headers.items():
                headers[header] = value
        kwargs = {"json": data} if method.upper() == "POST" else {"params": data}
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, self.base_url + path, headers=headers, **kwargs
            ) as response:
                resp = await response.json()
        return resp

    async def generate_image_request(
        self,
        request: models.GenerationInputStable
    ) -> models.RequestAsync:
        return models.RequestAsync.from_dict(
            await self._run("POST", "/v2/generate/async", request)
        )

    async def image_generation_status(
        self,
        request_id: str
    ) -> models.RequestStatusStable:
        return models.RequestStatusStable.from_dict(
            await self._run("GET", f"/v2/generate/status/{request_id}")
        )

    async def generate_images(
        self,
        request: models.GenerationInputStable
    ) -> models.RequestStatusStable:
        resp: models.RequestAsync = await self.generate_image_request(request)
        request_id = resp.id
        while True:
            status = await self.image_generation_status(request_id)
            if status.done:
                return status
            else:
                await asyncio.sleep(int(status.wait_time * 0.5))
    
    async def generate_text_request(
        self,
        request: models.GenerationInputKobold
    ) -> models.RequestAsync:
        return models.RequestAsync.from_dict(
            await self._run("POST", "/v2/generate/text/async", request)
        )
    
    async def text_generation_status(
        self,
        request_id: str
    ) -> models.RequestStatusKobold:
        return models.RequestStatusKobold.from_dict(
            await self._run("GET", f"/v2/generate/text/status/{request_id}")
        )
    
    async def generate_text(
        self,
        request: models.GenerationInputKobold
    ) -> Union[models.RequestStatusKobold, models.RequestAsync]:
        resp: models.RequestAsync = await self.generate_text_request(request)
        if request.dry_run:
            return resp
        request_id = resp.id
        while True:
            status = await self.text_generation_status(request_id)
            if status.done:
                return status
            else:
                await asyncio.sleep(int(status.wait_time * 0.5))
    
    async def get_models(
            self,
            type: Optional[Literal['text', 'image']] = 'image',
            min_count: Optional[int] = None,
            max_count: Optional[int] = None,
            model_state: Optional[Literal['known', 'custom', 'all']] = 'all'
    ) -> list[models.ActiveModel]:
        data = {'type': type,
                'min_count': min_count,
                'max_count': max_count,
                'model_state': model_state}
        cleaned = {}
        for key, value in data.items():
            if not value is None:
                cleaned[key] = value
        active_models: list[dict] = await self._run('GET', '/v2/status/models', data=cleaned)
        converted = []
        for active_model in active_models:
            converted.append(models.ActiveModel.from_dict(active_model))
        return converted
    
    # NEEDS TESTING
    async def find_user(
        self,
        api_key: Optional[str] = None
    ) -> models.UserDetails:
        if api_key is None:
            api_key = self.api_key
        return models.UserDetails.from_dict(
            await self._run('GET', '/v2/find_user', additional_headers={'apikey': api_key})
        )
    
    # NEEDS TESTING
    async def interrogate_image_request(
        self,
        request: models.ModelInterrogationInputStable
    ) -> models.RequestInterrogationResponse:
        return models.RequestInterrogationResponse.from_dict(
            await self._run("POST", f"/v2/interrogate/async", request)
        )
    
    # NEEDS TESTING
    async def image_interrogation_status(
        self,
        request_id: str
    ) -> models.RequestInterrogationResponse:
        return models.RequestInterrogationResponse.from_dict(
            await self._run("GET", f"/v2/interrogate/status/{request_id}")
        )
    
    # NEEDS TESTING
    async def interrogate_image(
        self,
        request: models.ModelInterrogationInputStable
    ) -> models.RequestInterrogationResponse:
        resp: models.RequestInterrogationResponse = await self.interrogate_image_request(request)
        if request.dry_run:
            return resp
        request_id = resp.id
        while True:
            status = await self.image_interrogation_status(request_id)
            if status.done:
                return status
            else:
                await asyncio.sleep(int(status.wait_time * 0.5))
