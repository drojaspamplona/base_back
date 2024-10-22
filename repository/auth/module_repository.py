from typing import List, Dict

from repository import BaseRepository


class ModuleRepository(BaseRepository):
    def __init__(self):
        super().__init__("auth", "module", "module_id")

    async def get_module_actions(self) -> List[Dict]:
        return await self.execute("select * from auth.vw_module_actions", None)
