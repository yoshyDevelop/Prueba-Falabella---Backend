from datetime import datetime, timedelta
from database import engine, SessionLocal, Base
from models import DocumentType, Customer, Purchase


def seed_database():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        existing = db.query(DocumentType).first()
        if existing:
            print("Base de datos ya tiene datos. Saltando seed...")
            return
        
        doc_types = [
            DocumentType(code="CC", name="Cedula de Ciudadania"),
            DocumentType(code="NIT", name="Numero de Identificacion Tributaria"),
            DocumentType(code="PAS", name="Pasaporte")
        ]
        db.add_all(doc_types)
        db.commit()
        print("Tipos de documento creados.")
        
        cc_type = db.query(DocumentType).filter(DocumentType.code == "CC").first()
        nit_type = db.query(DocumentType).filter(DocumentType.code == "NIT").first()
        
        customer1 = Customer(
            document_number="1234567890",
            first_name="Juan",
            last_name="Garcia Rodriguez",
            email="juan.garcia@email.com",
            phone="3001234567",
            document_type_id=cc_type.id
        )
        
        customer2 = Customer(
            document_number="900123456-1",
            first_name="Empresa",
            last_name="ABC S.A.S",
            email="contacto@empresaabc.com",
            phone="6011234567",
            document_type_id=nit_type.id
        )
        
        db.add_all([customer1, customer2])
        db.commit()
        print("Clientes creados.")
        
        now = datetime.utcnow()
        purchases = [
            Purchase(amount=2500000.0, created_at=now - timedelta(days=5), customer_id=customer1.id),
            Purchase(amount=1800000.0, created_at=now - timedelta(days=10), customer_id=customer1.id),
            Purchase(amount=1200000.0, created_at=now - timedelta(days=15), customer_id=customer1.id),
            Purchase(amount=350000.0, created_at=now - timedelta(days=20), customer_id=customer2.id),
            Purchase(amount=150000.0, created_at=now - timedelta(days=25), customer_id=customer2.id),
        ]
        
        db.add_all(purchases)
        db.commit()
        print("Compras creadas.")
        print(f"Cliente {customer1.first_name} tiene compras por: 5,500,000 (supera umbral de fidelizacion)")
        print(f"Cliente {customer2.first_name} tiene compras por: 500,000")
        
        print("\nSeed completado exitosamente!")
        
    except Exception as e:
        db.rollback()
        print(f"Error durante seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
