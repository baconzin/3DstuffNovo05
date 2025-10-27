#!/usr/bin/env node
/**
 * HELPER PARA ADICIONAR PRODUTOS - GitHub Pages
 * 
 * Como usar:
 * node add_product_helper.js
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (prompt) => {
  return new Promise((resolve) => {
    rl.question(prompt, resolve);
  });
};

const generateId = () => {
  return Math.random().toString(36).substr(2, 8);
};

const addProduct = async () => {
  console.log('\n🏪 ADICIONAR NOVO PRODUTO - 3D STUFF');
  console.log('=====================================\n');

  try {
    // Carregar produtos existentes
    const productsPath = path.join(__dirname, 'src', 'data', 'products.json');
    let products = [];
    
    if (fs.existsSync(productsPath)) {
      const data = fs.readFileSync(productsPath, 'utf8');
      products = JSON.parse(data);
    }

    // Coletar dados do produto
    const name = await question('📝 Nome do produto: ');
    if (!name.trim()) {
      console.log('❌ Nome é obrigatório');
      return;
    }

    const description = await question('📄 Descrição: ');
    if (!description.trim()) {
      console.log('❌ Descrição é obrigatória');
      return;
    }

    let price;
    while (true) {
      const priceInput = await question('💰 Preço (ex: 25.50): R$ ');
      price = parseFloat(priceInput);
      if (!isNaN(price) && price > 0) {
        break;
      }
      console.log('❌ Preço inválido. Use formato: 25.50');
    }

    console.log('\n🏷️ Categorias disponíveis:');
    console.log('1. Miniaturas');
    console.log('2. Utilitários');
    console.log('3. Decoração');
    console.log('4. Personalizados');
    
    let category;
    while (true) {
      const catChoice = await question('Escolha a categoria (1-4): ');
      const categories = {
        '1': 'Miniaturas',
        '2': 'Utilitários', 
        '3': 'Decoração',
        '4': 'Personalizados'
      };
      
      if (categories[catChoice]) {
        category = categories[catChoice];
        break;
      }
      console.log('❌ Opção inválida');
    }

    const image = await question('🖼️ URL da imagem (deixe vazio para placeholder): ');

    // Criar produto
    const newProduct = {
      id: generateId(),
      name: name.trim(),
      description: description.trim(),
      price: `R$ ${price.toFixed(2).replace('.', ',')}`,
      image: image.trim() || `https://via.placeholder.com/300x300/3b82f6/ffffff?text=${encodeURIComponent(name.substring(0, 10))}`,
      category: category,
      active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    // Adicionar à lista
    products.push(newProduct);

    // Salvar arquivo
    fs.writeFileSync(productsPath, JSON.stringify(products, null, 2), 'utf8');

    console.log('\n✅ PRODUTO ADICIONADO COM SUCESSO!');
    console.log('================================');
    console.log(`📝 Nome: ${newProduct.name}`);
    console.log(`💰 Preço: ${newProduct.price}`);
    console.log(`🏷️ Categoria: ${newProduct.category}`);
    console.log(`🆔 ID: ${newProduct.id}`);
    console.log(`🖼️ Imagem: ${newProduct.image}`);
    console.log('\n🚀 Para ver no site:');
    console.log('1. yarn build (para gerar build atualizado)');
    console.log('2. yarn deploy (para atualizar GitHub Pages)\n');

  } catch (error) {
    console.log('❌ Erro:', error.message);
  } finally {
    rl.close();
  }
};

// Verificar se está na pasta correta
if (!fs.existsSync(path.join(__dirname, 'src', 'data'))) {
  console.log('❌ Execute este script na pasta frontend do projeto');
  console.log('💡 Dica: cd frontend && node add_product_helper.js');
  process.exit(1);
}

addProduct();