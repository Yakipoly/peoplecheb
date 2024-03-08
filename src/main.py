import asyncio, uvicorn, typer
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from app.exceptions import DuplicatedEntryError
from app.db.base import init_models, get_session
from app import service


app = FastAPI(
    docs_url=f"/documentation",
    root_path="/app",
    openapi_url=f"/openapi.json",
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian",
        "filter": "true",
        "tryItOutEnabled": "true",
    },
)
cli = typer.Typer()


class UserSchema(BaseModel):
    first_name: str
    last_name: str


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


@app.get("/users/", response_model=list[UserSchema])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await service.get_users(session)
    return [UserSchema(first_name=c.first_name, last_name=c.last_name) for c in users]


@app.post("/users/")
async def add_user(user: UserSchema, session: AsyncSession = Depends(get_session)):
    user = service.add_user(session, user.first_name, user.last_name)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("The user is already stored")


if __name__ == "__main__":
    # cli()
    uvicorn.run("main:app", host="localhost", port=7000)
