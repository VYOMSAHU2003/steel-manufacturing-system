# Oracle Database Setup Guide

This guide provides instructions for setting up the Oracle database for the Steel Manufacturing System.

## Prerequisites

- Oracle Database 11g or higher
- SQLPlus or Oracle SQL Developer
- Database user with CREATE TABLE, CREATE SEQUENCE, and CREATE INDEX privileges

## Connection Setup

### 1. Create Oracle Database User

Connect to Oracle as SYSDBA and run:

```sql
-- Create tablespace (optional but recommended)
CREATE TABLESPACE steel_mfg
  DATAFILE 'steel_mfg.dbf' SIZE 500M
  AUTOEXTEND ON NEXT 50M;

-- Create user
CREATE USER steel_admin IDENTIFIED BY "StrongPassword123"
  DEFAULT TABLESPACE steel_mfg
  QUOTA UNLIMITED ON steel_mfg;

-- Grant privileges
GRANT CREATE SESSION TO steel_admin;
GRANT CREATE TABLE TO steel_admin;
GRANT CREATE SEQUENCE TO steel_admin;
GRANT CREATE INDEX TO steel_admin;
GRANT ALTER SESSION TO steel_admin;
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
ORACLE_HOST=your_oracle_host
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=ORCL
ORACLE_USER=steel_admin
ORACLE_PASSWORD=StrongPassword123
```

### 3. Test Connection

From project root, test the connection:

```python
python -c "
from config.database import engine
with engine.connect() as conn:
    result = conn.execute('SELECT 1 FROM dual')
    print('✓ Oracle connection successful')
"
```

## Schema Creation

### Option 1: Automatic (Recommended)

The application will automatically create tables on first run:

```bash
python scripts/init_db.py
```

This script will:
1. Create all required tables
2. Create indexes for foreign keys
3. Seed default users
4. Set up audit triggers (optional)

### Option 2: Manual Schema Creation

If you prefer to create the schema manually, use the SQL below:

