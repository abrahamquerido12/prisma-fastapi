from typing import List
from fastapi import APIRouter, Depends
from src.prisma import prisma
from src.utils.auth import JWTBearer, decodeJWT
from pydantic import BaseModel
import datetime


router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    users = await prisma.user.find_many()
    print("users", users)

    for user in users:
        del user.password

    return users


@router.get("/users/me", tags=["users"])
async def read_user_me(token=Depends(JWTBearer())):
    decoded = decodeJWT(token)

    if "userId" in decoded:
        userId = decoded["userId"]
        return await prisma.user.find_unique(where={"id": userId})
    return None


@router.get("/users/{userId}", tags=["users"])
async def read_user(userId: str):
    user = await prisma.user.find_unique(where={"id": userId})

    return user


class UpdateUser(BaseModel):
   
    email: str = None
    name: str = None
    fistLastName: str = None
    secondLastName: str = None
    position: str = None
    company: str = None
    street: str = None
    extNumber: str = None
    intNumber: str = None
    suburb: str = None
    city: str = None
    state: str = None
    zipCode: str = None
    phone: str = None
    birthDay: str = None
    age: int = None


@router.put("/users/{userId}", tags=["users"])
async def update_user(userId: str, user: UpdateUser):
    if user.email:
        await prisma.user.update(
            where={"id": int(userId)},
            data={"email": user.email}
        )

     
    profile_update_data = {
        "name": user.name,
        "firstLastName": user.fistLastName,
        "secondLastName": user.secondLastName,
        "position": user.position,
        "company": user.company,
        "street": user.street,
        "extNumber": user.extNumber,
        "intNumber": user.intNumber,
        "suburb": user.suburb,
        "city": user.city,
        "state": user.state,
        "zipCode": user.zipCode,
        "phone": user.phone,
        "birthDay": user.birthDay,
        "age": user.age,
    }

    profile_update_data = {
        k: v for k, v in profile_update_data.items() if v is not None
    }

    profile = await prisma.profile.update(
        where={"userId": int(userId)},
        data=profile_update_data
    )

    return profile         

#route to delete user by id

@router.delete("/users/{userId}", tags=["users"])
async def delete_user(userId: str):
    today = datetime.datetime.now()
    user = await prisma.user.update(
        where={"id": int(userId)},
        data={"isDeleted": True,
              "deletedAt": today
              }
    )

    return user

