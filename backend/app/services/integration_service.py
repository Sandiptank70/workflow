from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import json
import importlib
from app.models import IntegrationType, Integration
from app.utils.encryption import encryption_service

class IntegrationService:
    """Service for managing integration types and integrations"""
    
    @staticmethod
    def create_integration_type(
        db: Session,
        name: str,
        parameters: List[Dict[str, Any]],
        description: Optional[str] = None,
        tasks: Optional[List[Dict[str, Any]]] = None
    ) -> IntegrationType:
        """Create a new integration type"""
        # Check if type already exists
        existing = db.query(IntegrationType).filter(IntegrationType.name == name).first()
        if existing:
            raise ValueError(f"Integration type '{name}' already exists")
        
        integration_type = IntegrationType(
            name=name,
            description=description,
            parameters=json.dumps(parameters),
            tasks=json.dumps(tasks) if tasks else None
        )
        db.add(integration_type)
        db.commit()
        db.refresh(integration_type)
        return integration_type
    
    @staticmethod
    def get_integration_types(db: Session) -> List[IntegrationType]:
        """Get all integration types"""
        return db.query(IntegrationType).all()
    
    @staticmethod
    def get_integration_type(db: Session, type_id: int) -> Optional[IntegrationType]:
        """Get integration type by ID"""
        return db.query(IntegrationType).filter(IntegrationType.id == type_id).first()
    
    @staticmethod
    def test_integration(
        db: Session,
        integration_type_id: int,
        credentials: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Test integration connection"""
        integration_type = IntegrationService.get_integration_type(db, integration_type_id)
        if not integration_type:
            return {
                "success": False,
                "message": "Integration type not found"
            }
        
        try:
            # Dynamically import the integration module
            module_name = integration_type.name.lower()
            module = importlib.import_module(f"app.integrations.{module_name}")
            
            # Call test_connection function
            if hasattr(module, "test_connection"):
                result = module.test_connection(credentials)
                return result
            else:
                return {
                    "success": False,
                    "message": f"test_connection not implemented for {integration_type.name}"
                }
        except ImportError:
            return {
                "success": False,
                "message": f"Integration module not found for {integration_type.name}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error testing connection: {str(e)}"
            }
    
    @staticmethod
    def create_integration(
        db: Session,
        name: str,
        integration_type_id: int,
        credentials: Dict[str, Any]
    ) -> Integration:
        """Create a new integration with encrypted credentials"""
        integration_type = IntegrationService.get_integration_type(db, integration_type_id)
        if not integration_type:
            raise ValueError("Integration type not found")
        
        # Encrypt credentials
        credentials_json = json.dumps(credentials)
        encrypted_credentials = encryption_service.encrypt(credentials_json)
        
        integration = Integration(
            name=name,
            integration_type_id=integration_type_id,
            credentials=encrypted_credentials
        )
        db.add(integration)
        db.commit()
        db.refresh(integration)
        return integration
    
    @staticmethod
    def get_integrations(db: Session) -> List[Integration]:
        """Get all integrations"""
        return db.query(Integration).all()
    
    @staticmethod
    def get_integration(db: Session, integration_id: int) -> Optional[Integration]:
        """Get integration by ID"""
        return db.query(Integration).filter(Integration.id == integration_id).first()
    
    @staticmethod
    def get_integration_credentials(db: Session, integration_id: int) -> Dict[str, Any]:
        """Get decrypted credentials for an integration"""
        integration = IntegrationService.get_integration(db, integration_id)
        if not integration:
            raise ValueError("Integration not found")
        
        # Decrypt credentials
        decrypted_json = encryption_service.decrypt(integration.credentials)
        return json.loads(decrypted_json)
    
    @staticmethod
    def delete_integration(db: Session, integration_id: int) -> bool:
        """Delete an integration"""
        integration = IntegrationService.get_integration(db, integration_id)
        if not integration:
            return False
        
        db.delete(integration)
        db.commit()
        return True