```sql
-- Users Table
CREATE TABLE users (
    user_id         NUMBER PRIMARY KEY,
    username        VARCHAR2(50) NOT NULL UNIQUE,
    email           VARCHAR2(100) NOT NULL UNIQUE,
    password_hash   VARCHAR2(255) NOT NULL,
    full_name       VARCHAR2(100) NOT NULL,
    role            VARCHAR2(20) NOT NULL,
    is_active       NUMBER(1) DEFAULT 1,
    created_at      TIMESTAMP DEFAULT SYSDATE,
    updated_at      TIMESTAMP DEFAULT SYSDATE
);

CREATE SEQUENCE users_seq START WITH 1;

-- Raw Materials Table
CREATE TABLE raw_materials (
    material_id     NUMBER PRIMARY KEY,
    material_name   VARCHAR2(100) NOT NULL,
    material_type   VARCHAR2(50) NOT NULL,
    supplier        VARCHAR2(100) NOT NULL,
    quantity_available NUMBER(10,2) NOT NULL DEFAULT 0,
    unit            VARCHAR2(20) NOT NULL,
    cost_per_unit   NUMBER(10,2) NOT NULL,
    status          VARCHAR2(20) DEFAULT 'available',
    expiry_date     TIMESTAMP,
    batch_number    VARCHAR2(50) NOT NULL,
    quality_grade   VARCHAR2(20),
    created_at      TIMESTAMP DEFAULT SYSDATE,
    updated_at      TIMESTAMP DEFAULT SYSDATE,
    created_by      NUMBER REFERENCES users(user_id)
);

CREATE SEQUENCE raw_materials_seq START WITH 1;
CREATE INDEX idx_materials_batch ON raw_materials(batch_number);

-- Production Orders Table
CREATE TABLE production_orders (
    order_id        NUMBER PRIMARY KEY,
    order_number    VARCHAR2(50) NOT NULL UNIQUE,
    product_name    VARCHAR2(100) NOT NULL,
    quantity_ordered NUMBER(10,2) NOT NULL,
    quantity_produced NUMBER(10,2) DEFAULT 0,
    unit            VARCHAR2(20) NOT NULL,
    status          VARCHAR2(20) DEFAULT 'pending',
    start_date      TIMESTAMP,
    expected_completion TIMESTAMP NOT NULL,
    actual_completion TIMESTAMP,
    assigned_to     NUMBER REFERENCES users(user_id),
    notes           CLOB,
    created_at      TIMESTAMP DEFAULT SYSDATE,
    updated_at      TIMESTAMP DEFAULT SYSDATE
);

CREATE SEQUENCE production_orders_seq START WITH 1;

-- Inventory Logs Table
CREATE TABLE inventory_logs (
    log_id          NUMBER PRIMARY KEY,
    material_id     NUMBER NOT NULL REFERENCES raw_materials(material_id),
    transaction_type VARCHAR2(20) NOT NULL,
    quantity_change NUMBER(10,2) NOT NULL,
    quantity_before NUMBER(10,2) NOT NULL,
    quantity_after  NUMBER(10,2) NOT NULL,
    reference_id    VARCHAR2(50),
    notes           CLOB,
    recorded_by     NUMBER REFERENCES users(user_id),
    recorded_at     TIMESTAMP DEFAULT SYSDATE
);

CREATE SEQUENCE inventory_logs_seq START WITH 1;
CREATE INDEX idx_inventory_material ON inventory_logs(material_id);

-- Quality Inspections Table
CREATE TABLE quality_inspections (
    inspection_id   NUMBER PRIMARY KEY,
    order_id        NUMBER NOT NULL REFERENCES production_orders(order_id),
    inspection_date TIMESTAMP DEFAULT SYSDATE,
    tested_by       NUMBER REFERENCES users(user_id),
    status          VARCHAR2(20) NOT NULL,
    tensile_strength NUMBER(10,2),
    hardness        NUMBER(10,2),
    ductility       NUMBER(10,2),
    surface_quality VARCHAR2(50),
    defects_found   CLOB,
    rework_required NUMBER(1) DEFAULT 0,
    passed_date     TIMESTAMP,
    notes           CLOB,
    created_at      TIMESTAMP DEFAULT SYSDATE
);

CREATE SEQUENCE quality_inspections_seq START WITH 1;
CREATE INDEX idx_quality_order ON quality_inspections(order_id);

-- Shipments Table
CREATE TABLE shipments (
    shipment_id     NUMBER PRIMARY KEY,
    shipment_number VARCHAR2(50) NOT NULL UNIQUE,
    order_id        NUMBER NOT NULL REFERENCES production_orders(order_id),
    destination     VARCHAR2(200) NOT NULL,
    quantity_shipped NUMBER(10,2) NOT NULL,
    unit            VARCHAR2(20) NOT NULL,
    status          VARCHAR2(20) DEFAULT 'pending',
    scheduled_date  TIMESTAMP NOT NULL,
    actual_ship_date TIMESTAMP,
    expected_delivery TIMESTAMP NOT NULL,
    actual_delivery TIMESTAMP,
    carrier         VARCHAR2(100),
    tracking_number VARCHAR2(100),
    logistics_handler NUMBER REFERENCES users(user_id),
    notes           CLOB,
    created_at      TIMESTAMP DEFAULT SYSDATE,
    updated_at      TIMESTAMP DEFAULT SYSDATE
);

CREATE SEQUENCE shipments_seq START WITH 1;

-- Create indexes on commonly queried columns
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_raw_materials_type ON raw_materials(material_type);
CREATE INDEX idx_prod_orders_status ON production_orders(status);
CREATE INDEX idx_shipments_status ON shipments(status);
```

## Sequence Management

Oracle uses sequences for auto-incrementing primary keys. The SQLAlchemy ORM automatically manages these.

