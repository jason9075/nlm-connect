import os
import asyncio
from notebooklm import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens


class NLMClient:
    def __init__(self, notebook_id: str):
        self.notebook_id = notebook_id
        self.cookie_str = os.getenv("COOKIE")
        self._auth = None
        if not self.cookie_str:
            raise ValueError("COOKIE environment variable is not set")

    def _parse_cookies(self) -> dict[str, str]:
        """Parse cookie string into a dictionary."""
        cookies = {}
        for item in self.cookie_str.split(';'):
            if '=' in item:
                name, value = item.strip().split('=', 1)
                
                # Check for common copy-paste errors (ellipsis)
                if '\u2026' in value:
                    raise ValueError(f"Cookie '{name}' appears to be truncated (contains '...'). Please please copy the full cookie value from the browser.")
                
                # Ensure value is ASCII safe (httpx requirement)
                if not value.isascii():
                    print(f"Warning: Cookie '{name}' contains non-ASCII characters. Attempting to filter...")
                    value = value.encode('ascii', 'ignore').decode('ascii')
                    
                cookies[name] = value
        return cookies

    async def _ensure_auth(self):
        """Ensure we have valid auth tokens."""
        if self._auth:
            return self._auth
            
        cookies = self._parse_cookies()
        print("Fetching authentication tokens...")
        csrf_token, session_id = await fetch_tokens(cookies)
        
        self._auth = AuthTokens(
            cookies=cookies,
            csrf_token=csrf_token,
            session_id=session_id
        )
        return self._auth

    async def list_sources(self):
        """List all sources from the notebook."""
        auth = await self._ensure_auth()
        async with NotebookLMClient(auth) as client:
            print(f"Listing sources for notebook {self.notebook_id}...")
            return await client.sources.list(self.notebook_id)
            
    async def get_source_content(self, source_id: str):
        """Fetch content for a single source."""
        auth = await self._ensure_auth()
        async with NotebookLMClient(auth) as client:
            return await client.sources.get_fulltext(self.notebook_id, source_id)

