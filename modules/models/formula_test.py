from .base import *


class FormulaTest(Base):
    __tablename__ = "Formula"
    id = Column(Integer, primary_key=True, index=True)
    num = Column(Integer, primary_key=True, index=True)
    formula = Column(String, nullable=False)
    functionid = Column(Integer, ForeignKey("Function.id"))
    function_t = relationship("Function", back_populates="datas")
