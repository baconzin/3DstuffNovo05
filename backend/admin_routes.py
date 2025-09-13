from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from inventory_service import inventory_service
from email_service import email_service
from webhook_service import webhook_service
from typing import Dict, List
import logging

router = APIRouter(prefix="/api/admin", tags=["admin"])
logger = logging.getLogger(__name__)

@router.get("/inventory/summary")
async def get_inventory_summary():
    """Obter resumo geral do estoque"""
    try:
        from database import products_collection
        
        products = await products_collection.find({"active": True}).to_list(100)
        inventory_data = []
        
        total_stock = 0
        total_reserved = 0
        
        for product in products:
            stock_info = await inventory_service.get_stock_info(product["id"])
            
            if stock_info:
                inventory_data.append({
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "category": product["category"],
                    "price": product["price"],
                    "available_quantity": stock_info["available_quantity"],
                    "reserved_quantity": stock_info["reserved_quantity"],
                    "sold_quantity": stock_info["sold_quantity"],
                    "status": stock_info["status"],
                    "needs_restock": stock_info["needs_restock"]
                })
                
                total_stock += stock_info["available_quantity"]
                total_reserved += stock_info["reserved_quantity"]
        
        return {
            "total_products": len(inventory_data),
            "total_stock": total_stock,
            "total_reserved": total_reserved,
            "products": inventory_data
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter resumo do estoque: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inventory/low-stock")
async def get_low_stock_alert():
    """Obter produtos com estoque baixo"""
    try:
        low_stock_products = await inventory_service.get_low_stock_products()
        
        # Enriquecer com dados do produto
        from database import products_collection
        enriched_data = []
        
        for stock_item in low_stock_products:
            product = await products_collection.find_one({"id": stock_item["product_id"]})
            if product:
                enriched_data.append({
                    "product_id": stock_item["product_id"],
                    "product_name": product["name"],
                    "category": product["category"],
                    "available_quantity": stock_item["available_quantity"],
                    "reorder_level": stock_item["reorder_level"],
                    "status": stock_item["status"]
                })
        
        return {
            "alert_count": len(enriched_data),
            "low_stock_products": enriched_data
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter alertas de estoque: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/inventory/restock/{product_id}")
async def restock_product(product_id: str, quantity: int):
    """Repor estoque de um produto"""
    try:
        result = await inventory_service.add_stock(
            product_id, 
            quantity, 
            f"Reposição manual via admin - {quantity} unidades"
        )
        
        if result["success"]:
            logger.info(f"Reposição de estoque: {product_id} - {quantity} unidades")
            return {
                "success": True,
                "message": result["message"],
                "product_id": product_id,
                "quantity_added": quantity
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao repor estoque: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sales/summary")
async def get_sales_summary():
    """Obter resumo de vendas"""
    try:
        stats = await webhook_service.get_webhook_stats()
        
        return {
            "sales_summary": stats.get("webhook_stats", []),
            "last_updated": stats.get("last_updated")
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter resumo de vendas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test/send-email")
async def test_email_system(email: str):
    """Testar sistema de email"""
    try:
        test_data = {
            "email": email,
            "name": "Teste Admin",
            "message": "Este é um email de teste do sistema administrativo."
        }
        
        success = await email_service.send_contact_confirmation(test_data)
        
        return {
            "success": success,
            "message": "Email de teste enviado com sucesso" if success else "Erro ao enviar email"
        }
        
    except Exception as e:
        logger.error(f"Erro no teste de email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def admin_health_check():
    """Verificação de saúde do sistema administrativo"""
    try:
        # Verificar inventário
        inventory_ok = True
        try:
            await inventory_service.get_low_stock_products()
        except:
            inventory_ok = False
        
        # Verificar webhook
        webhook_ok = True
        try:
            await webhook_service.get_webhook_stats()
        except:
            webhook_ok = False
        
        return {
            "admin_system": "healthy",
            "inventory_service": "ok" if inventory_ok else "error",
            "webhook_service": "ok" if webhook_ok else "error",
            "email_service": "configured" if email_service.sendgrid_key else "mock_mode"
        }
        
    except Exception as e:
        logger.error(f"Erro na verificação de saúde: {e}")
        raise HTTPException(status_code=500, detail=str(e))