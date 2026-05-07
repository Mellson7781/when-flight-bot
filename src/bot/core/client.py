import httpx


client = httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=5.0))