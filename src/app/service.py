from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import *


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(
        select(User).order_by(User.last_name.desc()).limit(20)
    )
    return result.scalars().all()


def add_user(session: AsyncSession, first_name: str, last_name: int):
    new_user = User(first_name=first_name, last_name=last_name)
    session.add(new_user)
    return new_user
