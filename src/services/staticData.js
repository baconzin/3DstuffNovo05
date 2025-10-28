// Serviço de dados estáticos para substituir as chamadas de API
import productsData from '../data/products.json';
import companyData from '../data/company.json';

class StaticDataService {
  // Produtos
  async getProducts(category = null) {
    let products = [...productsData];
    
    if (category && category !== 'Todos') {
      products = products.filter(product => product.category === category);
    }
    
    return products;
  }

  async getProduct(id) {
    const product = productsData.find(p => p.id === id);
    if (!product) {
      throw new Error('Produto não encontrado');
    }
    return product;
  }

  // Informações da empresa
  async getCompanyInfo() {
    return companyData;
  }

  // Categorias disponíveis
  getCategories() {
    const categories = [...new Set(productsData.map(product => product.category))];
    return ['Todos', ...categories];
  }

  // Produtos em destaque (primeiros 6)
  async getFeaturedProducts() {
    return productsData.slice(0, 6);
  }

  // Buscar produtos por nome
  async searchProducts(query) {
    const searchTerm = query.toLowerCase();
    return productsData.filter(product => 
      product.name.toLowerCase().includes(searchTerm) ||
      product.description.toLowerCase().includes(searchTerm)
    );
  }

  // Gerar mensagem WhatsApp para produto
  generateWhatsAppMessage(product, quantity = 1) {
    const message = `Olá! Tenho interesse no produto:

🛍️ *${product.name}*
💰 Preço: ${product.price}
📦 Quantidade: ${quantity}
🆔 Código: ${product.id}

📝 Descrição: ${product.description}

Gostaria de mais informações sobre disponibilidade e formas de pagamento.

Obrigado!`;

    return encodeURIComponent(message);
  }

  // Gerar link WhatsApp
  generateWhatsAppLink(product, quantity = 1) {
    const phone = companyData.whatsapp;
    const message = this.generateWhatsAppMessage(product, quantity);
    return `https://wa.me/${phone}?text=${message}`;
  }

  // Mensagem de contato geral
  generateContactMessage(name, email, message) {
    const contactMsg = `Olá! Meu nome é *${name}*.

📧 Email: ${email}

💬 Mensagem: ${message}

Aguardo retorno. Obrigado!`;

    return encodeURIComponent(contactMsg);
  }

  // Link de contato geral
  generateContactLink(name, email, message) {
    const phone = companyData.whatsapp;
    const contactMessage = this.generateContactMessage(name, email, message);
    return `https://wa.me/${phone}?text=${contactMessage}`;
  }
}

export default new StaticDataService();