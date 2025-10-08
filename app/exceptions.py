from fastapi import HTTPException, status


IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль",
)

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",
)

TokenNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен не найден',
)

TokenNotValidException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен не валидный!'
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен истек'
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Пользователь не найден',
)

PermissionErrorException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Недостаточно прав',
)

ProfileNotActiveException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Профиль пользователя не активен",
)

PasswordsDoNotMatchException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Пароли не совпадают",
)
