from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, str_uniq, int_pk


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    role_id : Mapped[int] = mapped_column(ForeignKey('roles.id'), default=1, nullable=True)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

class Roles(Base):
    __tablename__ = 'roles'
    id: Mapped[int_pk]
    roles: Mapped[str] = mapped_column(default=None, nullable=False)
    permissions: Mapped[str] = mapped_column(default=None, nullable=False)
