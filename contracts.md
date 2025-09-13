# 3D Stuff - Contratos de API

## Dados Mockados no Frontend (mock.js)

### Produtos
- 6 produtos com: id, name, description, price, image, category
- Categorias: Miniaturas, Utilitários, Personalizados, Decoração

### Informações da Empresa
- Nome, slogan, sobre, whatsapp, email, redes sociais

### Formulário de Contato
- Campos: name, email, message

## APIs a serem implementadas no Backend

### 1. Produtos
- `GET /api/products` - Listar todos os produtos
- `GET /api/products?category={categoria}` - Filtrar por categoria
- `GET /api/products/{id}` - Buscar produto específico

### 2. Contato
- `POST /api/contact` - Enviar mensagem de contato

### 3. Informações da Empresa
- `GET /api/company-info` - Buscar informações da empresa

## Modelos MongoDB

### Product
```python
{
    "_id": ObjectId,
    "name": str,
    "description": str,
    "price": str,
    "image": str,
    "category": str,
    "created_at": datetime,
    "updated_at": datetime,
    "active": bool
}
```

### ContactMessage
```python
{
    "_id": ObjectId,
    "name": str,
    "email": str,
    "message": str,
    "created_at": datetime,
    "status": str  # "new", "read", "replied"
}
```

### CompanyInfo
```python
{
    "_id": ObjectId,
    "name": str,
    "slogan": str,
    "about": str,
    "whatsapp": str,
    "email": str,
    "social_media": {
        "instagram": str,
        "facebook": str,
        "tiktok": str
    }
}
```

## Integração Frontend/Backend

### Mudanças no Frontend
1. Remover importação de `mock.js` dos componentes
2. Substituir dados mock por chamadas à API
3. Adicionar loading states e error handling

### Endpoints a serem consumidos
- Products.jsx: `GET /api/products` e filtros
- Contact.jsx: `POST /api/contact`
- Hero.jsx e About.jsx: `GET /api/company-info`