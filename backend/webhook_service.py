from typing import Dict
import logging
from datetime import datetime
from email_service import email_service
from inventory_service import inventory_service
from database import db

logger = logging.getLogger(__name__)

class WebhookService:
    def __init__(self):
        self.payments_collection = db.mercado_pago_payments
    
    async def process_payment_notification(self, payment_id: str, payment_data: Dict):
        """Processar notificação de pagamento do Mercado Pago"""
        try:
            logger.info(f"Processando notificação de pagamento: {payment_id}")
            
            status = payment_data.get("status")
            
            # Buscar dados do pagamento no banco
            payment_record = await self.payments_collection.find_one({"payment_id": str(payment_id)})
            
            if not payment_record:
                logger.error(f"Pagamento {payment_id} não encontrado no banco de dados")
                return False
            
            old_status = payment_record.get("status")
            
            # Atualizar status no banco
            await self.payments_collection.update_one(
                {"payment_id": str(payment_id)},
                {
                    "$set": {
                        "status": status,
                        "status_detail": payment_data.get("status_detail", ""),
                        "updated_at": datetime.utcnow(),
                        "webhook_data": payment_data
                    }
                }
            )
            
            # Processar baseado no status
            if status == "approved" and old_status != "approved":
                await self._handle_payment_approved(payment_record, payment_data)
            elif status == "cancelled" or status == "rejected":
                await self._handle_payment_failed(payment_record, payment_data)
            elif status == "pending":
                await self._handle_payment_pending(payment_record, payment_data)
            
            logger.info(f"Notificação processada com sucesso: {payment_id} - Status: {status}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar notificação: {e}")
            return False
    
    async def _handle_payment_approved(self, payment_record: Dict, payment_data: Dict):
        """Lidar com pagamento aprovado"""
        try:
            logger.info(f"Pagamento aprovado: {payment_record['payment_id']}")
            
            # 1. Confirmar venda no estoque
            product_id = payment_record["product_id"]
            quantity = 1  # Por enquanto, sempre 1 produto
            order_id = payment_record["payment_id"]
            
            # Verificar se o estoque já foi reservado
            stock_info = await inventory_service.get_stock_info(product_id)
            
            if stock_info and stock_info["reserved_quantity"] > 0:
                # Confirmar a venda (mover de reservado para vendido)
                await inventory_service.confirm_sale(product_id, quantity, order_id)
            else:
                # Se não havia reserva, decrementar diretamente
                availability = await inventory_service.check_availability(product_id, quantity)
                if availability["can_fulfill"]:
                    await inventory_service.reserve_stock(product_id, quantity, order_id)
                    await inventory_service.confirm_sale(product_id, quantity, order_id)
                else:
                    logger.warning(f"Produto {product_id} sem estoque suficiente, mas pagamento aprovado")
            
            # 2. Atualizar status no registro
            await self.payments_collection.update_one(
                {"payment_id": payment_record["payment_id"]},
                {
                    "$set": {
                        "approved_at": datetime.utcnow(),
                        "inventory_updated": True
                    }
                }
            )
            
            # 3. Enviar email de confirmação
            email_data = {
                "customer_email": payment_record["customer_email"],
                "customer_name": payment_record["customer_name"],
                "product_name": payment_record["product_name"],
                "amount": payment_record["amount"],
                "payment_method": payment_record["payment_method_id"],
                "payment_id": payment_record["payment_id"]
            }
            
            await email_service.send_payment_confirmation(email_data)
            
            logger.info(f"Pagamento aprovado processado completamente: {payment_record['payment_id']}")
            
        except Exception as e:
            logger.error(f"Erro ao processar pagamento aprovado: {e}")
    
    async def _handle_payment_failed(self, payment_record: Dict, payment_data: Dict):
        """Lidar com pagamento cancelado/rejeitado"""
        try:
            logger.info(f"Pagamento falhou: {payment_record['payment_id']} - Status: {payment_data.get('status')}")
            
            # 1. Cancelar reserva de estoque se existir
            product_id = payment_record["product_id"]
            quantity = 1
            order_id = payment_record["payment_id"]
            
            await inventory_service.cancel_reservation(product_id, quantity, order_id)
            
            # 2. Atualizar registro
            await self.payments_collection.update_one(
                {"payment_id": payment_record["payment_id"]},
                {
                    "$set": {
                        "cancelled_at": datetime.utcnow(),
                        "inventory_released": True
                    }
                }
            )
            
            logger.info(f"Pagamento falhou processado: {payment_record['payment_id']}")
            
        except Exception as e:
            logger.error(f"Erro ao processar pagamento falhou: {e}")
    
    async def _handle_payment_pending(self, payment_record: Dict, payment_data: Dict):
        """Lidar com pagamento pendente"""
        try:
            logger.info(f"Pagamento pendente: {payment_record['payment_id']}")
            
            # 1. Reservar estoque se ainda não foi reservado
            product_id = payment_record["product_id"]
            quantity = 1
            order_id = payment_record["payment_id"]
            
            # Verificar se já tem reserva
            stock_info = await inventory_service.get_stock_info(product_id)
            
            if not stock_info or stock_info["reserved_quantity"] == 0:
                await inventory_service.reserve_stock(product_id, quantity, order_id)
            
            # 2. Enviar email de pagamento pendente (apenas na primeira vez)
            if payment_record.get("status") != "pending":
                email_data = {
                    "customer_email": payment_record["customer_email"],
                    "customer_name": payment_record["customer_name"],
                    "product_name": payment_record["product_name"],
                    "payment_method": payment_record["payment_method_id"],
                    "payment_id": payment_record["payment_id"]
                }
                
                await email_service.send_payment_pending(email_data)
            
            logger.info(f"Pagamento pendente processado: {payment_record['payment_id']}")
            
        except Exception as e:
            logger.error(f"Erro ao processar pagamento pendente: {e}")
    
    async def get_webhook_stats(self) -> Dict:
        """Obter estatísticas dos webhooks processados"""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$status",
                        "count": {"$sum": 1},
                        "total_amount": {"$sum": "$amount"}
                    }
                }
            ]
            
            stats = await self.payments_collection.aggregate(pipeline).to_list(10)
            
            return {
                "webhook_stats": stats,
                "last_updated": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {"error": str(e)}

# Instância global do serviço de webhook
webhook_service = WebhookService()