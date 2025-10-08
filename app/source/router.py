from typing import Annotated

from fastapi import APIRouter

from app.source import schemas
from app.source.service import ProductsService, get_product_service
from app.users.dependencies import *
from app.users.models import User

router = APIRouter(prefix='/products', tags=['Products'])


@router.get(
    "/",
    response_model=list[schemas.SProduct],)
async def get_all_products(
        product_service: Annotated[ProductsService, Depends(get_product_service)],
        user: Annotated[User, Depends(PermissionsCheck("admin,manager,user", "admin:read,manager:read,user:read"))]
):
    return await product_service.get_products()

@router.put(
    "/update/",
    status_code=status.HTTP_200_OK,)
async def update_product(
        product_id:int,
        product: schemas.SProduct,
        product_service: Annotated[ProductsService, Depends(get_product_service)],
        user: Annotated[User, Depends(PermissionsCheck("admin,manager", "admin:write,manager:write"))]
):
    return await product_service.update_product(product_id, product)

@router.delete(
    "/delete/",
    status_code=status.HTTP_200_OK,
)
async def delete_product(
        product_id: int,
        product_service: Annotated[ProductsService, Depends(get_product_service)],
        user: Annotated[User, Depends(PermissionsCheck("admin,manager", "manager:delete,admin:full-delete"))]
):
    return await product_service.delete_product(product_id)
