from app.database import Base
from app.models.lab import Lab
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,ForeignKey

class Equipment(Base):
    __tablename__="equipments"
    __table_args__={"comment":"实验室设备表"}
    name:Mapped[str]=mapped_column(String(50),comment="设备名称",nullable=False)
    model:Mapped[str|None]=mapped_column(String(50),comment="设备型号")
    image:Mapped[str|None]=mapped_column(String(255),comment="设备图片")
    #外键列：数据库里只存一个整数，指向labs表的id列
    #nullable=False保证每台设备必须挂在某个实验室下，数据库层面还会校验lab_id必须真实存在
    lab_id:Mapped[int]=mapped_column(ForeignKey("labs.id"),comment="所属实验室ID",nullable=False)
    quantity:Mapped[int]=mapped_column(default=1,comment="数量")
    status:Mapped[int]=mapped_column(default=1,comment="状态：0-停用，1-正常")

    #relationship不是数据库列，是SQLAlchemy提供的"对象导航"：
    #访问equipment.lab时，SQLAlchemy自动按lab_id去labs表查出对应的Lab对象（默认懒加载，用到才查）
    lab:Mapped["Lab"]=relationship()

    @property
    def lab_name(self)->str|None:
        """计算属性：给Pydantic响应模型用，让接口直接返回实验室名称，前端不用再发一次请求"""
        return self.lab.name if self.lab else None
