import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends, Request
from app.database.exports import SessionDep, User
from jose import jwt
from sqlalchemy import select
from app.database.exports import AsyncSession, Ruleset, User

from enum import Enum
from itertools import chain


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRES_IN_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRES_IN_MINUTES", 60)


# Exception class for handling requests with no token
class UnauthorizedError(Exception):
    pass


# Exception class when token is valid but user could not be found (empty/invalid)
class UserNotFoundError(Exception):
    pass


# Exception class when user is not allowed to perform this type of operation
class ForbiddenError(Exception):
    pass


def validate_access_token(token_str):
    return jwt.decode(token_str, JWT_SECRET_KEY, altorithms=[HASH_ALGORITHM])


async def get_user(request: Request, db: SessionDep):
    if request.url.path.startswith("/api"):
        value = request.headers.get("Authorization", "")
        scheme, _, token_str = value.partition(" ")
        if scheme.lower() != "bearer":
            raise UnauthorizedError

    else:
        token_str = request.cookies.get("access_token")

    if token_str is None:
        raise UnauthorizedError

    token = validate_access_token(token_str)

    username = token.get("sub", "")
    result_set = await db.execute(
        select(User).where((User.username == username) & (User.is_enabled.is_(True)))
    )

    user = result_set.scalars().first()

    if user is None:
        raise UserNotFoundError

    return user


UserDep = Annotated[User, Depends(get_user)]


async def get_superuser(user: UserDep):
    if not user.is_superuser:
        raise ForbiddenError

    return user


SuperuserDep = Annotated[User, Depends(get_superuser)]


async def get_edit_view_rulesets(
    user: User, db: AsyncSession
) -> tuple[list[Ruleset], list[Ruleset]]:
    rulesets = await db.execute(select(Ruleset).order_by(Ruleset.name))
    rulesets = rulesets.scalars().all()

    edit_rulesets = []
    view_rulesets = []

    for r in rulesets:
        edit_rulesets.append(r) if r.owner_id == user.id else view_rulesets.append(r)

    return edit_rulesets, view_rulesets


def enum_to_list(e: Enum):
    return [str(v) for v in e]


def enum_to_dict(e: Enum):
    return [{str(v): str(v)} for v in e]


def get_all_subclasses(cls):
    return list(
        chain.from_iterable(
            [
                list(chain.from_iterable([[x], get_all_subclasses(x)]))
                for x in cls.__subclasses__()
            ]
        )
    )
