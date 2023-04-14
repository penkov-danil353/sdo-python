from .base import *


class CodeTest(Base):
    __tablename__ = "Test"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    functions = relationship("Function", back_populates="test")
