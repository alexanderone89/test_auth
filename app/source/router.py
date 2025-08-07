from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

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
        user: Annotated[User, Depends(get_current_user)],
):
    return await product_service.get_products()

@router.put(
    "/update/",
    status_code=status.HTTP_200_OK,)
async def update_product(
        product_id:int,
        product: schemas.SProduct,
        product_service: Annotated[ProductsService, Depends(get_product_service)],
        user: Annotated[
            User,
            Depends(get_current_manager_and_admin_user)
        ],
):
    return await product_service.update_product(product_id, product)

@router.delete(
    "/delete/",
    status_code=status.HTTP_200_OK,
)
async def delete_product(
        product_id: int,
        product_service: Annotated[ProductsService, Depends(get_product_service)],
        user: Annotated[
            User,
            Depends(get_current_manager_and_admin_user),
        ],
):
    return await product_service.delete_product(product_id)
