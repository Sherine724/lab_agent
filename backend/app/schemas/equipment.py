from pydantic import BaseModel,ConfigDict
class EquipmentResponse(BaseModel):
    id:int
    name:str
    model:str|None=None
    image:str|None=None
    lab_id:int
    #来自Equipment模型上的lab_name计算属性，from_attributes会自动读取
    lab_name:str|None=None
    quantity:int|None=None
    status:int

    model_config=ConfigDict(from_attributes=True)

class EquipmentCreateRequest(BaseModel):
    name:str
    model:str|None=None
    image:str|None=None
    lab_id:int
    quantity:int|None=1
    status:int|None=1

class EquipmentUpdateRequest(BaseModel):
    name:str|None=None
    model:str|None=None
    image:str|None=None
    lab_id:int|None=None
    quantity:int|None=None
    status:int|None=None