To manually check sequences:

```sql
-- View all sequences
SELECT sequence_name, last_number FROM user_sequences;

-- Reset sequence if needed
ALTER SEQUENCE users_seq INCREMENT BY 1;
ALTER SEQUENCE users_seq NOCACHE;
```

## Backup and Maintenance

### Regular Backups

```bash
# Export data
exp steel_admin/password file=backup.dmp log=export.log

# Import data
imp steel_admin/password file=backup.dmp log=import.log
```

### Table Statistics

Update table statistics for query optimization:

```sql
BEGIN
  DBMS_STATS.gather_schema_stats(ownname=>'STEEL_ADMIN');
END;
/
```

## Troubleshooting

### Connection Refused
- Check Oracle service is running: `lsnrctl status`
- Verify TNS configuration in `tnsnames.ora`
- Check firewall allows port 1521

### Permission Denied
- Grant necessary privileges to user:
```sql
GRANT CREATE SESSION, CREATE TABLE, CREATE INDEX TO steel_admin;
```

### Table Already Exists
- Drop and recreate:
```sql
DROP TABLE shipments CASCADE CONSTRAINTS;
DROP TABLE quality_inspections CASCADE CONSTRAINTS;
DROP TABLE inventory_logs CASCADE CONSTRAINTS;
DROP TABLE production_orders CASCADE CONSTRAINTS;
DROP TABLE raw_materials CASCADE CONSTRAINTS;
DROP TABLE users CASCADE CONSTRAINTS;
```

### Sequence Issues
- Check sequence ownership:
```sql
SELECT sequence_owner, sequence_name FROM dba_sequences WHERE sequence_owner='STEEL_ADMIN';
```

## Performance Tuning

### Add Indexes for Better Performance

```sql
-- Additional indexes for frequently used queries
CREATE INDEX idx_materials_status ON raw_materials(status);
CREATE INDEX idx_materials_supplier ON raw_materials(supplier);
CREATE INDEX idx_orders_assigned ON production_orders(assigned_to);
CREATE INDEX idx_shipments_carrier ON shipments(carrier);
CREATE INDEX idx_quality_status ON quality_inspections(status);
```

### Enable Query Cache

```sql
-- Monitor query performance
SET TIMING ON;

-- Check execution plans
EXPLAIN PLAN FOR
  SELECT * FROM raw_materials WHERE quantity_available < 10;

SELECT * FROM TABLE(DBMS_XPLAN.display);
```

## User Management

### Create Additional Users

```sql
-- Create quality inspector user
CREATE USER quality_user IDENTIFIED BY "QualityPass123"
  DEFAULT TABLESPACE steel_mfg
  QUOTA UNLIMITED ON steel_mfg;

GRANT CREATE SESSION TO quality_user;

-- Grant table access (if using separate users)
GRANT SELECT, INSERT, UPDATE ON steel_admin.raw_materials TO quality_user;
```

### Monitor User Sessions

```sql
SELECT username, sid, serial# FROM v$session WHERE username='STEEL_ADMIN';

-- Kill session if needed
ALTER SYSTEM KILL SESSION 'sid,serial#';
```

## Archival and Cleanup

### Archive Old Records

```sql
-- Archive shipments older than 1 year
CREATE TABLE shipments_archive AS
  SELECT * FROM shipments 
  WHERE TRUNC(actual_delivery) < TRUNC(ADD_MONTHS(SYSDATE, -12));

DELETE FROM shipments 
  WHERE TRUNC(actual_delivery) < TRUNC(ADD_MONTHS(SYSDATE, -12));

COMMIT;
```

## Next Steps

1. Complete the setup steps above
2. Run `python scripts/init_db.py` to create tables
3. Start the application: `streamlit run app.py`
4. Log in with default credentials
5. Begin managing your manufacturing operations

---

For more information, refer to the main [README.md](./README.md) file.
