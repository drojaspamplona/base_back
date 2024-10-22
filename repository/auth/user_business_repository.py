from typing import Dict, List

from repository import BaseRepository


class UserBusinessRepository(BaseRepository):
    def __init__(self):
        super().__init__("auth", "user_business", "user_business_id")

    async def get_by_user_id(self, user_id: int) -> List[Dict]:
        return await self.execute(f"{self.build_select()} where user_id = %s", (user_id,))
