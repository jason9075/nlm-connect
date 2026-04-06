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
        try:
            csrf_token, session_id = await fetch_tokens(cookies)
        except Exception as e:
            print("\n" + "="*60)
            print("❌ Authentication Failed!")
            print("Your COOKIE is likely expired or invalid.")
            print("\nPlease follow these steps to update it:")
            print("1. Open your browser and go to https://notebooklm.google.com/")
            print("2. Press F12 to open Developer Tools and go to the 'Network' tab.")
            print("3. Refresh the page.")
            print("4. Find a request to 'notebooklm.google.com' (the document itself).")
            print("5. Look at the 'Request Headers' and copy the entire value of 'Cookie:'.")
            print("6. Paste this new value into your .env file as COOKIE=...")
            print("="*60 + "\n")
            raise Exception("Authentication failed due to invalid COOKIE.") from e
        
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

    async def delete_source(self, source_id: str):
        """Delete a single source."""
        auth = await self._ensure_auth()
        async with NotebookLMClient(auth) as client:
            return await client.sources.delete(self.notebook_id, source_id)

