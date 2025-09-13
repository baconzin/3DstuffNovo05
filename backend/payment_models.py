from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
import re

# Request Models
class PaymentRequest(BaseModel):
    product_id: str
    quantity: int = 1
    customer_email: EmailStr
    customer_document: str
    customer_name: str
    payment_method: str  # 'credit_card', 'pix', 'boleto'
    installments: Optional[int] = 1
    card_token: Optional[str] = None
    
    @validator('customer_document')
    def validate_document(cls, v):
        # Remove non-numeric characters
        document = re.sub(r'[^0-9]', '', v)
        
        # Validate CPF (11 digits) or CNPJ (14 digits)
        if len(document) == 11:
            if not cls.validate_cpf(document):
                raise ValueError('CPF inválido')
        elif len(document) == 14:
            if not cls.validate_cnpj(document):
                raise ValueError('CNPJ inválido')
        else:
            raise ValueError('Documento deve ser CPF (11 dígitos) ou CNPJ (14 dígitos)')
        
        return document
    
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Validar CPF brasileiro"""
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        # Calcular primeiro dígito verificador
        sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Calcular segundo dígito verificador
        sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        return cpf[9:11] == f"{digit1}{digit2}"
    
    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        """Validar CNPJ brasileiro"""
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        
        # Primeiro dígito verificador
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Segundo dígito verificador
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        return cnpj[12:14] == f"{digit1}{digit2}"

# Response Models
class PaymentResponse(BaseModel):
    success: bool
    payment_id: Optional[str] = None
    status: Optional[str] = None
    status_detail: Optional[str] = None
    amount: Optional[float] = None
    qr_code: Optional[str] = None
    qr_code_base64: Optional[str] = None
    ticket_url: Optional[str] = None
    barcode: Optional[str] = None
    message: str
    transaction_data: Optional[Dict[str, Any]] = None

class PaymentStatusResponse(BaseModel):
    payment_id: str
    status: str
    status_detail: str
    payment_method: str
    amount: float
    net_amount: Optional[float] = None
    currency: str
    created_at: datetime
    approved_at: Optional[datetime] = None

# Database Models
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from database import Base

class MercadoPagoPayment(Base):
    __tablename__ = "mercado_pago_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(String, unique=True, index=True)  # MP payment ID
    external_reference = Column(String, index=True)  # Our order reference
    status = Column(String, index=True)
    status_detail = Column(String)
    payment_method_id = Column(String)
    payment_type = Column(String)
    amount = Column(Float, nullable=False)
    net_amount = Column(Float)
    currency = Column(String, default="BRL")
    installments = Column(Integer, default=1)
    
    # Customer info
    customer_email = Column(String, nullable=False)
    customer_document = Column(String)
    customer_name = Column(String)
    
    # Product info
    product_id = Column(String, nullable=False)
    product_name = Column(String)
    description = Column(String)
    
    # Payment details
    payment_data = Column(JSON)  # Full MP response
    qr_code = Column(Text)
    ticket_url = Column(String)
    barcode = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_at = Column(DateTime)

class WebhookNotification(Base):
    __tablename__ = "webhook_notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(String, unique=True, index=True)
    topic = Column(String, index=True)
    resource = Column(String)
    payment_id = Column(String, index=True)
    processed = Column(Boolean, default=False)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)