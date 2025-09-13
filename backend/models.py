from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

# Product Models
class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: str
    image: str
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True

class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: str
    image: str
    category: str

# Contact Models
class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "new"

class ContactMessageCreate(BaseModel):
    name: str
    email: str
    message: str

class ContactMessageResponse(BaseModel):
    id: str
    name: str
    email: str
    message: str
    created_at: datetime
    status: str

# Company Info Models
class SocialMedia(BaseModel):
    instagram: str
    facebook: str
    tiktok: str

class CompanyInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    slogan: str
    about: str
    whatsapp: str
    email: str
    social_media: SocialMedia

class CompanyInfoResponse(BaseModel):
    name: str
    slogan: str
    about: str
    whatsapp: str
    email: str
    social_media: SocialMedia