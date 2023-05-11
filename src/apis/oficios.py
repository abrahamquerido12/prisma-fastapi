from typing import List
from fastapi import APIRouter
from src.utils.helpers import generar_oficio, generar_oficio_pdf, generar_doc, send_mail
from src.prisma import prisma

import os



router = APIRouter()

@router.post("/oficios/{user_id}")
async def create_oficio(user_id: int):
    user = await prisma.user.find_unique(
        where={"id": user_id},
        include={"profile": True}
    )

    if not user:
        return {"error": "user not found"}

    rutaOficio = generar_oficio(user)
    fullPath = os.path.abspath(rutaOficio)

    formattedPath = fullPath.replace("\\", "/")

    return formattedPath
    

@router.get("/oficios")
async def  get_oficios(user_ids: str = ""):
    try:
        user_ids_list = [int(user_id.strip()) for user_id in user_ids.split(",") if user_id.strip()]
        
        if user_ids_list:
                users = await prisma.user.find_many(
                    where={
                        "id": {
                            "in": user_ids_list
                        }
                    },
                    include={"profile": True}
                )
        else:
                users = await prisma.user.find_many(include={"profile": True})
            
        oficios = []
        for user in users:
                rutaOficio = generar_oficio(user)
                fullPath = os.path.abspath(rutaOficio)
                formattedPath = fullPath.replace("\\", "/")
                oficios.append(formattedPath)

        return {"oficios": oficios}
    except:
        return {"error": "Error al procesar la consulta de Prisma"}


@router.get("/oficios/{user_id}/pdf")
async def generate_pdf(user_id: int):
    user = await prisma.user.find_unique(
        where={"id": user_id},
        include={"profile": True}
    )

    if not user:
        return {"error": "user not found"}

    rutaOficioPdf = generar_oficio_pdf(user)

    # check if rutaOficioPdf = {error: ....}
    if "error" in rutaOficioPdf:
        return {"error": "error generating pdf"}
    
    fullPath = os.path.abspath(rutaOficioPdf)
    formattedPath = fullPath.replace("\\", "/")


    return formattedPath

@router.get("/oficios/{user_id}/doc")
async def generate_doc(user_id: int):
    user = await prisma.user.find_unique(
        where={"id": user_id},
        include={"profile": True}
    )

    if not user:
        return {"error": "user not found"}

    rutaOficiDoc = generar_doc(user)

    # check if rutaOficioWord = {error: ....}
    if "error" in rutaOficiDoc:
        return {"error": "error generating doc"}
    
    fullPath = os.path.abspath(rutaOficiDoc)
    formattedPath = fullPath.replace("\\", "/")


    return formattedPath

#route to send to through email
@router.get("/oficios/{user_id}/email")
async def send_email(user_id: int, file_type: str = "txt"):
    user = await prisma.user.find_unique(
        where={
            "id": user_id
        },
        include={
            "profile": True
        }
    )
    
    if not user:
        return {"error": "user not found"}
      

    result = await send_mail(user, file_type)

    return result 