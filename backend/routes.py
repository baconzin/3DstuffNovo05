from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models import (
    ProductResponse, 
    ContactMessageCreate, 
    ContactMessageResponse, 
    CompanyInfoResponse
)
from database import products_collection, contacts_collection, company_info_collection
from datetime import datetime
import uuid

router = APIRouter(prefix="/api")

# Produtos Endpoints
@router.get("/products", response_model=List[ProductResponse])
async def get_products(category: Optional[str] = Query(None)):
    """Busca produtos, opcionalmente filtrados por categoria"""
    try:
        query = {"active": True}
        if category and category != "Todos":
            query["category"] = category
        
        products_cursor = products_collection.find(query)
        products = await products_cursor.to_list(1000)
        
        return [
            ProductResponse(
                id=product["id"],
                name=product["name"],
                description=product["description"],
                price=product["price"],
                image=product["image"],
                category=product["category"]
            )
            for product in products
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produtos: {str(e)}")

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Busca um produto específico por ID"""
    try:
        product = await products_collection.find_one({"id": product_id, "active": True})
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        return ProductResponse(
            id=product["id"],
            name=product["name"],
            description=product["description"],
            price=product["price"],
            image=product["image"],
            category=product["category"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produto: {str(e)}")

# Contato Endpoints
@router.post("/contact", response_model=ContactMessageResponse)
async def create_contact_message(contact_data: ContactMessageCreate):
    """Cria uma nova mensagem de contato"""
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
        
        return ContactMessageResponse(**contact_message)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar mensagem de contato: {str(e)}")

@router.get("/contact", response_model=List[ContactMessageResponse])
async def get_contact_messages():
    """Lista todas as mensagens de contato (para admin)"""
    try:
        messages_cursor = contacts_collection.find({}).sort("created_at", -1)
        messages = await messages_cursor.to_list(1000)
        
        return [
            ContactMessageResponse(
                id=msg["id"],
                name=msg["name"],
                email=msg["email"],
                message=msg["message"],
                created_at=msg["created_at"],
                status=msg["status"]
            )
            for msg in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar mensagens: {str(e)}")

# Informações da Empresa Endpoints
@router.get("/company-info", response_model=CompanyInfoResponse)
async def get_company_info():
    """Busca informações da empresa"""
    try:
        company_info = await company_info_collection.find_one({})
        if not company_info:
            raise HTTPException(status_code=404, detail="Informações da empresa não encontradas")
        
        return CompanyInfoResponse(
            name=company_info["name"],
            slogan=company_info["slogan"],
            about=company_info["about"],
            whatsapp=company_info["whatsapp"],
            email=company_info["email"],
            social_media=company_info["social_media"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar informações da empresa: {str(e)}")

# Health Check
@router.get("/health")
async def health_check():
    """Endpoint de verificação de saúde da API"""
    return {"status": "healthy", "message": "3D Stuff API está funcionando!"}