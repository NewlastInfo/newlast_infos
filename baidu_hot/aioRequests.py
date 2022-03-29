import aiohttp
import asyncio
import json


class AioRequests:

    @classmethod
    async def req(cls,
                  req: dict,
                  max_retry: int = 5,
                  ) -> (dict or bytes or str, str):
        retry: int = 0
        while retry < max_retry:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.request(**req) as response:
                        if response.status == 429:
                            max_retry += 1
                            continue
                        elif response.status == 200:
                            return response.text, ''
                except Exception as e:
                    err = e
                finally:
                    retry += 1
        return dict(), err
