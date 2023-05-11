import datetime
from typing import List, Optional
from fastapi import APIRouter
from prisma.models import User
from pydantic import BaseModel
from src.models.scalar import Gender
import json
from src.prisma import prisma
from src.utils.auth import (
    encryptPassword,
    signJWT,
    validatePassword,
)

router = APIRouter()


class SignIn(BaseModel):
    email: str
    password: str


class SignInOut(BaseModel):
    token: str
    user: User


@router.post("/auth/sign-in", tags=["auth"])
async def sign_in(signIn: SignIn):
    user = await prisma.user.find_first(
        where={
            "email": signIn.email,
        }
    )

    validated = validatePassword(signIn.password, user.password)
    del user.password

    if validated:
        token = signJWT(user.id)
        return SignInOut(token=token, user=user)

    return None


class SignUp(BaseModel):
    email: str
    password: str
    
    name: str
    firstLastName: str
    secondLastName: str
    position: str
    company: str
    street: str
    extNumber: str
    intNumber: str
    suburb: str
    city: str
    state: str
    zipCode: str
    phone: str
    birthDay: str
    age: int





@router.post("/auth/sign-up", tags=["auth"])
async def sign_up(user: SignUp):
    password = encryptPassword(user.password)
    created = await prisma.user.create(
        {
            "email": user.email,
            "password": encryptPassword(password),
            
        }
    )

    #date example 1990-01-01 
    date_object = datetime.datetime.strptime(user.birthDay,  '%Y-%m-%d').date()

    await prisma.profile.create({
        "userId": created.id,
        "name": user.name,
        "firstLastName": user.firstLastName,
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
    })

    return created


@router.get("/auth", tags=["auth"])
async def auth(active:bool = True):
    if active:
        users = await prisma.user.find_many(
            where={
                "isDeleted": False,
            },
            include={
                "profile": True,
            }
        )
    else:
        users = await prisma.user.find_many()

    for user in users:
        del user.password

    rows = []
    for user in users:
        row = {
        "id": user.id,
        "email": user.email,
        "name": user.profile.name,
        "firstLastName": user.profile.firstLastName,
        "secondLastName": user.profile.secondLastName,
        "position": user.profile.position,
        "company": user.profile.company,
        "street": user.profile.street,
        "extNumber": user.profile.extNumber,
        "intNumber": user.profile.intNumber,
        "suburb": user.profile.suburb,
        "city": user.profile.city,
        "state": user.profile.state,
        "zipCode": user.profile.zipCode,
        "phone": user.profile.phone,
        "birthDay": user.profile.birthDay,
        "age": user.profile.age,
        }
        rows.append(row)
      

    return rows
