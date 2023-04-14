from .base import *


class FuncTest(Base):
    __tablename__ = "Function"

    id = Column(Integer, primary_key=True, index=True)
    func_name = Column(String, nullable=False)
    testid = Column(Integer, ForeignKey("Test.id"))
    test = relationship("Test", back_populates="functions")
    datas = relationship("DataTest", back_populates="function_t")
    formulas = relationship("Formula", back_populates="function_t")
