from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from fastapi import Depends

from app.database.base import Base

User: DeclarativeMeta = Base.classes.user_
Ruleset: DeclarativeMeta = Base.classes.ruleset
Sentence: DeclarativeMeta = Base.classes.sentence


async def async_session():
    async with AsyncSessionmaker.begin() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(async_session)]
