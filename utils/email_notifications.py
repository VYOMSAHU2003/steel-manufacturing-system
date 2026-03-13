"""
Email notification helpers for low stock alerts.
"""

import os
import smtplib
from email.message import EmailMessage
from typing import Dict, List

from models.database_models import User, UserRole


def _parse_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _get_management_emails(db_session) -> List[str]:
    configured_emails = os.getenv("MANAGEMENT_EMAILS", "").strip()
    if configured_emails:
        return [email.strip() for email in configured_emails.split(",") if email.strip()]

    management_roles = [
        UserRole.ADMIN,
        UserRole.STORE_MANAGER,
        UserRole.PRODUCTION_MANAGER,
    ]

    users = db_session.query(User).filter(
        User.is_active == True,
        User.role.in_(management_roles)
    ).all()

    emails = []
    for user in users:
        if user.email and user.email.strip():
            emails.append(user.email.strip())

    # Preserve order while removing duplicates.
    unique = list(dict.fromkeys(emails))
    return unique


def send_low_stock_email_notification(
    db_session,
    material_name: str,
    material_type: str,
    current_stock: float,
    unit: str,
    threshold: float,
    alert_type: str,
) -> Dict[str, object]:
    """Send low stock alert email to management team.

    Returns a structured status so caller can log/handle failures safely.
    """
    smtp_enabled = _parse_bool(os.getenv("SMTP_ENABLED", "false"), default=False)
    if not smtp_enabled:
        return {"success": False, "message": "SMTP notifications disabled"}

    recipients = _get_management_emails(db_session)
    if not recipients:
        return {"success": False, "message": "No management email recipients configured"}

    smtp_host = os.getenv("SMTP_HOST", "").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_use_tls = _parse_bool(os.getenv("SMTP_USE_TLS", "true"), default=True)
    smtp_timeout = int(os.getenv("SMTP_TIMEOUT", "20"))
    from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username).strip()

    if not smtp_host or not from_email:
        return {"success": False, "message": "SMTP_HOST or SMTP_FROM_EMAIL/SMTP_USERNAME is missing"}

    subject = f"[{alert_type.upper()}] Raw Material Low Stock Alert - {material_name}"
    body = (
        "Dear Management Team,\n\n"
        "A low stock condition has been detected for a raw material.\n\n"
        f"Material Name: {material_name}\n"
        f"Material Type: {material_type}\n"
        f"Current Stock: {current_stock:.2f} {unit}\n"
        f"Threshold: {threshold:.2f} {unit}\n"
        f"Alert Severity: {alert_type.upper()}\n\n"
        "Action Required: Please arrange procurement/replenishment at the earliest.\n\n"
        "This is an automated notification from the Steel Plant Inventory System."
    )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = ", ".join(recipients)
    message.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=smtp_timeout) as smtp:
            if smtp_use_tls:
                smtp.starttls()

            if smtp_username and smtp_password:
                smtp.login(smtp_username, smtp_password)

            smtp.send_message(message)

        return {
            "success": True,
            "message": f"Email sent to {len(recipients)} management recipients"
        }
    except Exception as exc:
        return {"success": False, "message": f"Email send failed: {exc}"}
