from typing import Annotated

from fastapi import APIRouter,status, Depends, Query
from starlette.responses import Response

from app.users.dependencies import (get_current_user,
                                    get_current_admin_user,
                                    get_user_service)
from app.users.models import User
from app.users.schemas import (SUserRegister,
                               SUserAuth,
                               Role,
                               SUpdateUser,
                               UserLoginSchema,
                               SURole)
from app.users.service import UserService

router = APIRouter(prefix='/auth', tags=['Users & Auth'])
@router.get("/me/",
            status_code=status.HTTP_200_OK
)
async def get_me(
        user_data: Annotated[User, Depends(get_current_user)],
        user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_user(user_data)

@router.get(
    "/all_users/",
    status_code=status.HTTP_200_OK,
    response_model=None
)
async def get_all_users(
        user: Annotated[User, Depends(get_current_admin_user)],
        user_service: Annotated[UserService,Depends(get_user_service)]
):
    return await user_service.get_users()

@router.put("/setroles/",
            status_code=status.HTTP_202_ACCEPTED,)
async def set_role(
        user_service: Annotated[UserService,Depends(get_user_service)],
        user_data: User = Depends(get_current_admin_user),
        role: SURole = Depends()
):
    return await user_service.update_role(role)

@router.put("/update-profile/",
            status_code=status.HTTP_202_ACCEPTED,
            response_model=SUpdateUser
)
async def update_profile(
        user_service: Annotated[UserService,Depends(get_user_service)],
        user_data: SUpdateUser,
        user: Annotated[User, Depends(get_current_user)],
):
    return await user_service.update_user(body=user_data, user_id=user.id)


@router.post("/login/",
             status_code=status.HTTP_200_OK,
             response_model=UserLoginSchema
)
async def auth_user(
        user_data: SUserAuth,
        user_service: Annotated[UserService,Depends(get_user_service)],
        response: Response
):
    return await user_service.login(response=response, user_data=user_data)

@router.post("/logout/",
             status_code=status.HTTP_200_OK
)
async def logout_user(
        response: Response,
        user_service: Annotated[UserService,Depends(get_user_service)]
):
    return await user_service.logout(response=response)

@router.post("/register/",
             status_code=status.HTTP_200_OK,
             # response_model=SUserRegister
)
async def register_user(
        user_service: Annotated[UserService,Depends(get_user_service)],
        user_data: SUserRegister
):
    return await user_service.create_user(body=user_data)

@router.delete("/remove/",
               status_code=status.HTTP_200_OK
)
async def remove_user(
        user_service: Annotated[UserService,Depends(get_user_service)],
        response: Response,
        user_data: User = Depends(get_current_user)
):
    return await user_service.delete_user(user=user_data, response=response)

@router.delete("/full-remove/",
               status_code=status.HTTP_200_OK)
async def full_remove_user(
        user_service: Annotated[UserService,Depends(get_user_service)],
        user_data: Annotated[User, Depends(get_current_admin_user)],
        user_id: int
):
    return await user_service.full_delete_user(user_id=user_id)
