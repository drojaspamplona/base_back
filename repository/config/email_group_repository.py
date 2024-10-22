from repository import BaseRepository


class EmailGroupRepository(BaseRepository):
    def __init__(self):
        super().__init__("config", "email_group", "email_group_id")

    async def get_emails_by_type_and_business(self, email_group_type: int, business: int):
        return await self.execute("""select email from config.email_group_detail as egd
                                    join auth."user" u on u.user_id = egd.user_id
                                    join config.email_group eg on eg.email_group_id = egd.email_group_id
                                    where eg.email_group_type_id = %s and eg.business_id = %s
                                    union
                                    select email from config.email_group_emails ege
                                    join config.email_group as eg on eg.email_group_id = ege.email_group_id
                                    where eg.email_group_type_id  = %s and eg.business_id = %s""",
                                  (email_group_type, business, email_group_type, business))
