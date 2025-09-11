// Mock data para o site 3D Stuff

export const products = [
  {
    id: 1,
    name: "Miniatura de Personagem",
    description: "Miniaturas detalhadas de personagens famosos, impressas em alta qualidade.",
    price: "R$ 45,00",
    image: "https://via.placeholder.com/300x300/f97316/ffffff?text=Miniatura",
    category: "Miniaturas"
  },
  {
    id: 2,
    name: "Suporte para Celular",
    description: "Suporte ergonômico e resistente para seu smartphone.",
    price: "R$ 25,00",
    image: "https://via.placeholder.com/300x300/f97316/ffffff?text=Suporte",
    category: "Utilitários"
  },
  {
    id: 3,
    name: "Chaveiros Personalizados",
    description: "Chaveiros únicos com seu design ou nome personalizado.",
    price: "R$ 15,00",
    image: "https://via.placeholder.com/300x300/f97316/ffffff?text=Chaveiro",
    category: "Personalizados"
  },
  {
    id: 4,
    name: "Peças Decorativas",
    description: "Objetos decorativos modernos para sua casa ou escritório.",
    price: "R$ 35,00",
    image: "https://via.placeholder.com/300x300/f97316/ffffff?text=Decorativo",
    category: "Decoração"
  },
  {
    id: 5,
    name: "Porta-Canetas Geométrico",
    description: "Organizador de mesa com design geométrico único.",
    price: "R$ 30,00",
    image: "https://via.placeholder.com/300x300/f97316/ffffff?text=Porta-Canetas",
    category: "Utilitários"
  },
  {
    id: 6,
    name: "Luminária Personalizada",
    description: "Luminária LED com design exclusivo para ambientes modernos.",
    price: "R$ 80,00",
    image: "https://via.placeholder.com/300x300/f97316/ffffff?text=Luminária",
    category: "Decoração"
  }
];

export const companyInfo = {
  name: "3D Stuff",
  slogan: "Produtos exclusivos em impressão 3D para você.",
  about: "A 3D Stuff nasceu com a missão de transformar ideias em realidade através da impressão 3D. Trabalhamos com tecnologia de ponta e criatividade para oferecer peças únicas e personalizadas.",
  whatsapp: "5511999999999",
  email: "contato@3dstuff.com.br",
  socialMedia: {
    instagram: "@3dstuff",
    facebook: "3DStuff",
    tiktok: "@3dstuff"
  }
};

export const contactFormFields = [
  { name: "name", label: "Nome", type: "text", required: true },
  { name: "email", label: "E-mail", type: "email", required: true },
  { name: "message", label: "Mensagem", type: "textarea", required: true }
];