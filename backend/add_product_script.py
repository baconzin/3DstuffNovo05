#!/usr/bin/env python3
"""
Script para adicionar produtos reais à 3D Stuff
Uso: python add_product_script.py
"""

import asyncio
from database import products_collection, db
from inventory_service import inventory_service
from datetime import datetime
import uuid

class ProductManager:
    def __init__(self):
        self.products_collection = products_collection

    async def add_product(self, product_data):
        """Adicionar um novo produto"""
        try:
            # Validar dados obrigatórios
            required_fields = ['name', 'description', 'price', 'category']
            for field in required_fields:
                if not product_data.get(field):
                    print(f"❌ Erro: Campo '{field}' é obrigatório")
                    return False

            # Gerar ID único
            product_id = str(uuid.uuid4())[:8]  # ID mais curto para facilitar
            
            # Estruturar produto
            new_product = {
                "id": product_id,
                "name": product_data["name"],
                "description": product_data["description"],
                "price": f"R$ {float(product_data['price']):.2f}".replace('.', ','),
                "image": product_data.get("image", "https://via.placeholder.com/300x300/3b82f6/ffffff?text=3D+Produto"),
                "category": product_data["category"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "active": True
            }

            # Inserir no banco
            result = await self.products_collection.insert_one(new_product)
            
            if result.inserted_id:
                # Inicializar estoque
                stock_quantity = product_data.get("stock", 10)
                await inventory_service.initialize_product_stock(product_id, stock_quantity)
                
                print(f"✅ Produto '{product_data['name']}' adicionado com sucesso!")
                print(f"   ID: {product_id}")
                print(f"   Preço: R$ {float(product_data['price']):.2f}")
                print(f"   Estoque inicial: {stock_quantity} unidades")
                return True
            else:
                print("❌ Erro ao salvar produto no banco")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    async def list_products(self):
        """Listar todos os produtos"""
        try:
            products = await self.products_collection.find({"active": True}).to_list(100)
            
            if not products:
                print("📦 Nenhum produto encontrado")
                return
                
            print("\n📦 PRODUTOS CADASTRADOS:")
            print("-" * 80)
            
            for product in products:
                # Buscar info do estoque
                stock_info = await inventory_service.get_stock_info(product["id"])
                stock_qty = stock_info["available_quantity"] if stock_info else "N/A"
                
                print(f"🆔 ID: {product['id']}")
                print(f"📝 Nome: {product['name']}")
                print(f"🏷️  Categoria: {product['category']}")
                print(f"💰 Preço: {product['price']}")
                print(f"📦 Estoque: {stock_qty} unidades")
                print(f"🔗 Imagem: {product['image'][:50]}...")
                print("-" * 80)
                
        except Exception as e:
            print(f"❌ Erro ao listar produtos: {e}")

    async def update_product_stock(self, product_id, new_quantity, operation="set"):
        """Atualizar estoque de um produto"""
        try:
            if operation == "set":
                # Definir estoque absoluto
                stock_info = await inventory_service.get_stock_info(product_id)
                if stock_info:
                    current = stock_info["available_quantity"]
                    difference = new_quantity - current
                    
                    if difference > 0:
                        result = await inventory_service.add_stock(product_id, difference, f"Ajuste de estoque para {new_quantity}")
                    elif difference < 0:
                        # Remover estoque (simular venda)
                        result = {"success": True, "message": f"Estoque ajustado para {new_quantity}"}
                        await self.products_collection.update_one(
                            {"id": product_id},
                            {"$set": {"updated_at": datetime.utcnow()}}
                        )
                else:
                    await inventory_service.initialize_product_stock(product_id, new_quantity)
                    result = {"success": True, "message": f"Estoque inicializado com {new_quantity}"}
                    
            elif operation == "add":
                # Adicionar ao estoque atual
                result = await inventory_service.add_stock(product_id, new_quantity, f"Reposição de {new_quantity} unidades")
            
            if result.get("success"):
                print(f"✅ {result['message']}")
                return True
            else:
                print(f"❌ Erro: {result.get('message', 'Erro desconhecido')}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao atualizar estoque: {e}")
            return False

    async def remove_product(self, product_id):
        """Remover produto (marcar como inativo)"""
        try:
            result = await self.products_collection.update_one(
                {"id": product_id},
                {"$set": {"active": False, "updated_at": datetime.utcnow()}}
            )
            
            if result.modified_count > 0:
                print(f"✅ Produto {product_id} removido com sucesso")
                return True
            else:
                print(f"❌ Produto {product_id} não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao remover produto: {e}")
            return False

async def interactive_menu():
    """Menu interativo para gerenciar produtos"""
    manager = ProductManager()
    
    while True:
        print("\n" + "="*60)
        print("🏪 GERENCIADOR DE PRODUTOS - 3D STUFF")
        print("="*60)
        print("1. 📦 Listar produtos")
        print("2. ➕ Adicionar produto")
        print("3. 📊 Ver/Atualizar estoque")
        print("4. 🗑️  Remover produto")
        print("5. 🚪 Sair")
        print("-"*60)
        
        choice = input("Escolha uma opção (1-5): ").strip()
        
        if choice == "1":
            await manager.list_products()
            
        elif choice == "2":
            print("\n➕ ADICIONAR NOVO PRODUTO")
            print("-"*40)
            
            name = input("📝 Nome do produto: ").strip()
            if not name:
                print("❌ Nome é obrigatório")
                continue
                
            description = input("📄 Descrição: ").strip()
            if not description:
                print("❌ Descrição é obrigatória")
                continue
                
            try:
                price = float(input("💰 Preço (apenas números, ex: 25.50): ").strip())
            except ValueError:
                print("❌ Preço inválido")
                continue
                
            print("\n🏷️ Categorias disponíveis:")
            print("1. Miniaturas")
            print("2. Utilitários") 
            print("3. Decoração")
            print("4. Personalizados")
            
            cat_choice = input("Escolha a categoria (1-4): ").strip()
            categories = {"1": "Miniaturas", "2": "Utilitários", "3": "Decoração", "4": "Personalizados"}
            category = categories.get(cat_choice)
            
            if not category:
                print("❌ Categoria inválida")
                continue
                
            image_url = input("🖼️ URL da imagem (deixe vazio para usar placeholder): ").strip()
            
            try:
                stock = int(input("📦 Quantidade inicial em estoque (padrão 10): ").strip() or "10")
            except ValueError:
                stock = 10
                
            product_data = {
                "name": name,
                "description": description,
                "price": price,
                "category": category,
                "image": image_url if image_url else None,
                "stock": stock
            }
            
            await manager.add_product(product_data)
            
        elif choice == "3":
            await manager.list_products()
            product_id = input("\n🆔 Digite o ID do produto para gerenciar estoque: ").strip()
            
            if not product_id:
                continue
                
            print("\n📊 OPÇÕES DE ESTOQUE:")
            print("1. Ver estoque atual")
            print("2. Definir quantidade exata")
            print("3. Adicionar ao estoque atual")
            
            stock_choice = input("Escolha (1-3): ").strip()
            
            if stock_choice == "1":
                stock_info = await inventory_service.get_stock_info(product_id)
                if stock_info:
                    print(f"\n📦 Estoque do produto {product_id}:")
                    print(f"   Disponível: {stock_info['available_quantity']}")
                    print(f"   Reservado: {stock_info['reserved_quantity']}")
                    print(f"   Vendido: {stock_info['sold_quantity']}")
                    print(f"   Status: {stock_info['status']}")
                else:
                    print("❌ Produto não encontrado no estoque")
                    
            elif stock_choice in ["2", "3"]:
                try:
                    qty = int(input("📦 Quantidade: ").strip())
                    operation = "set" if stock_choice == "2" else "add"
                    await manager.update_product_stock(product_id, qty, operation)
                except ValueError:
                    print("❌ Quantidade inválida")
                    
        elif choice == "4":
            await manager.list_products()
            product_id = input("\n🆔 Digite o ID do produto para remover: ").strip()
            
            if product_id:
                confirm = input(f"⚠️ Tem certeza que deseja remover o produto {product_id}? (s/N): ").strip().lower()
                if confirm == 's':
                    await manager.remove_product(product_id)
                    
        elif choice == "5":
            print("👋 Até logo!")
            break
            
        else:
            print("❌ Opção inválida")
            
        input("\nPressione Enter para continuar...")

# Função para adicionar produtos de exemplo
async def add_sample_products():
    """Adicionar alguns produtos de exemplo"""
    manager = ProductManager()
    
    sample_products = [
        {
            "name": "Miniatura Dragon Ball - Goku",
            "description": "Miniatura detalhada do Goku em posição de luta, impressa em PLA de alta qualidade.",
            "price": 45.00,
            "category": "Miniaturas",
            "stock": 15,
            "image": "https://via.placeholder.com/300x300/3b82f6/ffffff?text=Goku+3D"
        },
        {
            "name": "Suporte Celular Ajustável",
            "description": "Suporte ergonômico para celular com ângulo ajustável, ideal para mesa de trabalho.",
            "price": 22.00,
            "category": "Utilitários", 
            "stock": 25,
            "image": "https://via.placeholder.com/300x300/3b82f6/ffffff?text=Suporte"
        },
        {
            "name": "Vaso Decorativo Geométrico",
            "description": "Vaso moderno com design geométrico, perfeito para plantas pequenas.",
            "price": 35.00,
            "category": "Decoração",
            "stock": 12,
            "image": "https://via.placeholder.com/300x300/3b82f6/ffffff?text=Vaso"
        }
    ]
    
    print("🌱 Adicionando produtos de exemplo...")
    for product in sample_products:
        await manager.add_product(product)

if __name__ == "__main__":
    print("🏪 GERENCIADOR DE PRODUTOS - 3D STUFF")
    print("Escolha uma opção:")
    print("1. Menu interativo")
    print("2. Adicionar produtos de exemplo")
    
    choice = input("Opção (1-2): ").strip()
    
    if choice == "1":
        asyncio.run(interactive_menu())
    elif choice == "2":
        asyncio.run(add_sample_products())
    else:
        print("❌ Opção inválida")