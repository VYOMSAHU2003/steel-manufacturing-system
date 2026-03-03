import pandas as pd
from datetime import datetime
import streamlit as st

def format_currency(value: float) -> str:
    """Format value as currency"""
    return f"${value:,.2f}"

def format_date(date: datetime) -> str:
    """Format datetime as readable string"""
    if date is None:
        return "N/A"
    return date.strftime("%Y-%m-%d %H:%M")

def format_date_only(date: datetime) -> str:
    """Format datetime as date only"""
    if date is None:
        return "N/A"
    return date.strftime("%Y-%m-%d")

def calculate_cost(quantity: float, cost_per_unit: float) -> float:
    """Calculate total cost"""
    return quantity * cost_per_unit

def get_material_status_color(status: str) -> str:
    """Get color for material status badge"""
    colors = {
        "available": "🟢",
        "reserved": "🟡",
        "used": "⚫",
        "expired": "🔴"
    }
    return colors.get(status, "⚪")

def get_order_status_color(status: str) -> str:
    """Get color for order status badge"""
    colors = {
        "pending": "🟡",
        "in_progress": "🔵",
        "completed": "🟢",
        "cancelled": "🔴"
    }
    return colors.get(status, "⚪")

def get_quality_status_color(status: str) -> str:
    """Get color for quality status"""
    colors = {
        "pass": "🟢",
        "fail": "🔴",
        "rework": "🟡"
    }
    return colors.get(status, "⚪")

def get_shipment_status_color(status: str) -> str:
    """Get color for shipment status"""
    colors = {
        "pending": "🟡",
        "in_transit": "🔵",
        "delivered": "🟢",
        "cancelled": "🔴"
    }
    return colors.get(status, "⚪")

def create_dataframe_display(data_list, columns_map: dict = None) -> pd.DataFrame:
    """Convert list of objects to dataframe for display"""
    if not data_list:
        return pd.DataFrame()
    
    df = pd.DataFrame([vars(item) for item in data_list])
    
    if columns_map:
        df = df.rename(columns=columns_map)
    
    return df

def validate_required_fields(data: dict, required_fields: list) -> tuple[bool, str]:
    """Validate that required fields are present and not empty"""
    for field in required_fields:
        if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
            return False, f"Required field missing: {field}"
    return True, ""

def validate_positive_number(value: float, field_name: str) -> tuple[bool, str]:
    """Validate that a value is positive"""
    try:
        num = float(value)
        if num <= 0:
            return False, f"{field_name} must be positive"
        return True, ""
    except ValueError:
        return False, f"{field_name} must be a valid number"

def display_success_message(message: str):
    """Display a success message"""
    st.success(f"✓ {message}")

def display_error_message(message: str):
    """Display an error message"""
    st.error(f"✗ {message}")

def display_info_message(message: str):
    """Display an info message"""
    st.info(f"ℹ {message}")

def display_warning_message(message: str):
    """Display a warning message"""
    st.warning(f"⚠ {message}")
