from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String

class Lab(Base):
    __tablename__="labs"
    __table_args__={"comment":"实验室信息表"}
    name:Mapped[str]=mapped_column(String(50),comment="实验室名称",nullable=False,unique=True)
    location:Mapped[str|None]=mapped_column(String(100),comment="位置")
    image:Mapped[str|None]=mapped_column(String(255),comment="实验室图片")
    capacity:Mapped[int|None]=mapped_column(comment="学生容量")
    status:Mapped[int]=mapped_column(default=1,comment="状态：0-禁用，1-正常")
