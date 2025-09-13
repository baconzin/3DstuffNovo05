import asyncio
from inventory_service import inventory_service
from database import products_collection

async def initialize_all_products_inventory():
    """Inicializar estoque para todos os produtos existentes"""
    try:
        print("🔄 Inicializando estoque para todos os produtos...")
        
        # Buscar todos os produtos
        products = await products_collection.find({"active": True}).to_list(100)
        
        for product in products:
            product_id = product["id"]
            
            # Definir estoque inicial baseado no tipo de produto
            initial_stock = 50  # Padrão para produtos impressos sob demanda
            
            # Ajustar estoque baseado na categoria
            category = product.get("category", "")
            if category == "Miniaturas":
                initial_stock = 30  # Mais complexas, menor estoque
            elif category == "Utilitários":
                initial_stock = 100  # Mais demandados
            elif category == "Decoração":
                initial_stock = 40
            elif category == "Personalizados":
                initial_stock = 20  # Feitos sob medida
            
            success = await inventory_service.initialize_product_stock(product_id, initial_stock)
            
            if success:
                print(f"✅ Estoque inicializado: {product['name']} - {initial_stock} unidades")
            else:
                print(f"❌ Erro ao inicializar: {product['name']}")
        
        print("🎉 Inicialização de estoque concluída!")
        
        # Mostrar resumo do estoque
        await show_inventory_summary()
        
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")

async def show_inventory_summary():
    """Mostrar resumo do estoque atual"""
    try:
        print("\n📊 RESUMO DO ESTOQUE:")
        print("-" * 50)
        
        products = await products_collection.find({"active": True}).to_list(100)
        
        total_products = 0
        total_stock = 0
        
        for product in products:
            stock_info = await inventory_service.get_stock_info(product["id"])
            
            if stock_info:
                available = stock_info["available_quantity"]
                reserved = stock_info["reserved_quantity"]
                status = stock_info["status"]
                
                status_emoji = {
                    "in_stock": "✅",
                    "low_stock": "⚠️",
                    "out_of_stock": "❌"
                }.get(status, "❓")
                
                print(f"{status_emoji} {product['name'][:30]:30} | Disponível: {available:3} | Reservado: {reserved:2} | Status: {status}")
                
                total_products += 1
                total_stock += available
        
        print("-" * 50)
        print(f"📦 Total de produtos: {total_products}")
        print(f"📈 Total em estoque: {total_stock} unidades")
        
        # Produtos com estoque baixo
        low_stock = await inventory_service.get_low_stock_products()
        if low_stock:
            print(f"\n⚠️  ALERTA: {len(low_stock)} produtos com estoque baixo!")
            for item in low_stock:
                print(f"   - Produto ID: {item['product_id']} | Disponível: {item['available_quantity']}")
        
    except Exception as e:
        print(f"❌ Erro ao mostrar resumo: {e}")

async def main():
    """Função principal"""
    await initialize_all_products_inventory()

if __name__ == "__main__":
    asyncio.run(main())