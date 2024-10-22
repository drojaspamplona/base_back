from typing import List, Dict, NoReturn

from repository import BaseRepository


class UserPermissionsRepository(BaseRepository):
    def __init__(self):
        super().__init__("auth", "user_permissions", "user_permissions_id")

    async def get_user_permissions(self, user_id: int) -> List[Dict]:
        return await self.execute("select * from auth.vw_user_permissions where user_id = %s", (user_id,))

    async def delete_all_user_permissions(self, user_id: int) -> NoReturn:
        await self.execute_non_query("delete from auth.user_permissions where user_id = %s", (user_id,))
