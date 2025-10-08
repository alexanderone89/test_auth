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
from app.users.dao import UsersDAO, RoleDao
from app.users.service import UserService, RoleService


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise TokenNotFoundException
    return token

class PermissionsCheck:
    def __init__(self, role: str, permissions: str)->None:
        self.role = role
        self.permissions = permissions

    async def __call__(self, token: str = Depends(get_token)):
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

        role = payload.get('role')
        if not role:
            raise PermissionErrorException

        if role not in self.role:
            raise PermissionErrorException

        permissions_to_list = payload.get('permissions').split(',')
        if not permissions_to_list:
            raise PermissionErrorException

        self_permissions_to_list = self.permissions.split(',')
        any_in = any(i in self_permissions_to_list for i in permissions_to_list)
        if not any_in:
            raise PermissionErrorException

        return user

async def get_user_service():
    return UserService(dao=UsersDAO())

async def get_roles_service():
    return RoleService(dao=RoleDao())