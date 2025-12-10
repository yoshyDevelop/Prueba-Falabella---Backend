from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pandas as pd
import io

from database import engine, get_db, Base
from models import Customer, Purchase, DocumentType

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rios del Desierto API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/customer/{doc_number}")
def get_customer_by_document(doc_number: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.document_number == doc_number).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    total_purchases = sum(p.amount for p in customer.purchases)
    
    return {
        "id": customer.id,
        "document_number": customer.document_number,
        "document_type_code": customer.document_type.code,
        "document_type_name": customer.document_type.name,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone": customer.phone,
        "total_purchases": total_purchases,
        "purchase_count": len(customer.purchases)
    }


@app.get("/api/loyalty-report")
def get_loyalty_report(db: Session = Depends(get_db)):
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    
    query = """
        SELECT 
            c.id as customer_id,
            c.document_number,
            c.first_name,
            c.last_name,
            c.email,
            c.phone,
            dt.code as document_type_code,
            p.amount,
            p.created_at
        FROM purchases p
        JOIN customers c ON p.customer_id = c.id
        JOIN document_types dt ON c.document_type_id = dt.id
        WHERE p.created_at >= :one_month_ago
    """
    
    df = pd.read_sql(query, engine, params={"one_month_ago": one_month_ago})
    
    if df.empty:
        raise HTTPException(status_code=404, detail="No hay compras en el ultimo mes")
    
    loyalty_df = df.groupby([
        'customer_id', 'document_number', 'first_name', 
        'last_name', 'email', 'phone', 'document_type_code'
    ]).agg({
        'amount': 'sum'
    }).reset_index()
    
    loyalty_df.columns = [
        'ID Cliente', 'Documento', 'Nombre', 
        'Apellido', 'Email', 'Telefono', 'Tipo Doc', 'Total Compras'
    ]
    
    loyalty_df = loyalty_df[loyalty_df['Total Compras'] > 5000000]
    
    if loyalty_df.empty:
        raise HTTPException(
            status_code=404, 
            detail="No hay clientes que superen el umbral de fidelizacion (5,000,000)"
        )
    
    loyalty_df = loyalty_df.sort_values('Total Compras', ascending=False)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        loyalty_df.to_excel(writer, index=False, sheet_name='Reporte Fidelizacion')
    output.seek(0)
    
    filename = f"reporte_fidelizacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/api/customers")
def get_all_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return [
        {
            "id": c.id,
            "document_number": c.document_number,
            "document_type_code": c.document_type.code,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "email": c.email,
            "phone": c.phone
        }
        for c in customers
    ]
