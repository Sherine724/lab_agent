from app.models.equipment import Equipment
from app.models.lab import Lab
from app.schemas.equipment import EquipmentResponse,EquipmentCreateRequest,EquipmentUpdateRequest
from sqlalchemy.orm import Session
from app.common.exceptions import BusinessException
from app.common.response import PageResponse

def _get_lab_or_raise(db:Session,lab_id:int)->Lab:
    """校验lab_id对应的实验室真实存在，新增和修改设备时都要过这一关"""
    lab=db.query(Lab).filter(Lab.id==lab_id).first()
    if not lab:
        raise BusinessException(message="所属实验室不存在")
    return lab

def get_equipment_page_list(
        db:Session,
        page:int,
        page_size:int,
        keywords:str|None=None,
        lab_id:int|None=None
):
    query=db.query(Equipment)
    if keywords:
        query=query.filter(Equipment.name.ilike(f"%{keywords}%"))
    #按所属实验室筛选
    if lab_id:
        query=query.filter(Equipment.lab_id==lab_id)
    total=query.count()
    items=(
        query.order_by(Equipment.id.asc())
        .offset((page-1)*page_size)
        .limit(page_size)
        .all()
        )
    return PageResponse(
        list=[EquipmentResponse.model_validate(item) for item in items],
        total=total
        )

def create_equipment(db:Session,data:EquipmentCreateRequest):
    """新增设备"""
    _get_lab_or_raise(db,data.lab_id)
    equipment=Equipment(
        name=data.name,
        model=data.model,
        image=data.image,
        lab_id=data.lab_id,
        quantity=data.quantity,
        status=data.status
    )
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return EquipmentResponse.model_validate(equipment)

def update_equipment(db:Session,equipment_id:int,data:EquipmentUpdateRequest):
    """更新设备"""
    equipment=db.query(Equipment).filter(Equipment.id==equipment_id).first()
    if not equipment:
        raise BusinessException(message="要修改的设备不存在")
    payload=data.model_dump(exclude_none=True)
    #换实验室时同样要校验新的lab_id存在
    if "lab_id" in payload:
        _get_lab_or_raise(db,payload["lab_id"])
    for field,value in payload.items():
        setattr(equipment,field,value)
    db.commit()
    db.refresh(equipment)
    return EquipmentResponse.model_validate(equipment)

def delete_equipment(db:Session,equipment_id:int):
    """删除设备"""
    equipment=db.query(Equipment).filter(Equipment.id==equipment_id).first()
    if not equipment:
        raise BusinessException(message="要删除的设备不存在")
    db.delete(equipment)
    db.commit()
