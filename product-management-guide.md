# 🏪 GUIA COMPLETO - Adicionar Produtos Reais

## 🎯 MÉTODOS DISPONÍVEIS

### 1️⃣ **Script Interativo (Recomendado)**
```bash
cd /app/backend
python add_product_script.py
```
**Funcionalidades:**
- ✅ Menu amigável
- ✅ Adicionar produtos passo a passo
- ✅ Gerenciar estoque
- ✅ Listar produtos
- ✅ Remover produtos

### 2️⃣ **Script Rápido (Uma linha)**
```bash
cd /app/backend
python quick_add_product.py "Nome" "Descrição" 25.50 "Categoria" 10 "URL_imagem"
```

### 3️⃣ **Direto no Banco (Avançado)**
Editar o arquivo `/app/backend/seed_data.py`

---

## 📦 ESTRUTURA DE UM PRODUTO

```python
{
    "id": "12345678",                    # ID único (8 chars)
    "name": "Nome do Produto",           # Nome visível 
    "description": "Descrição detalhada", # Descrição completa
    "price": "R$ 25,50",                # Preço formatado
    "image": "https://...",              # URL da imagem
    "category": "Categoria",             # Ver categorias abaixo 
    "created_at": "2025-01-15...",       # Data criação
    "updated_at": "2025-01-15...",       # Data atualização
    "active": true                       # Produto ativo
}
```

---

## 🏷️ CATEGORIAS DISPONÍVEIS

1. **Miniaturas** - Figuras, personagens, colecionáveis
2. **Utilitários** - Suportes, organizadores, ferramentas
3. **Decoração** - Vasos, luminárias, objetos decorativos
4. **Personalizados** - Produtos sob medida

---

## 🖼️ COMO ADICIONAR IMAGENS DOS PRODUTOS

### **Opção 1: Imagens Online (Mais Fácil)**
```python
# Use qualquer URL de imagem
"image": "https://imgur.com/sua-imagem.jpg"
"image": "https://drive.google.com/sua-imagem.jpg"
"image": "https://seu-site.com/imagem.jpg"
```

### **Opção 2: Placeholder Automático**
```python
# Deixe vazio que gera automaticamente
"image": ""  # Gera: placeholder com nome do produto
```

### **Opção 3: Upload Local (Avançado)**
1. Coloque imagens em `/app/frontend/public/images/products/`
2. Use: `"image": "/images/products/meu-produto.jpg"`

---

## 💰 COMO DEFINIR PREÇOS

```python
# CORRETO - Sempre usar número decimal
"price": 25.50   # R$ 25,50
"price": 100.00  # R$ 100,00
"price": 15.90   # R$ 15,90

# INCORRETO - Não usar string já formatada
"price": "R$ 25,50"  # ❌ Erro
```

---

## 📊 GESTÃO DE ESTOQUE

### **Estoque Inicial:**
- Definido ao criar produto
- Padrão: 10 unidades
- Pode ser alterado depois

### **Tipos de Estoque:**
- **Disponível**: Pronto para venda
- **Reservado**: Em processo de pagamento
- **Vendido**: Já processado e enviado

### **Alertas Automáticos:**
- Estoque baixo: < 10 unidades
- Estoque zero: Produto some do site

---

## 🚀 EXEMPLOS PRÁTICOS

### **Exemplo 1: Miniatura**
```bash
python quick_add_product.py \
  "Miniatura Pikachu" \
  "Miniatura detalhada do Pikachu em PLA amarelo, 10cm de altura" \
  45.00 \
  "Miniaturas" \
  12 \
  "https://imgur.com/pikachu3d.jpg"
```

### **Exemplo 2: Utilitário**
```bash
python quick_add_product.py \
  "Suporte Notebook Ergonômico" \
  "Suporte ajustável para laptop com ventilação, melhora postura" \
  38.50 \
  "Utilitários" \
  20
```

### **Exemplo 3: Decoração**
```bash
python quick_add_product.py \
  "Luminária Lua Cheia" \
  "Luminária LED em formato de lua com 3 intensidades de luz" \
  65.00 \
  "Decoração" \
  8 \
  "https://exemplo.com/luminaria-lua.jpg"
```

---

## 🔄 FLUXO COMPLETO

### **1. Preparar Produto:**
- ✅ Escolher nome atrativo
- ✅ Escrever descrição detalhada  
- ✅ Definir preço competitivo
- ✅ Tirar/conseguir foto de qualidade
- ✅ Definir categoria correta

### **2. Adicionar no Sistema:**
```bash
cd /app/backend
python add_product_script.py
# Escolher opção 2 (Adicionar produto)
# Preencher todos os dados
```

### **3. Verificar no Site:**
- Abrir www.3dstuff.com.br
- Ir na seção Produtos
- Verificar se apareceu
- Testar filtro por categoria

### **4. Gerenciar Estoque:**
```bash
cd /app/backend
python add_product_script.py
# Escolher opção 3 (Ver/Atualizar estoque)
```

---

## 📱 DICAS DE FOTOS DOS PRODUTOS

### **Qualidade da Imagem:**
- ✅ Resolução mínima: 300x300px
- ✅ Formato: JPG ou PNG
- ✅ Fundo neutro (branco/cinza)
- ✅ Boa iluminação

### **Ângulos Importantes:**
- Vista frontal (principal)
- Vista lateral
- Detalhes especiais
- Comparação de tamanho

### **Ferramentas Gratuitas:**
- **Remove.bg** - Remover fundo
- **Canva** - Editar imagens
- **Imgur** - Hospedar imagens grátis

---

## 🛡️ SEGURANÇA E BACKUP

### **Backup dos Produtos:**
```bash
cd /app/backend
python -c "
import asyncio
from database import products_collection
async def backup():
    products = await products_collection.find().to_list(1000)
    import json
    with open('backup_produtos.json', 'w') as f:
        json.dump(products, f, indent=2, default=str)
    print('✅ Backup salvo em backup_produtos.json')
asyncio.run(backup())
"
```

### **Restaurar Backup:**
```bash
# Em caso de perda de dados
python seed_data.py  # Restaura produtos iniciais
```

---

## 🎯 PRÓXIMOS PASSOS

1. **Adicionar primeiros produtos reais**
2. **Testar sistema de pagamento**
3. **Configurar estoque real**
4. **Monitorar vendas**
5. **Adicionar mais produtos conforme demanda**

---

## 🆘 SOLUÇÃO DE PROBLEMAS

### **Produto não aparece no site:**
- Verificar se `active: true`
- Verificar categoria correta
- Limpar cache do navegador

### **Imagem não carrega:**
- Verificar URL da imagem
- Testar URL no navegador
- Usar placeholder temporário

### **Erro de preço:**
- Usar formato decimal (25.50)
- Não incluir "R$" no script
- Verificar vírgulas/pontos

### **Estoque incorreto:**
- Usar script de estoque
- Verificar logs do sistema
- Reinicializar se necessário

---

🎉 **Agora você pode adicionar quantos produtos quiser e começar a vender de verdade!**