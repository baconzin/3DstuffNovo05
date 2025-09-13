from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from routes import router
from payment_routes import router as payment_router
from contact_routes import router as contact_router
from admin_routes import router as admin_router
from database import close_db_connection

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(
    title="3D Stuff API",
    description="API completa para o e-commerce de produtos de impressão 3D com Mercado Pago, gestão de estoque e emails automáticos",
    version="2.0.0"
)

# Include all routes
app.include_router(router)
app.include_router(payment_router)
app.include_router(contact_router)
app.include_router(admin_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db_connection()
