"""User model for storing user information."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Represents a user with contact information."""
    
    name: str
    email: str
    address: str
    phone: Optional[str] = None
    
    def __post_init__(self):
        """Validate user data after initialization."""
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address")
        
        if not self.address or not self.address.strip():
            raise ValueError("Address cannot be empty")
    
    def get_full_name(self) -> str:
        """Return the full name of the user."""
        return self.name.strip()
    
    def get_greeting(self) -> str:
        """Generate a personalized greeting for the user."""
        return f"Hello {self.get_full_name()}!"
    
    def to_dict(self) -> dict:
        """Convert user object to dictionary."""
        return {
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone
        }
