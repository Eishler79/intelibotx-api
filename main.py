from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import dashboard
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
import os

# ================================
# Cargar variables de entorno
# ================================
load_dotenv()
print("🔐 API Key:", os.getenv("BINANCE_TESTNET_API_KEY"))
print("🔐 API Secret:", os.getenv("BINANCE_TESTNET_API_SECRET"))

# ================================
# Crear instancia FastAPI
# ================================
app = FastAPI(
    title="InteliBotX API",
    version="0.1.0",
)

# ================================
# Middleware CORS reforzado
# ================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://intelibotx-ui.vercel.app",
    ],
    allow_origin_regex=".*",  # <- Esto permite cualquier origen como fallback
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# Incluir rutas
# ================================
app.include_router(dashboard.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ================================
# Configuración de templates HTML
# ================================
templates = Jinja2Templates(directory="templates")

# ================================
# DASHBOARD HTML
# ================================
@app.get("/dashboard")
def get_dashboard(request: Request):
    operations_path = Path("data/operations.json")
    operations = []
    if operations_path.exists():
        with open(operations_path, "r") as f:
            operations = json.load(f)

    operations = sorted(operations, key=lambda x: x["timestamp"], reverse=True)

    summary_by_symbol = {}
    for op in operations:
        symbol = op["symbol"]
        if symbol not in summary_by_symbol:
            summary_by_symbol[symbol] = op

    news_list = [
        {"title": "⚡ ETF impacta BTC", "symbol": "BTC", "source": "Simulado"},
        {"title": "⚡ Regulation impacta ETH", "symbol": "ETH", "source": "Simulado"},
    ]

    economic_events = [
        {"title": "📊 NFP Payroll", "date": "2025-07-05", "impact": "Alto"},
        {"title": "🧾 CPI Report", "date": "2025-07-07", "impact": "Medio"},
    ]

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "operations": operations,
        "summary": summary_by_symbol.values(),
        "news_list": news_list,
        "economic_events": economic_events,
    })

@app.get("/")
def read_root():
    return {"message": "Bienvenido a InteliBotX API 🚀"}

# ================================
# INCLUIR TODOS LOS ROUTERS
# ================================
from routes.spot import router as spot_router
from routes.futures import router as futures_router
from routes.testnet import router as testnet_router
from routes import test_signature
from routes.smart_trade_routes import router as smart_trade_router

app.include_router(spot_router, prefix="/spot", tags=["spot"])
app.include_router(futures_router, prefix="/futures", tags=["futures"])
app.include_router(testnet_router, tags=["testnet"])
app.include_router(test_signature.router)
app.include_router(smart_trade_router, prefix="/api", tags=["smart-trade"])

# ================================
# RUN LOCAL OPCIONAL
# ================================
if __name__ == "__main__":
    from execution.smart_trade_session import SmartTradeSession
    session = SmartTradeSession(symbol="BTCUSDT", interval="15m", stake=20.0)
    session.run()

print("🔍 Todas las variables:", dict(os.environ))