from app.models.lab import Lab
from app.models.equipment import Equipment
from app.schemas.lab import LabResponse,LabCreateRequest,LabUpdateRequest
from sqlalchemy.orm import Session
from app.common.exceptions import BusinessException
from app.common.response import PageResponse

def get_lab_page_list(
        db:Session,
        page:int,
        page_size:int,
        keywords:str|None=None
):
    query=db.query(Lab)
    if keywords:
        query=query.filter(Lab.name.ilike(f"%{keywords}%"))
    total=query.count()
    items=(
        query.order_by(Lab.id.asc())
        .offset((page-1)*page_size)
        .limit(page_size)
        .all()
        )
    return PageResponse(
        list=[LabResponse.model_validate(item) for item in items],
        total=total
        )

def get_all_labs(db:Session):
    """不分页查全部实验室，给设备管理页的下拉框用"""
    items=db.query(Lab).order_by(Lab.id.asc()).all()
    return [LabResponse.model_validate(item) for item in items]

def create_lab(db:Session,data:LabCreateRequest):
    """新增实验室"""
    exist=db.query(Lab).filter(Lab.name==data.name).first()
    if exist:
        raise BusinessException(message="实验室名称已存在")
    lab=Lab(
        name=data.name,
        location=data.location,
        image=data.image,
        capacity=data.capacity,
        status=data.status
    )
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return LabResponse.model_validate(lab)

def update_lab(db:Session,lab_id:int,data:LabUpdateRequest):
    """更新实验室"""
    lab=db.query(Lab).filter(Lab.id==lab_id).first()
    if not lab:
        raise BusinessException(message="要修改的实验室不存在")
    payload=data.model_dump(exclude_none=True)
    #改名时查重，注意不能和自己比，否则不改名也会报"已存在"
    if "name" in payload and payload["name"]!=lab.name:
        exist=db.query(Lab).filter(Lab.name==payload["name"]).first()
        if exist:
            raise BusinessException(message="实验室名称已存在")
    for field,value in payload.items():
        setattr(lab,field,value)
    db.commit()
    db.refresh(lab)
    return LabResponse.model_validate(lab)

def delete_lab(db:Session,lab_id:int):
    """删除实验室"""
    lab=db.query(Lab).filter(Lab.id==lab_id).first()
    if not lab:
        raise BusinessException(message="要删除的实验室不存在")
    #外键关联的删除保护：实验室下还挂着设备时拒绝删除，
    #否则设备的外键会指向一个不存在的lab_id，变成"孤儿数据"
    count=db.query(Equipment).filter(Equipment.lab_id==lab_id).count()
    if count>0:
        raise BusinessException(message="该实验室下还有设备，无法删除")
    db.delete(lab)
    db.commit()
