"""Welcome Mailer - A simple email service for sending personalized welcome emails.

This package provides functionality to:
- Collect user information (name, email, address)
- Send personalized welcome emails
- Process batch email operations
"""

__version__ = "1.0.0"
__author__ = "Welcome Mailer Team"

from .user import User
from .email_service import EmailService
from .config import Config

__all__ = ["User", "EmailService", "Config"]
