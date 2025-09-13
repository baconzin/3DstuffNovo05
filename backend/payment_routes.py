from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from payment_models import PaymentRequest, PaymentResponse, PaymentStatusResponse, MercadoPagoPayment, WebhookNotification
from mercado_pago_service import MercadoPagoService
from typing import Dict, Any
import logging
import json
from datetime import datetime

router = APIRouter(prefix="/api/payments", tags=["payments"])
logger = logging.getLogger(__name__)

@router.post("/create", response_model=PaymentResponse)
async def create_payment(
    payment_request: PaymentRequest,
    db: Session = Depends(get_db)
):
    """Criar novo pagamento"""
    try:
        mp_service = MercadoPagoService()
        
        # Validar produto
        product_info = mp_service.get_product_info(payment_request.product_id)
        if not product_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Produto não encontrado"
            )
        
        # Preparar dados do pagamento
        payment_data = {
            "product_id": payment_request.product_id,
            "quantity": payment_request.quantity,
            "customer_email": payment_request.customer_email,
            "customer_document": payment_request.customer_document,
            "customer_name": payment_request.customer_name,
            "installments": payment_request.installments,
            "card_token": payment_request.card_token
        }
        
        # Criar pagamento baseado no método
        if payment_request.payment_method == "pix":
            result = await mp_service.create_pix_payment(payment_data)
        elif payment_request.payment_method == "credit_card":
            if not payment_request.card_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Token do cartão é obrigatório"
                )
            result = await mp_service.create_credit_card_payment(payment_data)
        elif payment_request.payment_method == "boleto":
            result = await mp_service.create_boleto_payment(payment_data)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Método de pagamento inválido"
            )
        
        if result["success"]:
            # Salvar no banco de dados
            db_payment = MercadoPagoPayment(
                payment_id=result["payment_id"],
                external_reference=result["external_reference"],
                status=result["status"],
                payment_method_id=payment_request.payment_method,
                payment_type=payment_request.payment_method,
                amount=result["amount"],
                currency="BRL",
                installments=payment_request.installments or 1,
                customer_email=payment_request.customer_email,
                customer_document=payment_request.customer_document,
                customer_name=payment_request.customer_name,
                product_id=payment_request.product_id,
                product_name=product_info["name"],
                description=product_info["description"],
                payment_data=result.get("transaction_data", {}),
                qr_code=result.get("qr_code", ""),
                ticket_url=result.get("ticket_url", ""),
                barcode=result.get("barcode", "")
            )
            
            db.add(db_payment)
            db.commit()
            db.refresh(db_payment)
            
            return PaymentResponse(
                success=True,
                payment_id=result["payment_id"],
                status=result["status"],
                status_detail=result.get("status_detail", ""),
                amount=result["amount"],
                qr_code=result.get("qr_code", ""),
                qr_code_base64=result.get("qr_code_base64", ""),
                ticket_url=result.get("ticket_url", ""),
                barcode=result.get("barcode", ""),
                message="Pagamento criado com sucesso",
                transaction_data=result.get("transaction_data", {})
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar pagamento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/{payment_id}/status", response_model=PaymentStatusResponse)
async def get_payment_status(
    payment_id: str,
    db: Session = Depends(get_db)
):
    """Buscar status do pagamento"""
    try:
        mp_service = MercadoPagoService()
        
        # Buscar status no Mercado Pago
        result = await mp_service.get_payment_status(payment_id)
        
        if result["success"]:
            # Atualizar no banco de dados
            db_payment = db.query(MercadoPagoPayment).filter(
                MercadoPagoPayment.payment_id == payment_id
            ).first()
            
            if db_payment:
                db_payment.status = result["status"]
                db_payment.status_detail = result["status_detail"]
                db_payment.net_amount = result.get("net_amount")
                db_payment.updated_at = datetime.utcnow()
                
                if result["status"] == "approved" and not db_payment.approved_at:
                    db_payment.approved_at = datetime.utcnow()
                
                db.commit()
            
            return PaymentStatusResponse(
                payment_id=result["payment_id"],
                status=result["status"],
                status_detail=result["status_detail"],
                payment_method=result["payment_method"],
                amount=result["amount"],
                net_amount=result.get("net_amount"),
                currency=result["currency"],
                created_at=datetime.fromisoformat(result["created_at"].replace("Z", "+00:00")),
                approved_at=datetime.fromisoformat(result["approved_at"].replace("Z", "+00:00")) if result.get("approved_at") else None
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pagamento não encontrado"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/installments/{product_id}")
async def get_installment_options(product_id: str):
    """Buscar opções de parcelamento para um produto"""
    try:
        mp_service = MercadoPagoService()
        
        # Buscar informações do produto
        product_info = mp_service.get_product_info(product_id)
        if not product_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Produto não encontrado"
            )
        
        # Buscar opções de parcelamento
        result = await mp_service.get_installment_options(product_info["price"])
        
        if result["success"]:
            return {
                "success": True,
                "product_price": product_info["price"],
                "installment_options": result["options"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao calcular parcelamento"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar parcelamento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/webhook")
async def webhook_handler(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Handler para webhooks do Mercado Pago"""
    try:
        # Obter dados do webhook
        body = await request.body()
        webhook_data = json.loads(body.decode())
        
        logger.info(f"Webhook recebido: {webhook_data}")
        
        # Salvar notificação
        notification = WebhookNotification(
            notification_id=str(webhook_data.get("id", "")),
            topic=webhook_data.get("topic", ""),
            resource=webhook_data.get("resource", ""),
            payment_id=webhook_data.get("data", {}).get("id", ""),
            payload=webhook_data
        )
        
        db.add(notification)
        db.commit()
        
        # Processar notificação em background
        if webhook_data.get("topic") == "payment":
            payment_id = webhook_data.get("data", {}).get("id")
            if payment_id:
                background_tasks.add_task(
                    process_payment_notification,
                    payment_id,
                    notification.id
                )
        
        return {"status": "received"}
        
    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar webhook"
        )

async def process_payment_notification(payment_id: str, notification_id: int):
    """Processar notificação de pagamento em background"""
    from database import SessionLocal
    
    db = SessionLocal()
    try:
        mp_service = MercadoPagoService()
        
        # Buscar status atualizado do pagamento
        result = await mp_service.get_payment_status(payment_id)
        
        if result["success"]:
            # Atualizar pagamento no banco
            db_payment = db.query(MercadoPagoPayment).filter(
                MercadoPagoPayment.payment_id == payment_id
            ).first()
            
            if db_payment:
                old_status = db_payment.status
                db_payment.status = result["status"]
                db_payment.status_detail = result["status_detail"]
                db_payment.updated_at = datetime.utcnow()
                
                if result["status"] == "approved" and old_status != "approved":
                    db_payment.approved_at = datetime.utcnow()
                    logger.info(f"Pagamento aprovado: {payment_id}")
                    
                    # Aqui você pode adicionar lógica para:
                    # - Enviar email de confirmação
                    # - Atualizar estoque
                    # - Processar entrega
                
                db.commit()
        
        # Marcar notificação como processada
        notification = db.query(WebhookNotification).filter(
            WebhookNotification.id == notification_id
        ).first()
        
        if notification:
            notification.processed = True
            db.commit()
        
        logger.info(f"Notificação processada: {payment_id}")
        
    except Exception as e:
        logger.error(f"Erro ao processar notificação: {str(e)}")
        db.rollback()
    finally:
        db.close()