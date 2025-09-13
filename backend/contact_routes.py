from fastapi import APIRouter, HTTPException, BackgroundTasks
from models import ContactMessageCreate, ContactMessageResponse
from database import contacts_collection
from email_service import email_service
from datetime import datetime
import uuid
import logging

router = APIRouter(prefix="/api", tags=["contact"])
logger = logging.getLogger(__name__)

@router.post("/contact", response_model=ContactMessageResponse)
async def create_contact_message(
    contact_data: ContactMessageCreate,
    background_tasks: BackgroundTasks
):
    """Criar uma nova mensagem de contato com email automático"""
    try:
        contact_message = {
            "id": str(uuid.uuid4()),
            "name": contact_data.name,
            "email": contact_data.email,
            "message": contact_data.message,
            "created_at": datetime.utcnow(),
            "status": "new"
        }
        
        result = await contacts_collection.insert_one(contact_message)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Erro ao salvar mensagem")
        
        # Enviar email de confirmação em background
        email_data = {
            "email": contact_data.email,
            "name": contact_data.name,
            "message": contact_data.message
        }
        
        background_tasks.add_task(
            email_service.send_contact_confirmation,
            email_data
        )
        
        logger.info(f"Nova mensagem de contato: {contact_data.name} - {contact_data.email}")
        
        return ContactMessageResponse(**contact_message)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar mensagem de contato: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Erro interno do servidor"
        )