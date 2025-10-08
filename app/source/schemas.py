from pydantic import BaseModel, Field


class Brand(BaseModel):
    name: str
    country: str
    address: str

class SProduct(BaseModel):
    type: str = Field(..., description="Тип товара")
    name: str = Field(..., description="Название товара")
    description: str = Field(..., description="Описание товара")
    brand: Brand
    availability: str = Field(..., description="Наличие штук")
    price: str = Field(..., description="Цена")
    priceCurrency: str = Field(..., description="Валюта")
