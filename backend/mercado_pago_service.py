import mercadopago
import os
import logging
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from payment_models import MercadoPagoPayment

class MercadoPagoService:
    def __init__(self):
        self.access_token = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
        self.public_key = os.getenv("MERCADO_PAGO_PUBLIC_KEY")
        
        if not self.access_token:
            raise ValueError("MERCADO_PAGO_ACCESS_TOKEN não configurado")
        
        self.sdk = mercadopago.SDK(self.access_token)
        self.logger = logging.getLogger(__name__)
    
    # Definir produtos com preços fixos (SEGURANÇA)
    PRODUCTS = {
        "1": {"name": "Miniatura de Personagem", "price": 45.00, "description": "Miniaturas detalhadas de personagens famosos"},
        "2": {"name": "Suporte para Celular", "price": 25.00, "description": "Suporte ergonômico e resistente"},
        "3": {"name": "Chaveiros Personalizados", "price": 15.00, "description": "Chaveiros únicos personalizados"},
        "4": {"name": "Peças Decorativas", "price": 35.00, "description": "Objetos decorativos modernos"},
        "5": {"name": "Porta-Canetas Geométrico", "price": 30.00, "description": "Organizador de mesa com design único"},
        "6": {"name": "Luminária Personalizada", "price": 80.00, "description": "Luminária LED com design exclusivo"},
    }
    
    def get_product_info(self, product_id: str) -> Optional[Dict]:
        """Buscar informações do produto por ID"""
        return self.PRODUCTS.get(product_id)
    
    async def create_pix_payment(self, payment_data: Dict) -> Dict:
        """Criar pagamento PIX"""
        try:
            product_info = self.get_product_info(payment_data["product_id"])
            if not product_info:
                return {"success": False, "error": "Produto não encontrado"}
            
            amount = product_info["price"] * payment_data.get("quantity", 1)
            
            # Dados do pagamento PIX
            pix_data = {
                "transaction_amount": amount,
                "payment_method_id": "pix",
                "description": f"{product_info['name']} - 3D Stuff",
                "external_reference": f"3DSTUFF_{payment_data['product_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "date_of_expiration": (datetime.now() + timedelta(minutes=30)).isoformat(),
                "payer": {
                    "email": payment_data["customer_email"],
                    "first_name": payment_data["customer_name"].split()[0],
                    "last_name": " ".join(payment_data["customer_name"].split()[1:]) if len(payment_data["customer_name"].split()) > 1 else "",
                    "identification": {
                        "type": "CPF" if len(payment_data["customer_document"]) == 11 else "CNPJ",
                        "number": payment_data["customer_document"]
                    }
                }
            }
            
            # Criar pagamento
            result = self.sdk.payment().create(pix_data)
            
            if result["status"] == 201:
                payment_info = result["response"]
                
                # Extrair dados do PIX
                point_of_interaction = payment_info.get("point_of_interaction", {})
                transaction_data = point_of_interaction.get("transaction_data", {})
                
                return {
                    "success": True,
                    "payment_id": str(payment_info["id"]),
                    "status": payment_info["status"],
                    "amount": amount,
                    "qr_code": transaction_data.get("qr_code", ""),
                    "qr_code_base64": transaction_data.get("qr_code_base64", ""),
                    "ticket_url": transaction_data.get("ticket_url", ""),
                    "external_reference": pix_data["external_reference"],
                    "expires_at": payment_info["date_of_expiration"],
                    "transaction_data": payment_info
                }
            else:
                self.logger.error(f"Erro PIX: {result}")
                return {"success": False, "error": "Erro ao criar pagamento PIX"}
                
        except Exception as e:
            self.logger.error(f"Exceção PIX: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def create_credit_card_payment(self, payment_data: Dict) -> Dict:
        """Criar pagamento com cartão de crédito"""
        try:
            product_info = self.get_product_info(payment_data["product_id"])
            if not product_info:
                return {"success": False, "error": "Produto não encontrado"}
            
            amount = product_info["price"] * payment_data.get("quantity", 1)
            installments = payment_data.get("installments", 1)
            
            # Dados do pagamento com cartão
            card_data = {
                "transaction_amount": amount,
                "token": payment_data["card_token"],
                "installments": installments,
                "payment_method_id": payment_data.get("payment_method_id", "visa"),
                "issuer_id": payment_data.get("issuer_id"),
                "description": f"{product_info['name']} - 3D Stuff",
                "external_reference": f"3DSTUFF_{payment_data['product_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "payer": {
                    "email": payment_data["customer_email"],
                    "first_name": payment_data["customer_name"].split()[0],
                    "last_name": " ".join(payment_data["customer_name"].split()[1:]) if len(payment_data["customer_name"].split()) > 1 else "",
                    "identification": {
                        "type": "CPF" if len(payment_data["customer_document"]) == 11 else "CNPJ",
                        "number": payment_data["customer_document"]
                    }
                }
            }
            
            # Criar pagamento
            result = self.sdk.payment().create(card_data)
            
            if result["status"] == 201:
                payment_info = result["response"]
                
                return {
                    "success": True,
                    "payment_id": str(payment_info["id"]),
                    "status": payment_info["status"],
                    "status_detail": payment_info["status_detail"],
                    "amount": amount,
                    "installments": installments,
                    "external_reference": card_data["external_reference"],
                    "transaction_data": payment_info
                }
            else:
                self.logger.error(f"Erro cartão: {result}")
                return {"success": False, "error": "Erro ao processar cartão"}
                
        except Exception as e:
            self.logger.error(f"Exceção cartão: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def create_boleto_payment(self, payment_data: Dict) -> Dict:
        """Criar pagamento com boleto"""
        try:
            product_info = self.get_product_info(payment_data["product_id"])
            if not product_info:
                return {"success": False, "error": "Produto não encontrado"}
            
            amount = product_info["price"] * payment_data.get("quantity", 1)
            
            # Dados do boleto
            boleto_data = {
                "transaction_amount": amount,
                "payment_method_id": "bolbradesco",
                "description": f"{product_info['name']} - 3D Stuff",
                "external_reference": f"3DSTUFF_{payment_data['product_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "date_of_expiration": (datetime.now() + timedelta(days=7)).isoformat(),
                "payer": {
                    "email": payment_data["customer_email"],
                    "first_name": payment_data["customer_name"].split()[0],
                    "last_name": " ".join(payment_data["customer_name"].split()[1:]) if len(payment_data["customer_name"].split()) > 1 else "",
                    "identification": {
                        "type": "CPF" if len(payment_data["customer_document"]) == 11 else "CNPJ",
                        "number": payment_data["customer_document"]
                    }
                }
            }
            
            # Criar pagamento
            result = self.sdk.payment().create(boleto_data)
            
            if result["status"] == 201:
                payment_info = result["response"]
                
                # Extrair dados do boleto
                transaction_details = payment_info.get("transaction_details", {})
                
                return {
                    "success": True,
                    "payment_id": str(payment_info["id"]),
                    "status": payment_info["status"],
                    "amount": amount,
                    "ticket_url": transaction_details.get("external_resource_url", ""),
                    "barcode": payment_info.get("barcode", ""),
                    "external_reference": boleto_data["external_reference"],
                    "expires_at": payment_info["date_of_expiration"],
                    "transaction_data": payment_info
                }
            else:
                self.logger.error(f"Erro boleto: {result}")
                return {"success": False, "error": "Erro ao gerar boleto"}
                
        except Exception as e:
            self.logger.error(f"Exceção boleto: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def get_payment_status(self, payment_id: str) -> Dict:
        """Buscar status do pagamento"""
        try:
            result = self.sdk.payment().get(payment_id)
            
            if result["status"] == 200:
                payment_info = result["response"]
                
                return {
                    "success": True,
                    "payment_id": str(payment_info["id"]),
                    "status": payment_info["status"],
                    "status_detail": payment_info["status_detail"],
                    "payment_method": payment_info["payment_method_id"],
                    "amount": payment_info["transaction_amount"],
                    "net_amount": payment_info.get("transaction_details", {}).get("net_received_amount"),
                    "currency": payment_info["currency_id"],
                    "created_at": payment_info["date_created"],
                    "approved_at": payment_info.get("date_approved"),
                    "external_reference": payment_info.get("external_reference")
                }
            else:
                return {"success": False, "error": "Pagamento não encontrado"}
                
        except Exception as e:
            self.logger.error(f"Erro status: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def get_installment_options(self, amount: float, payment_method_id: str = "visa") -> Dict:
        """Buscar opções de parcelamento"""
        try:
            # Simular bin do cartão para buscar parcelamento
            bin_number = "411111"  # Bin genérico para teste
            
            installment_data = {
                "bin": bin_number,
                "amount": amount
            }
            
            result = self.sdk.installments().get(installment_data)
            
            if result["status"] == 200 and result["response"]:
                installments_info = result["response"][0]
                installment_options = []
                
                for option in installments_info["payer_costs"]:
                    installment_options.append({
                        "installments": option["installments"],
                        "installment_rate": option["installment_rate"],
                        "discount_rate": option["discount_rate"],
                        "installment_amount": option["installment_amount"],
                        "total_amount": option["total_amount"],
                        "recommended_message": option["recommended_message"]
                    })
                
                return {
                    "success": True,
                    "options": installment_options
                }
            else:
                # Fallback com parcelamento padrão
                return {
                    "success": True,
                    "options": [
                        {"installments": 1, "installment_amount": amount, "total_amount": amount, "recommended_message": "À vista"},
                        {"installments": 2, "installment_amount": amount/2, "total_amount": amount, "recommended_message": "2x sem juros"},
                        {"installments": 3, "installment_amount": amount/3, "total_amount": amount, "recommended_message": "3x sem juros"}
                    ]
                }
                
        except Exception as e:
            self.logger.error(f"Erro parcelamento: {str(e)}")
            # Fallback básico
            return {
                "success": True,
                "options": [
                    {"installments": 1, "installment_amount": amount, "total_amount": amount, "recommended_message": "À vista"}
                ]
            }