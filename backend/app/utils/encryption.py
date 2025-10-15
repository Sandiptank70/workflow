from cryptography.fernet import Fernet
import os
import base64
from dotenv import load_dotenv

load_dotenv()

class EncryptionService:
    """Handle encryption and decryption of sensitive data"""
    
    def __init__(self):
        encryption_key = os.getenv("ENCRYPTION_KEY")
        if not encryption_key:
            raise ValueError("ENCRYPTION_KEY environment variable not set")
        
        # Ensure key is proper Fernet format
        try:
            self.cipher = Fernet(encryption_key.encode())
        except Exception:
            # Generate a new key if invalid
            raise ValueError("Invalid ENCRYPTION_KEY. Generate one using: Fernet.generate_key()")
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data and return base64 encoded string"""
        encrypted_data = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt base64 encoded string and return original data"""
        try:
            decoded_data = base64.b64decode(encrypted_data.encode())
            decrypted_data = self.cipher.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def generate_key() -> str:
        """Generate a new Fernet key"""
        return Fernet.generate_key().decode()

# Global instance
encryption_service = EncryptionService()
