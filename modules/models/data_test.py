from .base import *


class DataTest(Base):
    __tablename__ = "DataTest"
    id = Column(Integer, primary_key=True, index=True)
    data_pose = Column(Integer, nullable=False)
    data = Column(String, nullable=False)
    functionid = Column(Integer, ForeignKey("Function.id"))
    function_t = relationship("Function", back_populates="datas")
