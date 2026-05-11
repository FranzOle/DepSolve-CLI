from sqlalchemy import Column, Integer, String, ForeignKey
from src.database.connection import Base

class Dependency(Base):
    __tablename__ = 'dependencies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'), nullable=False)
    dependency_id = Column(Integer, ForeignKey('packages.id'), nullable=False)
    min_version = Column(String(20))