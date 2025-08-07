from dataclasses import dataclass

from app.source.dao import ProductsDao
from app.source.schemas import SProduct


@dataclass
class ProductsService:
    dao: ProductsDao

    async def get_products(self):
        return await self.dao.find_all()

    async def update_product(self, product_id: int, product: SProduct):
        check = await self.dao.update(product_id, product)
        if check is None:
            return {'message': 'Товар не найден'}
        return {'message': 'Товар успешно обновлен'}

    async def delete_product(self, product_id: int):
        check = await self.dao.delete(product_id)
        if check is None:
            return {'message': 'Товар не найден'}
        return {'message': 'Товар успешно удален'}

async def get_product_service():
    return ProductsService(dao=ProductsDao())