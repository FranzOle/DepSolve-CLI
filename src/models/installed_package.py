from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from src.database.connection import Base

class InstalledPackage(Base):
    __tablename__ = 'installed_packages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'), nullable=False)
    install_date = Column(DateTime(timezone=True), server_default=func.now())