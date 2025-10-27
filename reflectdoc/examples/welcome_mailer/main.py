"""Main application entry point for the Welcome Mailer system."""

import sys
from typing import List

from .user import User
from .email_service import EmailService
from .config import Config


def get_user_input() -> User:
    """Collect user information from command line input.
    
    Returns:
        User object with provided information
    """
    print("\n" + "="*50)
    print("Welcome Mailer - User Registration")
    print("="*50 + "\n")
    
    name = input("Enter your name: ").strip()
    email = input("Enter your email address: ").strip()
    address = input("Enter your address: ").strip()
    phone = input("Enter your phone (optional, press Enter to skip): ").strip() or None
    
    try:
        user = User(name=name, email=email, address=address, phone=phone)
        return user
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def display_user_info(user: User) -> None:
    """Display user information for confirmation.
    
    Args:
        user: User object to display
    """
    print("\n" + "-"*50)
    print("User Information:")
    print("-"*50)
    print(f"Name: {user.name}")
    print(f"Email: {user.email}")
    print(f"Address: {user.address}")
    if user.phone:
        print(f"Phone: {user.phone}")
    print("-"*50 + "\n")


def send_welcome_email(user: User, dry_run: bool = True) -> bool:
    """Send welcome email to the user.
    
    Args:
        user: User object containing recipient information
        dry_run: If True, simulate sending (default for demo)
        
    Returns:
        True if email sent successfully
    """
    email_service = EmailService()
    print(f"\n📧 Sending welcome email to {user.email}...")
    
    success = email_service.send_email(user, dry_run=dry_run)
    
    if success:
        print(f"✅ Welcome email sent successfully!")
        return True
    else:
        print(f"❌ Failed to send welcome email.")
        return False


def process_batch_users(users: List[User], dry_run: bool = True) -> dict:
    """Process multiple users and send welcome emails.
    
    Args:
        users: List of User objects
        dry_run: If True, simulate sending
        
    Returns:
        Dictionary with processing results
    """
    email_service = EmailService()
    print(f"\n📧 Processing {len(users)} users...")
    
    results = email_service.send_bulk_emails(users, dry_run=dry_run)
    
    print("\n" + "="*50)
    print("Batch Processing Results:")
    print("="*50)
    print(f"✅ Successful: {results['success_count']}")
    print(f"❌ Failed: {results['failed_count']}")
    if results['failed_recipients']:
        print(f"Failed recipients: {', '.join(results['failed_recipients'])}")
    print("="*50 + "\n")
    
    return results


def main():
    """Main application function."""
    print(f"\n🎉 {Config.APP_NAME} v{Config.APP_VERSION}")
    print(f"Configuration: {Config.get_config_dict()}\n")
    
    # Interactive mode - collect single user input
    user = get_user_input()
    
    # Display user information for confirmation
    display_user_info(user)
    
    # Confirm before sending
    confirm = input("Send welcome email? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        send_welcome_email(user, dry_run=True)
    else:
        print("\n❌ Email sending cancelled.")
        return
    
    print("\n✨ Thank you for using Welcome Mailer!\n")


def demo_batch_mode():
    """Demonstrate batch email processing with sample users."""
    print("\n🔬 Running Batch Mode Demo\n")
    
    # Create sample users
    sample_users = [
        User(name="Alice Johnson", email="alice@example.com", address="123 Main St, NYC", phone="555-0101"),
        User(name="Bob Smith", email="bob@example.com", address="456 Oak Ave, LA", phone="555-0102"),
        User(name="Charlie Brown", email="charlie@example.com", address="789 Pine Rd, Chicago"),
    ]
    
    # Process batch
    process_batch_users(sample_users, dry_run=True)


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        demo_batch_mode()
    else:
        main()
