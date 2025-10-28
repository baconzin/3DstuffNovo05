// API estática para GitHub Pages - Sem backend necessário
import staticData from './staticData';

// Produtos
export const productsAPI = {
  getAll: async (category = null) => {
    return await staticData.getProducts(category);
  },
  
  getById: async (id) => {
    return await staticData.getProduct(id);
  }
};

// Contato - Redirecionado para WhatsApp
export const contactAPI = {
  send: async (contactData) => {
    // Redirecionar para WhatsApp ao invés de enviar para backend
    const link = staticData.generateContactLink(
      contactData.name, 
      contactData.email, 
      contactData.message
    );
    
    window.open(link, '_blank');
    return { success: true, message: 'Redirecionando para WhatsApp...' };
  },
  
  getAll: async () => {
    // Não aplicável para site estático
    return [];
  }
};

// Informações da empresa
export const companyAPI = {
  getInfo: async () => {
    return await staticData.getCompanyInfo();
  }
};

// Health check
export const healthAPI = {
  check: async () => {
    return { status: 'ok', message: 'Site estático funcionando' };
  }
};

// Utilitários para WhatsApp
export const whatsappAPI = {
  // Comprar produto
  buyProduct: (product, quantity = 1) => {
    const link = staticData.generateWhatsAppLink(product, quantity);
    window.open(link, '_blank');
  },
  
  // Contato geral
  contact: (name = '', email = '', message = '') => {
    const link = staticData.generateContactLink(name, email, message);
    window.open(link, '_blank');
  }
};

export default { productsAPI, contactAPI, companyAPI, healthAPI, whatsappAPI };