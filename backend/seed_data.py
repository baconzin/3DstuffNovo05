from datetime import datetime
import asyncio
from database import products_collection, company_info_collection
from models import Product, CompanyInfo, SocialMedia

# Dados dos produtos baseados no mock.js
PRODUCTS_DATA = [
    {
        "id": "1",
        "name": "Miniatura de Personagem",
        "description": "Miniaturas detalhadas de personagens famosos, impressas em alta qualidade.",
        "price": "R$ 45,00",
        "image": "https://via.placeholder.com/300x300/f97316/ffffff?text=Miniatura",
        "category": "Miniaturas",
        "active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "2",
        "name": "Suporte para Celular",
        "description": "Suporte ergonômico e resistente para seu smartphone.",
        "price": "R$ 25,00",
        "image": "https://via.placeholder.com/300x300/f97316/ffffff?text=Suporte",
        "category": "Utilitários",
        "active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "3",
        "name": "Chaveiros Personalizados",
        "description": "Chaveiros únicos com seu design ou nome personalizado.",
        "price": "R$ 15,00",
        "image": "https://via.placeholder.com/300x300/f97316/ffffff?text=Chaveiro",
        "category": "Personalizados",
        "active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "4",
        "name": "Peças Decorativas",
        "description": "Objetos decorativos modernos para sua casa ou escritório.",
        "price": "R$ 35,00",
        "image": "https://via.placeholder.com/300x300/f97316/ffffff?text=Decorativo",
        "category": "Decoração",
        "active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "5",
        "name": "Porta-Canetas Geométrico",
        "description": "Organizador de mesa com design geométrico único.",
        "price": "R$ 30,00",
        "image": "https://via.placeholder.com/300x300/f97316/ffffff?text=Porta-Canetas",
        "category": "Utilitários",
        "active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "6",
        "name": "Luminária Personalizada",
        "description": "Luminária LED com design exclusivo para ambientes modernos.",
        "price": "R$ 80,00",
        "image": "https://via.placeholder.com/300x300/f97316/ffffff?text=Luminária",
        "category": "Decoração",
        "active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

# Dados da empresa baseados no mock.js
COMPANY_INFO_DATA = {
    "id": "company_1",
    "name": "3D Stuff",
    "slogan": "Produtos exclusivos em impressão 3D para você.",
    "about": "A 3D Stuff nasceu com a missão de transformar ideias em realidade através da impressão 3D. Trabalhamos com tecnologia de ponta e criatividade para oferecer peças únicas e personalizadas.",
    "whatsapp": "5511999999999",
    "email": "contato@3dstuff.com.br",
    "social_media": {
        "instagram": "@3dstuff",
        "facebook": "3DStuff",
        "tiktok": "@3dstuff"
    }
}

async def seed_database():
    """Popula o banco de dados com dados iniciais"""
    try:
        # Limpa coleções existentes
        await products_collection.delete_many({})
        await company_info_collection.delete_many({})
        
        # Insere produtos
        await products_collection.insert_many(PRODUCTS_DATA)
        print(f"✅ {len(PRODUCTS_DATA)} produtos inseridos com sucesso!")
        
        # Insere informações da empresa
        await company_info_collection.insert_one(COMPANY_INFO_DATA)
        print("✅ Informações da empresa inseridas com sucesso!")
        
        print("🎉 Seed do banco de dados concluído!")
        
    except Exception as e:
        print(f"❌ Erro ao fazer seed do banco: {e}")

if __name__ == "__main__":
    asyncio.run(seed_database())