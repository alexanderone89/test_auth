from dataclasses import dataclass

from starlette.responses import Response
from app.exceptions import (
    UserAlreadyExistsException,
    IncorrectEmailOrPasswordException,
    UserNotFoundException,
)
from app.users.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token
)
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import (
    SUserRegister,
    SUserAuth,
    UserLoginSchema,
    SUpdateUser,
    SURole
)


@dataclass
class UserService:
    dao: UsersDAO

    async def create_user(self, body: SUserRegister):
        user = await self.dao.find_one_or_none(filter_by={
            'email': body.email,
            'phone_number': body.phone_number,
        })
        if user:
            raise UserAlreadyExistsException

        user_dict = body.model_dump()
        user_dict['password'] = get_password_hash(body.password)

        new_user = await self.dao.add(**user_dict)
        return await self.get_user(new_user)

    async def update_user(self, body, user_id: int):
        body_dict = body.model_dump()
        check = await self.dao.update(
            filter_by={
                'id': user_id},
                **body_dict
        )
        return SUpdateUser(**body_dict)

    async def delete_user(self, user: User, response: Response):
        user = await self.dao.delete_user(user.id)
        await self.logout(response)
        return {'message': 'Пользователь успешно удален'}

    async def full_delete_user(self, user_id: int):
        check = await self.dao.full_delete(user_id)
        return {'message': 'Пользователь успешно удален'}

    async def update_role(self, role: SURole):

        check = await self.dao.update(filter_by={'id': role.id}, role=role.role)
        if check:
            return {"message": "Роль пользователя успешно обновлена!"}
        else:
            return {"message": "Ошибка при обновлении роли пользователя!"}

    async def login(self, response: Response, user_data: SUserAuth)->UserLoginSchema:
        check = await authenticate_user(email=user_data.email, password=user_data.password)
        if check is None:
            raise IncorrectEmailOrPasswordException
        access_token = create_access_token({"sub": str(check.id)})
        response.set_cookie(
            key="users_access_token",
            value=access_token,
            httponly=True
        )
        return UserLoginSchema(
            id=check.id,
            access_token=access_token)

    async def logout(self, response: Response):
        response.delete_cookie(key="users_access_token")
        return {'message': 'Пользователь успешно вышел из системы'}

    async def get_user(self, user: User):
        return await self.dao.find_one_or_none_by_id(user.id)

    async def get_users(self):
        return await self.dao.find_all()

