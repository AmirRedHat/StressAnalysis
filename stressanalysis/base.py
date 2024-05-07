import asyncio
from enum import Enum
import inspect
from time import time
from typing import Any, Coroutine
import httpx
from httpx import Response


class StressAnalysis:
    
    class RequestMethodType(Enum):
        GET = 1
        POST = 2
    
    headers = {"connection": "close"}
    client = httpx.AsyncClient(headers=headers)
    _endpoint_info = dict()
    request_timeout = 5


    def get_endpoint_info(cls):
        return cls._endpoint_info

    async def _response_handler(
        self, 
        url: str, 
        method: str,
        response: Coroutine[Any, Any, Response],
    ):
                    
        if not response:
            return None
        
        status_code = response.status_code
        if status_code >= 500:
            self._endpoint_info[url][f"{method}_FAIL"] += 1
        elif 200 <= status_code < 400:
            self._endpoint_info[url][f"{method}_SUCCESS"] += 1
        else:
            self._endpoint_info[url][f"{method}_ERROR"] += 1
    
    async def _request(self, *, url, data: dict, method: RequestMethodType):
        
        response = None
        start_time = time()
        try:
            match method:
                case self.RequestMethodType.GET:
                    method = "GET"
                    response = await self.client.get(url, params=data, timeout=self.request_timeout)
                case self.RequestMethodType.POST:
                    method = "POST"
                    response = await self.client.post(url, json=data, timeout=self.request_timeout)
                case _:
                    raise ValueError(f"{method} is invalid method")
            
            # check existence of url in _endpoint_info variable
            if url not in self._endpoint_info.keys():
                self._endpoint_info[url] = {
                    f"{method}_ERROR": 0,
                    f"{method}_SUCCESS": 0,
                    f"{method}_FAIL": 0,
                    "REQUEST_DURATION": 0
                }
                
        except httpx.ConnectTimeout:
            self._endpoint_info[url][f"{method}_ERROR"] += 1
            
        self._endpoint_info[url]["REQUEST_DURATION"] += round(float(time() - start_time), 2)
        await self._response_handler(
            url=url,
            method=method,
            response=response
        )
    
    def get(self, url: str, params: dict = {}):
        return asyncio.run(
            self._request(
                url=url,
                data=params,
                method=self.RequestMethodType.GET
            )
        )
    
    def post(self, url: str, payload: dict = {}):
        return asyncio.run(
            self._request(
                url=url,
                data=payload,
                method=self.RequestMethodType.GET
            )
        ) 
    
    def get_send_methods(self):
        send_decorator_methods = inspect.getsourcelines(self.__class__)[0]
        for i,line in enumerate(send_decorator_methods):
            line = line.strip()
            if line.split('(')[0].strip() == '@send':
                yield send_decorator_methods[i+1].split('def')[1].split('(')[0].strip()
                
    def analysis(self):
        method_names = list(self.get_send_methods())
        methods = inspect.getmembers(self)
        for name, method in methods:
            if name in method_names:
                method()
