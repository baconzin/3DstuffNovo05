#!/usr/bin/env python3
"""
SCRIPT RÁPIDO - Adicionar produto em uma linha
Uso: python quick_add_product.py "Nome" "Descrição" 25.50 "Categoria" 10 "URL_imagem"
"""

import asyncio
import sys
from database import products_collection
from inventory_service import inventory_service
from datetime import datetime
import uuid

async def quick_add_product(name, description, price, category, stock=10, image_url=""):
    """Adicionar produto rapidamente"""
    try:
        # Gerar ID
        product_id = str(uuid.uuid4())[:8]
        
        # Validar categoria
        valid_categories = ["Miniaturas", "Utilitários", "Decoração", "Personalizados"]
        if category not in valid_categories:
            print(f"❌ Categoria deve ser uma de: {', '.join(valid_categories)}")
            return False
        
        # Estruturar produto
        product = {
            "id": product_id,
            "name": name,
            "description": description,
            "price": f"R$ {float(price):.2f}".replace('.', ','),
            "image": image_url or f"https://via.placeholder.com/300x300/3b82f6/ffffff?text={name.replace(' ', '+')[:10]}",
            "category": category,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "active": True
        }
        
        # Inserir no banco
        result = await products_collection.insert_one(product)
        
        if result.inserted_id:
            # Inicializar estoque
            await inventory_service.initialize_product_stock(product_id, int(stock))
            
            print(f"✅ PRODUTO ADICIONADO:")
            print(f"   ID: {product_id}")
            print(f"   Nome: {name}")
            print(f"   Preço: R$ {float(price):.2f}")
            print(f"   Categoria: {category}")
            print(f"   Estoque: {stock} unidades")
            return True
        else:
            print("❌ Erro ao salvar produto")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("📝 USO:")
        print('python quick_add_product.py "Nome" "Descrição" preço "Categoria" [estoque] [url_imagem]')
        print("\n📚 EXEMPLO:")
        print('python quick_add_product.py "Caneca Personalizada" "Caneca de cerâmica com impressão 3D" 28.50 "Personalizados" 8')
        print("\n🏷️ CATEGORIAS VÁLIDAS:")
        print("- Miniaturas")
        print("- Utilitários") 
        print("- Decoração")
        print("- Personalizados")
        sys.exit(1)
    
    name = sys.argv[1]
    description = sys.argv[2]
    price = sys.argv[3]
    category = sys.argv[4]
    stock = int(sys.argv[5]) if len(sys.argv) > 5 else 10
    image_url = sys.argv[6] if len(sys.argv) > 6 else ""
    
    asyncio.run(quick_add_product(name, description, price, category, stock, image_url))