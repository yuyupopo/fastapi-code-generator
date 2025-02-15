# generated by fastapi-codegen:
#   filename:  custom_security.yaml
#   timestamp: 2020-06-19T00:00:00+00:00

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException, Path, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from .models import Error, Pet, PetForm

app = FastAPI()


DUMMY_CREDENTIALS = 'abcdefg'


class User(BaseModel):
    username: str
    email: str


def get_dummy_user(token: str) -> User:
    return User(username=token, email='abc@example.com')


async def valid_token(
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str:
    if auth.credentials == DUMMY_CREDENTIALS:
        return 'dummy'
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def valid_current_user(token: str = Depends(valid_token)) -> User:
    return get_dummy_user(token)


@app.get('/food/{food_id}', response_model=None, tags=['foods'])
def show_food_by_id(food_id: str, user: User = Depends(valid_current_user)) -> None:
    pass


@app.get('/pets', response_model=List[Pet], responses={'default': {'model': Error}})
def list_pets(
    limit: Optional[int] = 0,
    home_address: Optional[str] = Query('Unknown', alias='HomeAddress'),
    kind: Optional[str] = 'dog',
) -> Union[List[Pet], Error]:
    pass


@app.post(
    '/pets', response_model=None, tags=['pets'], responses={'default': {'model': Error}}
)
def post_pets(
    body: PetForm, user: User = Depends(valid_current_user)
) -> Union[None, Error]:
    pass


@app.get(
    '/pets/{pet_id}',
    response_model=Pet,
    tags=['pets'],
    responses={'default': {'model': Error}},
)
def show_pet_by_id(
    pet_id: str = Path(..., alias='petId'), user: User = Depends(valid_current_user)
) -> Union[Pet, Error]:
    pass


@app.put(
    '/pets/{pet_id}',
    response_model=None,
    tags=['pets'],
    responses={'default': {'model': Error}},
)
def put_pets_pet_id(
    pet_id: str = Path(..., alias='petId'),
    body: PetForm = None,
    user: User = Depends(valid_current_user),
) -> Union[None, Error]:
    pass
