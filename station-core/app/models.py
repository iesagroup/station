from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func
from app.database import Base



class StationTask(Base):
    __tablename__ = "station_tasks"

    id = Column(Integer, primary_key=True, index=True)
    server_task_id = Column(Integer, nullable=False)

    product_name = Column(String(255), nullable=False)
    gtin = Column(String(14), nullable=False)

    quantity_in_box = Column(Integer, nullable=False)
    quantity_in_pallet = Column(Integer, nullable=False)

    planned_quantity = Column(Integer, nullable=False)
    production_date = Column(Date, nullable=True)
    shelf_life_days = Column(Integer, nullable=True)

    scenario_code = Column(Integer, nullable=True)
    scenario_name = Column(String(255), nullable=True)

    status = Column(String(50), nullable=False, default="queued")

    created_at = Column(DateTime(timezone=True), server_default=func.now())