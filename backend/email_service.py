from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Para desenvolvimento, vou usar um serviço de email gratuito
        # Em produção, você pode configurar SendGrid real
        self.sendgrid_key = os.getenv("SENDGRID_API_KEY")
        self.sender_email = os.getenv("SENDER_EMAIL", "noreply@3dstuff.com.br")
        
        if self.sendgrid_key:
            self.sg = SendGridAPIClient(self.sendgrid_key)
        else:
            logger.warning("SendGrid não configurado. Emails serão logados apenas.")
    
    async def send_payment_confirmation(self, payment_data: Dict) -> bool:
        """Enviar email de confirmação de pagamento"""
        try:
            customer_email = payment_data["customer_email"]
            customer_name = payment_data["customer_name"]
            product_name = payment_data["product_name"]
            amount = payment_data["amount"]
            payment_method = payment_data["payment_method"]
            payment_id = payment_data["payment_id"]
            
            subject = f"✅ Pedido confirmado - {product_name} - 3D Stuff"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Pedido Confirmado - 3D Stuff</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #f97316, #fb923c); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .product-info {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f97316; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                    .button {{ background: #f97316; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 15px 0; }}
                    .success-icon {{ font-size: 60px; color: #22c55e; text-align: center; margin-bottom: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Pedido Confirmado!</h1>
                        <p>Seu pagamento foi aprovado com sucesso</p>
                    </div>
                    
                    <div class="content">
                        <div class="success-icon">✅</div>
                        
                        <p><strong>Olá, {customer_name}!</strong></p>
                        
                        <p>Ficamos felizes em confirmar que seu pedido foi aprovado e já está sendo processado!</p>
                        
                        <div class="product-info">
                            <h3>📦 Detalhes do Produto</h3>
                            <p><strong>Produto:</strong> {product_name}</p>
                            <p><strong>Valor:</strong> R$ {amount:.2f}</p>
                            <p><strong>Forma de pagamento:</strong> {self._format_payment_method(payment_method)}</p>
                            <p><strong>ID do Pagamento:</strong> {payment_id}</p>
                            <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
                        </div>
                        
                        <h3>📋 Próximos passos:</h3>
                        <ul>
                            <li>✅ Pagamento confirmado</li>
                            <li>🏭 Produto entrará em produção em até 24h</li>
                            <li>📱 Você receberá atualizações por WhatsApp</li>
                            <li>🚚 Entrega estimada: 5-7 dias úteis</li>
                        </ul>
                        
                        <p>Tem alguma dúvida? Entre em contato conosco:</p>
                        <p>📧 Email: contato@3dstuff.com.br</p>
                        <p>📱 WhatsApp: (19) 97163-6969</p>
                        
                        <a href="https://wa.me/5519971636969?text=Olá! Tenho uma dúvida sobre meu pedido {payment_id}" class="button">
                            💬 Falar no WhatsApp
                        </a>
                    </div>
                    
                    <div class="footer">
                        <p>Este email foi enviado automaticamente pela <strong>3D Stuff</strong></p>
                        <p>Transformamos ideias em realidade através da impressão 3D ✨</p>
                        <p><em>www.3dstuff.com.br</em></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return await self._send_email(customer_email, subject, html_content)
            
        except Exception as e:
            logger.error(f"Erro ao enviar email de confirmação: {e}")
            return False
    
    async def send_payment_pending(self, payment_data: Dict) -> bool:
        """Enviar email de pagamento pendente"""
        try:
            customer_email = payment_data["customer_email"]
            customer_name = payment_data["customer_name"]
            product_name = payment_data["product_name"]
            payment_method = payment_data["payment_method"]
            payment_id = payment_data["payment_id"]
            
            subject = f"⏳ Aguardando pagamento - {product_name} - 3D Stuff"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Aguardando Pagamento - 3D Stuff</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #f59e0b, #fbbf24); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .payment-info {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f59e0b; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                    .pending-icon {{ font-size: 60px; color: #f59e0b; text-align: center; margin-bottom: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>⏳ Aguardando Pagamento</h1>
                        <p>Seu pedido foi recebido</p>
                    </div>
                    
                    <div class="content">
                        <div class="pending-icon">⏳</div>
                        
                        <p><strong>Olá, {customer_name}!</strong></p>
                        
                        <p>Recebemos seu pedido e estamos aguardando a confirmação do pagamento.</p>
                        
                        <div class="payment-info">
                            <h3>📋 Detalhes do Pedido</h3>
                            <p><strong>Produto:</strong> {product_name}</p>
                            <p><strong>Forma de pagamento:</strong> {self._format_payment_method(payment_method)}</p>
                            <p><strong>ID do Pedido:</strong> {payment_id}</p>
                        </div>
                        
                        {self._get_payment_instructions(payment_method)}
                        
                        <p>Assim que recebermos a confirmação do pagamento, você receberá um novo email e começaremos a produção do seu produto!</p>
                        
                        <p>Dúvidas? Entre em contato:</p>
                        <p>📧 Email: contato@3dstuff.com.br</p>
                        <p>📱 WhatsApp: (19) 97163-6969</p>
                    </div>
                    
                    <div class="footer">
                        <p>Este email foi enviado automaticamente pela <strong>3D Stuff</strong></p>
                        <p>Transformamos ideias em realidade através da impressão 3D ✨</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return await self._send_email(customer_email, subject, html_content)
            
        except Exception as e:
            logger.error(f"Erro ao enviar email de pagamento pendente: {e}")
            return False
    
    async def send_contact_confirmation(self, contact_data: Dict) -> bool:
        """Enviar confirmação de recebimento do contato"""
        try:
            customer_email = contact_data["email"]
            customer_name = contact_data["name"]
            message = contact_data["message"]
            
            subject = "✅ Mensagem recebida - 3D Stuff"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Mensagem Recebida - 3D Stuff</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #f97316, #fb923c); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .message-box {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f97316; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📩 Mensagem Recebida!</h1>
                        <p>Obrigado por entrar em contato</p>
                    </div>
                    
                    <div class="content">
                        <p><strong>Olá, {customer_name}!</strong></p>
                        
                        <p>Recebemos sua mensagem e nossa equipe retornará o contato em até 24 horas.</p>
                        
                        <div class="message-box">
                            <h3>📝 Sua mensagem:</h3>
                            <p><em>"{message}"</em></p>
                        </div>
                        
                        <p>Se sua dúvida for urgente, entre em contato pelo WhatsApp:</p>
                        <p>📱 (19) 97163-6969</p>
                        
                        <p>Atenciosamente,<br><strong>Equipe 3D Stuff</strong></p>
                    </div>
                    
                    <div class="footer">
                        <p>Este email foi enviado automaticamente pela <strong>3D Stuff</strong></p>
                        <p>Transformamos ideias em realidade através da impressão 3D ✨</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return await self._send_email(customer_email, subject, html_content)
            
        except Exception as e:
            logger.error(f"Erro ao enviar email de confirmação de contato: {e}")
            return False
    
    async def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Método interno para enviar email"""
        try:
            if self.sendgrid_key:
                # Envio real via SendGrid
                message = Mail(
                    from_email=Email(self.sender_email, "3D Stuff"),
                    to_emails=To(to_email),
                    subject=subject,
                    html_content=Content("text/html", html_content)
                )
                
                response = self.sg.send(message)
                logger.info(f"Email enviado para {to_email}: Status {response.status_code}")
                return response.status_code == 202
            else:
                # Para desenvolvimento - apenas log
                logger.info(f"[EMAIL SIMULADO] Para: {to_email}")
                logger.info(f"[EMAIL SIMULADO] Assunto: {subject}")
                logger.info(f"[EMAIL SIMULADO] Conteúdo enviado com sucesso!")
                return True
                
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")
            return False
    
    def _format_payment_method(self, method: str) -> str:
        """Formatar método de pagamento para exibição"""
        methods = {
            "pix": "PIX",
            "credit_card": "Cartão de Crédito",
            "boleto": "Boleto Bancário"
        }
        return methods.get(method, method)
    
    def _get_payment_instructions(self, payment_method: str) -> str:
        """Obter instruções específicas por método de pagamento"""
        if payment_method == "pix":
            return """
            <div style="background: #e0f2fe; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4>💰 Instruções para PIX:</h4>
                <p>• O PIX tem validade de 30 minutos</p>
                <p>• Após o pagamento, a confirmação é automática</p>
                <p>• Você receberá um email assim que for confirmado</p>
            </div>
            """
        elif payment_method == "boleto":
            return """
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4>🧾 Instruções para Boleto:</h4>
                <p>• O boleto tem vencimento em 7 dias úteis</p>
                <p>• Pode ser pago em qualquer banco ou lotérica</p>
                <p>• A confirmação pode levar até 2 dias úteis</p>
            </div>
            """
        else:
            return """
            <div style="background: #fff3e0; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4>💳 Cartão de Crédito:</h4>
                <p>• A confirmação é processada automaticamente</p>
                <p>• Em caso de aprovação, você receberá confirmação imediata</p>
            </div>
            """

# Instância global do serviço de email
email_service = EmailService()