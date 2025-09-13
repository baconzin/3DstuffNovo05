from typing import Dict, Optional
from database import db
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class StockStatus(Enum):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    RESERVED = "reserved"

class InventoryService:
    def __init__(self):
        self.collection = db.inventory
        
    async def initialize_product_stock(self, product_id: str, initial_stock: int = 50) -> bool:
        """Inicializar estoque de um produto"""
        try:
            stock_data = {
                "product_id": product_id,
                "available_quantity": initial_stock,
                "reserved_quantity": 0,
                "sold_quantity": 0,
                "reorder_level": 10,  # Nível mínimo para alerta
                "status": StockStatus.IN_STOCK.value,
                "last_updated": datetime.utcnow(),
                "created_at": datetime.utcnow(),
                "stock_movements": []
            }
            
            # Verificar se já existe
            existing = await self.collection.find_one({"product_id": product_id})
            if existing:
                logger.info(f"Estoque já existe para produto {product_id}")
                return True
            
            await self.collection.insert_one(stock_data)
            logger.info(f"Estoque inicializado para produto {product_id}: {initial_stock} unidades")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar estoque: {e}")
            return False
    
    async def check_availability(self, product_id: str, quantity: int = 1) -> Dict:
        """Verificar disponibilidade de produto"""
        try:
            stock = await self.collection.find_one({"product_id": product_id})
            
            if not stock:
                # Inicializar estoque se não existir
                await self.initialize_product_stock(product_id)
                stock = await self.collection.find_one({"product_id": product_id})
            
            available = stock["available_quantity"]
            status = self._calculate_stock_status(available, stock["reorder_level"])
            
            return {
                "available": available >= quantity,
                "available_quantity": available,
                "requested_quantity": quantity,
                "status": status.value,
                "can_fulfill": available >= quantity
            }
            
        except Exception as e:
            logger.error(f"Erro ao verificar disponibilidade: {e}")
            return {
                "available": False,
                "available_quantity": 0,
                "requested_quantity": quantity,
                "status": StockStatus.OUT_OF_STOCK.value,
                "can_fulfill": False,
                "error": str(e)
            }
    
    async def reserve_stock(self, product_id: str, quantity: int, order_id: str) -> Dict:
        """Reservar estoque para um pedido"""
        try:
            # Verificar disponibilidade primeiro
            availability = await self.check_availability(product_id, quantity)
            
            if not availability["can_fulfill"]:
                return {
                    "success": False,
                    "message": "Estoque insuficiente",
                    "available_quantity": availability["available_quantity"]
                }
            
            # Reservar estoque
            movement = {
                "type": "reservation",
                "quantity": quantity,
                "order_id": order_id,
                "timestamp": datetime.utcnow(),
                "notes": f"Reserva para pedido {order_id}"
            }
            
            result = await self.collection.update_one(
                {"product_id": product_id},
                {
                    "$inc": {
                        "available_quantity": -quantity,
                        "reserved_quantity": quantity
                    },
                    "$push": {"stock_movements": movement},
                    "$set": {"last_updated": datetime.utcnow()}
                }
            )
            
            if result.modified_count > 0:
                # Atualizar status após reserva
                await self._update_stock_status(product_id)
                
                logger.info(f"Estoque reservado: {quantity} unidades do produto {product_id} para pedido {order_id}")
                return {
                    "success": True,
                    "message": "Estoque reservado com sucesso",
                    "reserved_quantity": quantity
                }
            else:
                return {
                    "success": False,
                    "message": "Erro ao reservar estoque"
                }
                
        except Exception as e:
            logger.error(f"Erro ao reservar estoque: {e}")
            return {
                "success": False,
                "message": f"Erro interno: {str(e)}"
            }
    
    async def confirm_sale(self, product_id: str, quantity: int, order_id: str) -> Dict:
        """Confirmar venda e atualizar estoque"""
        try:
            movement = {
                "type": "sale",
                "quantity": quantity,
                "order_id": order_id,
                "timestamp": datetime.utcnow(),
                "notes": f"Venda confirmada para pedido {order_id}"
            }
            
            result = await self.collection.update_one(
                {"product_id": product_id},
                {
                    "$inc": {
                        "reserved_quantity": -quantity,
                        "sold_quantity": quantity
                    },
                    "$push": {"stock_movements": movement},
                    "$set": {"last_updated": datetime.utcnow()}
                }
            )
            
            if result.modified_count > 0:
                await self._update_stock_status(product_id)
                
                logger.info(f"Venda confirmada: {quantity} unidades do produto {product_id} - pedido {order_id}")
                return {
                    "success": True,
                    "message": "Venda confirmada e estoque atualizado"
                }
            else:
                return {
                    "success": False,
                    "message": "Erro ao confirmar venda"
                }
                
        except Exception as e:
            logger.error(f"Erro ao confirmar venda: {e}")
            return {"success": False, "message": str(e)}
    
    async def cancel_reservation(self, product_id: str, quantity: int, order_id: str) -> Dict:
        """Cancelar reserva de estoque"""
        try:
            movement = {
                "type": "cancellation",
                "quantity": quantity,
                "order_id": order_id,
                "timestamp": datetime.utcnow(),
                "notes": f"Cancelamento de reserva para pedido {order_id}"
            }
            
            result = await self.collection.update_one(
                {"product_id": product_id},
                {
                    "$inc": {
                        "available_quantity": quantity,
                        "reserved_quantity": -quantity
                    },
                    "$push": {"stock_movements": movement},
                    "$set": {"last_updated": datetime.utcnow()}
                }
            )
            
            if result.modified_count > 0:
                await self._update_stock_status(product_id)
                
                logger.info(f"Reserva cancelada: {quantity} unidades do produto {product_id} - pedido {order_id}")
                return {
                    "success": True,
                    "message": "Reserva cancelada com sucesso"
                }
            else:
                return {
                    "success": False,
                    "message": "Erro ao cancelar reserva"
                }
                
        except Exception as e:
            logger.error(f"Erro ao cancelar reserva: {e}")
            return {"success": False, "message": str(e)}
    
    async def add_stock(self, product_id: str, quantity: int, notes: str = "Reposição de estoque") -> Dict:
        """Adicionar estoque (reposição)"""
        try:
            movement = {
                "type": "restock",
                "quantity": quantity,
                "timestamp": datetime.utcnow(),
                "notes": notes
            }
            
            result = await self.collection.update_one(
                {"product_id": product_id},
                {
                    "$inc": {"available_quantity": quantity},
                    "$push": {"stock_movements": movement},
                    "$set": {"last_updated": datetime.utcnow()}
                }
            )
            
            if result.modified_count > 0:
                await self._update_stock_status(product_id)
                
                logger.info(f"Estoque adicionado: {quantity} unidades do produto {product_id}")
                return {
                    "success": True,
                    "message": f"Adicionadas {quantity} unidades ao estoque"
                }
            else:
                return {
                    "success": False,
                    "message": "Erro ao adicionar estoque"
                }
                
        except Exception as e:
            logger.error(f"Erro ao adicionar estoque: {e}")
            return {"success": False, "message": str(e)}
    
    async def get_stock_info(self, product_id: str) -> Optional[Dict]:
        """Obter informações completas do estoque"""
        try:
            stock = await self.collection.find_one({"product_id": product_id})
            
            if not stock:
                # Inicializar se não existir
                await self.initialize_product_stock(product_id)
                stock = await self.collection.find_one({"product_id": product_id})
            
            return {
                "product_id": stock["product_id"],
                "available_quantity": stock["available_quantity"],
                "reserved_quantity": stock["reserved_quantity"],
                "sold_quantity": stock["sold_quantity"],
                "total_quantity": stock["available_quantity"] + stock["reserved_quantity"],
                "status": stock["status"],
                "reorder_level": stock["reorder_level"],
                "needs_restock": stock["available_quantity"] <= stock["reorder_level"],
                "last_updated": stock["last_updated"],
                "recent_movements": stock["stock_movements"][-5:] if stock["stock_movements"] else []
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter informações do estoque: {e}")
            return None
    
    async def get_low_stock_products(self) -> list:
        """Obter produtos com estoque baixo"""
        try:
            pipeline = [
                {
                    "$match": {
                        "$expr": {
                            "$lte": ["$available_quantity", "$reorder_level"]
                        }
                    }
                },
                {
                    "$project": {
                        "product_id": 1,
                        "available_quantity": 1,
                        "reorder_level": 1,
                        "status": 1
                    }
                }
            ]
            
            low_stock = await self.collection.aggregate(pipeline).to_list(100)
            return low_stock
            
        except Exception as e:
            logger.error(f"Erro ao buscar produtos com estoque baixo: {e}")
            return []
    
    async def _update_stock_status(self, product_id: str):
        """Atualizar status do estoque"""
        try:
            stock = await self.collection.find_one({"product_id": product_id})
            if not stock:
                return
            
            available = stock["available_quantity"]
            reorder_level = stock["reorder_level"]
            
            status = self._calculate_stock_status(available, reorder_level)
            
            await self.collection.update_one(
                {"product_id": product_id},
                {"$set": {"status": status.value}}
            )
            
        except Exception as e:
            logger.error(f"Erro ao atualizar status do estoque: {e}")
    
    def _calculate_stock_status(self, available: int, reorder_level: int) -> StockStatus:
        """Calcular status do estoque baseado na quantidade disponível"""
        if available <= 0:
            return StockStatus.OUT_OF_STOCK
        elif available <= reorder_level:
            return StockStatus.LOW_STOCK
        else:
            return StockStatus.IN_STOCK

# Instância global do serviço de inventário
inventory_service = InventoryService()