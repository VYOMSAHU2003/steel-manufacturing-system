from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from config.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STORE_MANAGER = "store_manager"
    PRODUCTION_MANAGER = "production_manager"
    QUALITY_MANAGER = "quality_manager"
    DISPATCH_MANAGER = "dispatch_manager"
    OPERATOR = "operator"
    VIEWER = "viewer"

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

class ProductStatus(str, enum.Enum):
    PRODUCED = "produced"
    QUALITY_CHECK = "quality_check"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISPATCHED = "dispatched"

class DefectType(str, enum.Enum):
    SURFACE_DEFECT = "surface_defect"
    DIMENSIONAL = "dimensional"
    CHEMICAL_COMPOSITION = "chemical_composition"
    STRUCTURAL = "structural"
    CONTAMINATION = "contamination"

class TransportType(str, enum.Enum):
    RAIL = "rail"
    TRUCK = "truck"
    SHIP = "ship"
    PIPELINE = "pipeline"

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

class FinishedProduct(Base):
    """Finished Steel Products Inventory - Railway Rails, Steel Plates, etc."""
    __tablename__ = "finished_products"
    
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(100), nullable=False, index=True)  # Railway Rails, Steel Plates, etc.
    product_type = Column(String(50), nullable=False)  # Structural, Sheets, Rails, etc.
    production_batch = Column(String(50), nullable=False, index=True)
    quality_grade = Column(String(20), nullable=False)  # Grade A, Grade B, etc.
    production_quantity = Column(Float, nullable=False)
    available_stock = Column(Float, nullable=False, default=0)
    unit = Column(String(20), nullable=False)  # tons, kg, pieces
    warehouse_location = Column(String(100), nullable=False)
    cost_per_unit = Column(Float, nullable=False)
    status = Column(Enum(ProductStatus), default=ProductStatus.PRODUCED)
    production_order_id = Column(Integer, ForeignKey("production_orders.order_id"))
    specifications = Column(Text)  # Technical specifications
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    
    def __repr__(self):
        return f"<FinishedProduct {self.product_name}>"

class DefectTracking(Base):
    """Track defective products and scrap generated during production"""
    __tablename__ = "defect_tracking"
    
    defect_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("finished_products.product_id"), nullable=True)
    product_name = Column(String(100), nullable=False)
    production_batch = Column(String(50), nullable=False, index=True)
    defective_quantity = Column(Float, nullable=False)
    scrap_quantity = Column(Float, nullable=False, default=0)
    unit = Column(String(20), nullable=False)
    defect_type = Column(Enum(DefectType), nullable=False)
    reason_for_defect = Column(Text, nullable=False)
    inspection_date = Column(DateTime, default=datetime.utcnow)
    inspected_by = Column(Integer, ForeignKey("users.user_id"))
    estimated_loss = Column(Float, nullable=True)  # Financial loss
    corrective_action = Column(Text)
    prevention_measure = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<DefectTracking {self.product_name}>"

class CustomerOrder(Base):
    """Customer orders for finished products"""
    __tablename__ = "customer_orders"
    
    customer_order_id = Column(Integer, primary_key=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_name = Column(String(200), nullable=False, index=True)
    customer_contact = Column(String(100))
    customer_address = Column(Text)
    product_name = Column(String(100), nullable=False)
    quantity_ordered = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    unit_price = Column(Float, nullable=False)
    total_value = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    required_delivery_date = Column(DateTime, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    special_requirements = Column(Text)
    sales_representative = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<CustomerOrder {self.order_number}>"

class DispatchRecord(Base):
    """Track finished goods leaving the plant"""
    __tablename__ = "dispatch_records"
    
    dispatch_id = Column(Integer, primary_key=True)
    dispatch_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_order_id = Column(Integer, ForeignKey("customer_orders.customer_order_id"))
    product_id = Column(Integer, ForeignKey("finished_products.product_id"))
    product_name = Column(String(100), nullable=False)
    dispatch_quantity = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    customer_name = Column(String(200), nullable=False)
    destination = Column(String(200), nullable=False)
    transport_type = Column(Enum(TransportType), nullable=False)
    vehicle_number = Column(String(50))
    driver_details = Column(String(200))
    dispatch_date = Column(DateTime, default=datetime.utcnow)
    expected_delivery_date = Column(DateTime, nullable=False)
    actual_delivery_date = Column(DateTime, nullable=True)
    dispatch_status = Column(Enum(ShipmentStatus), default=ShipmentStatus.PENDING)
    dispatch_manager = Column(Integer, ForeignKey("users.user_id"))
    gate_pass_number = Column(String(50))
    vehicle_weight_empty = Column(Float)
    vehicle_weight_loaded = Column(Float)
    transport_cost = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DispatchRecord {self.dispatch_number}>"

class ProductionPrediction(Base):
    """Store prediction data for raw material requirements"""
    __tablename__ = "production_predictions"
    
    prediction_id = Column(Integer, primary_key=True)
    product_name = Column(String(100), nullable=False)
    historical_production = Column(Float, nullable=False)
    raw_material_used = Column(Float, nullable=False)
    conversion_ratio = Column(Float, nullable=False)  # Product/Raw Material ratio
    target_production = Column(Float, nullable=False)
    predicted_raw_material = Column(Float, nullable=False)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    prediction_for_date = Column(DateTime, nullable=False)
    accuracy_score = Column(Float, nullable=True)  # For tracking prediction accuracy
    created_by = Column(Integer, ForeignKey("users.user_id"))
    notes = Column(Text)
    
    def __repr__(self):
        return f"<ProductionPrediction {self.product_name}>"

class MaterialConsumption(Base):
    """Track automatic material consumption for production"""
    __tablename__ = "material_consumption"
    
    consumption_id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey("raw_materials.material_id"), nullable=False)
    production_order_id = Column(Integer, ForeignKey("production_orders.order_id"))
    consumed_quantity = Column(Float, nullable=False)
    consumption_type = Column(String(50), nullable=False)  # production, testing, maintenance
    consumption_date = Column(DateTime, default=datetime.utcnow)
    consumed_by = Column(Integer, ForeignKey("users.user_id"))
    notes = Column(Text)
    old_stock = Column(Float, nullable=False)  # Stock before consumption
    new_stock = Column(Float, nullable=False)  # Stock after consumption
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<MaterialConsumption {self.consumption_id}>"

class LowStockAlert(Base):
    """System alerts for low stock materials"""
    __tablename__ = "low_stock_alerts"
    
    alert_id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey("raw_materials.material_id"), nullable=False)
    alert_type = Column(String(20), nullable=False)  # warning, critical, urgent
    current_stock = Column(Float, nullable=False)
    minimum_threshold = Column(Float, nullable=False)
    alert_message = Column(Text, nullable=False)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(Integer, ForeignKey("users.user_id"))
    acknowledged_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<LowStockAlert {self.alert_id}>"

class MaterialReorderSuggestion(Base):
    """Automatic reorder suggestions based on consumption patterns"""
    __tablename__ = "reorder_suggestions"
    
    suggestion_id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey("raw_materials.material_id"), nullable=False)
    current_stock = Column(Float, nullable=False)
    average_daily_consumption = Column(Float, nullable=False)
    days_until_stockout = Column(Integer, nullable=False)
    suggested_order_quantity = Column(Float, nullable=False)
    suggested_order_date = Column(DateTime, nullable=False)
    urgency_level = Column(String(20), nullable=False)  # low, medium, high, urgent
    is_processed = Column(Boolean, default=False)
    processed_by = Column(Integer, ForeignKey("users.user_id"))
    processed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<MaterialReorderSuggestion {self.suggestion_id}>"
