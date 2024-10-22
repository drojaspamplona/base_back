from typing import Dict, Optional, List

from repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("auth", "user", "user_id")

    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        return await self.get_one("select * from auth.user where email = %s", (email,))

    async def get_auth_user_by_id(self, user_id: int) -> Optional[Dict]:
        return await self.get_one("select * from auth.user where user_id = %s", (user_id,))

    async def get_user_permissions(self, user_id: int) -> List[Dict]:
        return await self.execute("select * from auth.vw_auth_user_permissions where user_id =%s", (user_id,))
