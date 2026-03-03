from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from config.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    OPERATOR = "operator"
    QUALITY = "quality"
    LOGISTICS = "logistics"

class MaterialStatus(str, enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    USED = "used"
    EXPIRED = "expired"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class QualityStatus(str, enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    REWORK = "rework"

class ShipmentStatus(str, enum.Enum):
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.OPERATOR, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User {self.username}>"

class RawMaterial(Base):
    __tablename__ = "raw_materials"
    
    material_id = Column(Integer, primary_key=True)
    material_name = Column(String(100), nullable=False, index=True)
    material_type = Column(String(50), nullable=False)
    supplier = Column(String(100), nullable=False)
    quantity_available = Column(Float, nullable=False, default=0)
    unit = Column(String(20), nullable=False)
    cost_per_unit = Column(Float, nullable=False)
    status = Column(Enum(MaterialStatus), default=MaterialStatus.AVAILABLE)
    expiry_date = Column(DateTime, nullable=True)
    batch_number = Column(String(50), nullable=False, index=True)
    quality_grade = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    
    def __repr__(self):
        return f"<RawMaterial {self.material_name}>"

class ProductionOrder(Base):
    __tablename__ = "production_orders"
    
    order_id = Column(Integer, primary_key=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    product_name = Column(String(100), nullable=False)
    quantity_ordered = Column(Float, nullable=False)
    quantity_produced = Column(Float, default=0)
    unit = Column(String(20), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    start_date = Column(DateTime, nullable=True)
    expected_completion = Column(DateTime, nullable=False)
    actual_completion = Column(DateTime, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.user_id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProductionOrder {self.order_number}>"

class InventoryLog(Base):
    __tablename__ = "inventory_logs"
    
    log_id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey("raw_materials.material_id"), nullable=False, index=True)
    transaction_type = Column(String(20), nullable=False)  # IN, OUT, ADJUST
    quantity_change = Column(Float, nullable=False)
    quantity_before = Column(Float, nullable=False)
    quantity_after = Column(Float, nullable=False)
    reference_id = Column(String(50))
    notes = Column(Text)
    recorded_by = Column(Integer, ForeignKey("users.user_id"))
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<InventoryLog {self.material_id}>"

class QualityInspection(Base):
    __tablename__ = "quality_inspections"
    
    inspection_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("production_orders.order_id"), nullable=False, index=True)
    inspection_date = Column(DateTime, default=datetime.utcnow)
    tested_by = Column(Integer, ForeignKey("users.user_id"))
    status = Column(Enum(QualityStatus), nullable=False)
    tensile_strength = Column(Float, nullable=True)
    hardness = Column(Float, nullable=True)
    ductility = Column(Float, nullable=True)
    surface_quality = Column(String(50))
    defects_found = Column(Text)
    rework_required = Column(Boolean, default=False)
    passed_date = Column(DateTime, nullable=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<QualityInspection {self.inspection_id}>"

class Shipment(Base):
    __tablename__ = "shipments"
    
    shipment_id = Column(Integer, primary_key=True)
    shipment_number = Column(String(50), unique=True, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("production_orders.order_id"), nullable=False)
    destination = Column(String(200), nullable=False)
    quantity_shipped = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    status = Column(Enum(ShipmentStatus), default=ShipmentStatus.PENDING)
    scheduled_date = Column(DateTime, nullable=False)
    actual_ship_date = Column(DateTime, nullable=True)
    expected_delivery = Column(DateTime, nullable=False)
    actual_delivery = Column(DateTime, nullable=True)
    carrier = Column(String(100))
    tracking_number = Column(String(100))
    logistics_handler = Column(Integer, ForeignKey("users.user_id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Shipment {self.shipment_number}>"
