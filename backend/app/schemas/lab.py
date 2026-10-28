from pydantic import BaseModel,ConfigDict
class LabResponse(BaseModel):
    id:int
    name:str
    location:str|None=None
    image:str|None=None
    capacity:int|None=None
    status:int

    model_config=ConfigDict(from_attributes=True)

class LabCreateRequest(BaseModel):
    name:str
    location:str|None=None
    image:str|None=None
    capacity:int|None=None
    status:int|None=1

class LabUpdateRequest(BaseModel):
    name:str|None=None
    location:str|None=None
    image:str|None=None
    capacity:int|None=None
    status:int|None=None
