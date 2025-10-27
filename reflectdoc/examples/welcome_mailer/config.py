"""Configuration settings for the welcome mailer application."""

import os
from typing import Dict


class Config:
    """Configuration class for email service settings."""
    
    # Email service configuration
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@welcomemailer.com")
    SENDER_NAME = os.getenv("SENDER_NAME", "Welcome Mailer Team")
    
    # Email templates
    WELCOME_EMAIL_SUBJECT = "Welcome to Our Platform!"
    
    # Application settings
    APP_NAME = "Welcome Mailer"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def get_email_template(cls, user_name: str, address: str) -> str:
        """Generate personalized email template.
        
        Args:
            user_name: Name of the user
            address: Address of the user
            
        Returns:
            Formatted email content
        """
        return f"""
Dear {user_name},

Welcome to {cls.APP_NAME}!

We're excited to have you join our community. Your registration has been successfully completed.

Your Details:
- Name: {user_name}
- Address: {address}

What's Next?
1. Explore our features and services
2. Complete your profile for a better experience
3. Connect with our community

If you have any questions or need assistance, feel free to reach out to our support team.

Best regards,
{cls.SENDER_NAME}

---
This is an automated message. Please do not reply directly to this email.
{cls.APP_NAME} v{cls.APP_VERSION}
"""
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, any]:
        """Return configuration as dictionary."""
        return {
            "smtp_server": cls.SMTP_SERVER,
            "smtp_port": cls.SMTP_PORT,
            "sender_email": cls.SENDER_EMAIL,
            "sender_name": cls.SENDER_NAME,
            "app_name": cls.APP_NAME,
            "app_version": cls.APP_VERSION,
            "debug": cls.DEBUG
        }
