# 🚀 Guia de Deploy - 3D Stuff

## 📋 Pré-requisitos

- Servidor Linux (Ubuntu 20.04+ recomendado)
- Node.js 18+
- Python 3.11+
- MongoDB
- Nginx
- Domínio: www.3dstuff.com.br

## 🔧 1. Configuração do Servidor

### Instalar dependências:

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Instalar MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Instalar Nginx
sudo apt install nginx -y

# Instalar PM2 para gerenciar processos
sudo npm install -g pm2
```

## 📁 2. Deploy do Backend

```bash
# Criar diretório
sudo mkdir -p /var/www/3dstuff
cd /var/www/3dstuff

# Clonar/copiar arquivos do backend
sudo cp -r /caminho/do/seu/backend ./backend
cd backend

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
sudo nano .env
# Copie o conteúdo do arquivo .env já configurado

# Testar backend
uvicorn server:app --host 0.0.0.0 --port 8001

# Configurar PM2 para backend
pm2 start "uvicorn server:app --host 0.0.0.0 --port 8001" --name "3dstuff-backend"
```

## 🖥️ 3. Deploy do Frontend

```bash
cd /var/www/3dstuff

# Copiar arquivos do frontend
sudo cp -r /caminho/do/seu/frontend ./frontend
cd frontend

# Instalar dependências
npm install

# Build para produção
npm run build

# Os arquivos estão em ./build
```

## ⚙️ 4. Configuração do Nginx

```bash
sudo nano /etc/nginx/sites-available/3dstuff.com.br
```

Conteúdo do arquivo:

```nginx
server {
    listen 80;
    server_name www.3dstuff.com.br 3dstuff.com.br;

    # Frontend (React)
    location / {
        root /var/www/3dstuff/frontend/build;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
        
        # Cache para assets estáticos
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8001/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeout para webhook
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
    }

    # Logs
    access_log /var/log/nginx/3dstuff_access.log;
    error_log /var/log/nginx/3dstuff_error.log;
}
```

Ativar site:

```bash
sudo ln -s /etc/nginx/sites-available/3dstuff.com.br /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔒 5. SSL com Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado SSL
sudo certbot --nginx -d www.3dstuff.com.br -d 3dstuff.com.br

# Renovação automática
sudo crontab -e
# Adicionar linha: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🗄️ 6. Configuração do MongoDB

```bash
# Iniciar MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Configurar banco
mongo
use fullstack_app

# Importar dados iniciais
cd /var/www/3dstuff/backend
source venv/bin/activate
python seed_data.py
python initialize_inventory.py
```

## 📨 7. Configuração do Webhook Mercado Pago

1. **Acessar painel Mercado Pago:**
   - https://www.mercadopago.com.br/developers/panel/app
   - Sua aplicação → Webhooks

2. **Configurar URL:**
   - URL: `https://www.3dstuff.com.br/api/payments/webhook`
   - Eventos: `payments` (Pagamentos)
   - Salvar

3. **Testar webhook:**
```bash
curl -X POST https://www.3dstuff.com.br/api/health
```

## 📧 8. Configuração de Email (Opcional)

Para ativar emails reais, configure SendGrid:

```bash
# No arquivo .env do backend
SENDGRID_API_KEY=sua_chave_sendgrid
SENDER_EMAIL=noreply@3dstuff.com.br
```

Ou mantenha sem configurar para apenas logs de email.

## 🚀 9. Inicialização e Monitoramento

```bash
# Inicializar todos os serviços
sudo systemctl start mongod
sudo systemctl start nginx
pm2 start 3dstuff-backend

# Verificar status
pm2 status
sudo systemctl status nginx
sudo systemctl status mongod

# Logs
pm2 logs 3dstuff-backend
sudo tail -f /var/log/nginx/3dstuff_access.log

# Configurar PM2 para iniciar com sistema
pm2 startup
pm2 save
```

## ✅ 10. Verificação Final

1. **Frontend:** https://www.3dstuff.com.br
2. **API:** https://www.3dstuff.com.br/api/health
3. **Produtos:** https://www.3dstuff.com.br/api/products
4. **Webhook:** Fazer um pagamento teste

## 🛠️ 11. Comandos Úteis

```bash
# Reiniciar backend
pm2 restart 3dstuff-backend

# Ver logs em tempo real
pm2 logs 3dstuff-backend --lines 100

# Atualizar código
cd /var/www/3dstuff/backend
git pull  # se usando git
pm2 restart 3dstuff-backend

# Verificar espaço em disco
df -h

# Monitorar processos
htop
```

## 🔧 12. Backup e Manutenção

```bash
# Backup MongoDB
mongodump --db fullstack_app --out /backup/mongodb/$(date +%Y%m%d)

# Backup arquivos
tar -czf /backup/3dstuff-$(date +%Y%m%d).tar.gz /var/www/3dstuff

# Limpeza de logs
sudo logrotate -f /etc/logrotate.conf
```

## 🚨 Solução de Problemas

### Backend não inicia:
```bash
cd /var/www/3dstuff/backend
source venv/bin/activate
python server.py  # Verificar erros
```

### Frontend não carrega:
```bash
sudo nginx -t  # Verificar configuração
sudo systemctl reload nginx
```

### MongoDB não conecta:
```bash
sudo systemctl status mongod
sudo systemctl restart mongod
```

### Webhook não funciona:
- Verificar URL no painel Mercado Pago
- Verificar logs: `pm2 logs 3dstuff-backend`
- Testar: `curl -X POST https://www.3dstuff.com.br/api/payments/webhook`

---

🎉 **Seu site estará rodando em: https://www.3dstuff.com.br**

**Suporte**: Qualquer dúvida, verificar logs com `pm2 logs` e `sudo tail -f /var/log/nginx/error.log`