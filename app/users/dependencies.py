from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone

from app.config import get_auth_data
from app.exceptions import (TokenNotFoundException,
                            TokenNotValidException,
                            TokenExpiredException,
                            UserNotFoundException,
                            PermissionErrorException,
                            ProfileNotActiveException)
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import Role
from app.users.service import UserService


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise TokenNotFoundException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])

    except JWTError:
        raise TokenNotValidException

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id = payload.get('sub')
    if not user_id:
        raise UserNotFoundException

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise UserNotFoundException

    if not user.is_active:
        raise ProfileNotActiveException
    return user

async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role == Role.ADMIN:
        return current_user
    raise PermissionErrorException

async def get_current_manager_user(current_user: User = Depends(get_current_user)):
    if current_user.role == Role.MANAGER:
        return current_user
    raise PermissionErrorException

async def get_current_manager_and_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role == Role.MANAGER or current_user.role == Role.ADMIN:
        return current_user
    raise PermissionErrorException

async def get_user_service():
    return UserService(dao=UsersDAO())