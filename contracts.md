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
- `POST /api/products` - Criar produto (admin)
- `PUT /api/products/{id}` - Atualizar produto (admin)
- `DELETE /api/products/{id}` - Deletar produto (admin)

### 2. Contato
- `POST /api/contact` - Enviar mensagem de contato
- `GET /api/contact` - Listar mensagens (admin)

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
    },
    "contact_info": {
        "phone": str,
        "address": str
    }
}
```

## Integração Frontend/Backend

### Mudanças no Frontend
1. Remover importação de `mock.js` dos componentes
2. Substituir dados mock por chamadas à API
3. Adicionar loading states e error handling
4. Implementar toast notifications para feedback

### Endpoints a serem consumidos
- Products.jsx: `GET /api/products` e filtros
- Contact.jsx: `POST /api/contact`
- Hero.jsx e About.jsx: `GET /api/company-info`

### Estados de Loading/Error
- Produtos: loading spinner durante fetch
- Formulário: desabilitar botão durante submit
- Toast de sucesso/erro para todas operações

## Funcionalidades Extras para Implementar
- Seed inicial do banco com produtos do mock.js
- Validação de dados no backend
- Rate limiting para formulário de contato
- Logs de todas as operações