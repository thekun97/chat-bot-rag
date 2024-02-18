from db.database import Database


class Repository:
    def __init__(self) -> None:
        self.db = Database()

    async def save(self, data, collection_name):
        return await self.db._insert(data, collection_name)

    async def find(self, criteria, collection_name, projection=None, limit=0, sort=None, cursor=False):
        print("DBBB", self.db.__dict__)
        return await self.db._find(criteria, collection_name, projection=None, limit=0, sort=None, cursor=False)

    async def find_by_id(self, id, collection_name):
        return await self.db._find_by_id(id, collection_name)

    async def update(self, id, data, collection_name):
        return await self.db._update(id, data, collection_name)
