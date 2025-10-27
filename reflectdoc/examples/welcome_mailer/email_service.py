"""Email service for sending welcome emails to users."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

from .user import User
from .config import Config


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending personalized welcome emails."""
    
    def __init__(self, smtp_server: Optional[str] = None, smtp_port: Optional[int] = None):
        """Initialize email service with SMTP configuration.
        
        Args:
            smtp_server: SMTP server address (default from Config)
            smtp_port: SMTP server port (default from Config)
        """
        self.smtp_server = smtp_server or Config.SMTP_SERVER
        self.smtp_port = smtp_port or Config.SMTP_PORT
        self.sender_email = Config.SENDER_EMAIL
        self.sender_name = Config.SENDER_NAME
        logger.info(f"EmailService initialized with server: {self.smtp_server}:{self.smtp_port}")
    
    def create_welcome_email(self, user: User) -> MIMEMultipart:
        """Create a personalized welcome email for the user.
        
        Args:
            user: User object containing recipient information
            
        Returns:
            MIMEMultipart email message
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = Config.WELCOME_EMAIL_SUBJECT
        message["From"] = f"{self.sender_name} <{self.sender_email}>"
        message["To"] = user.email
        
        # Generate personalized email body
        email_body = Config.get_email_template(user.name, user.address)
        
        # Create plain text part
        text_part = MIMEText(email_body, "plain")
        message.attach(text_part)
        
        logger.info(f"Welcome email created for {user.email}")
        return message
    
    def send_email(self, user: User, dry_run: bool = False) -> bool:
        """Send welcome email to the user.
        
        Args:
            user: User object containing recipient information
            dry_run: If True, simulate sending without actually sending
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            message = self.create_welcome_email(user)
            
            if dry_run or Config.DEBUG:
                logger.info(f"[DRY RUN] Would send email to {user.email}")
                logger.info(f"Subject: {message['Subject']}")
                logger.info(f"Body preview: {message.as_string()[:200]}...")
                return True
            
            # In production, this would connect to actual SMTP server
            # For demo purposes, we just simulate success
            logger.info(f"✉️  Email sent successfully to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {user.email}: {str(e)}")
            return False
    
    def send_bulk_emails(self, users: list[User], dry_run: bool = False) -> dict:
        """Send welcome emails to multiple users.
        
        Args:
            users: List of User objects
            dry_run: If True, simulate sending without actually sending
            
        Returns:
            Dictionary with success count and failed recipients
        """
        results = {
            "success_count": 0,
            "failed_count": 0,
            "failed_recipients": []
        }
        
        for user in users:
            if self.send_email(user, dry_run):
                results["success_count"] += 1
            else:
                results["failed_count"] += 1
                results["failed_recipients"].append(user.email)
        
        logger.info(f"Bulk email complete: {results['success_count']} sent, {results['failed_count']} failed")
        return results
