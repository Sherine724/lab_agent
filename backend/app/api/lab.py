from fastapi import APIRouter,Depends
from app.models.user import User
from app.common.response import Response
from app.schemas.lab import LabCreateRequest,LabUpdateRequest
from app.dependencies.auth import get_current_admin
from app.services import lab_service
from sqlalchemy.orm import Session
from app.database import get_db

router=APIRouter(prefix="/lab",tags=["实验室管理"])

@router.get("/page")
def get_lab_page_list(
    page:int=1,
    page_size:int=10,
    keywords:str|None=None,
    current_user:User=Depends(get_current_admin),
    db:Session=Depends(get_db)):

    res=lab_service.get_lab_page_list(db,page,page_size,keywords)
    return Response.success(data=res)

@router.get("/all")
def get_all_labs(
    current_user:User=Depends(get_current_admin),
    db:Session=Depends(get_db)):
    """不分页查全部实验室，设备管理页的下拉框用"""
    res=lab_service.get_all_labs(db)
    return Response.success(data=res)

@router.post("")
def create_lab(
    data:LabCreateRequest,
    current_user:User=Depends(get_current_admin),
    db:Session=Depends(get_db)
):
    res=lab_service.create_lab(db,data)
    return Response.success(data=res)

@router.put("/{lab_id}")
def update_lab(
    lab_id:int,
    data:LabUpdateRequest,
    current_user:User=Depends(get_current_admin),
    db:Session=Depends(get_db)
):
    res=lab_service.update_lab(db,lab_id,data)
    return Response.success(data=res)

@router.delete("/{lab_id}")
def delete_lab(
    lab_id:int,
    current_user:User=Depends(get_current_admin),
    db:Session=Depends(get_db)
):
    lab_service.delete_lab(db,lab_id)
    return Response.success(message="删除实验室成功！")
