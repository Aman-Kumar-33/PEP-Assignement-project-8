import datetime
from sqlalchemy.orm import Session
from backend.app.db.database import SessionLocal, engine
from backend.app.models import models
from backend.app.core.security import get_password_hash

def seed_data():
    db: Session = SessionLocal()

    # 1. Clear existing data (Optional - careful with this!)
    # models.Base.metadata.drop_all(bind=engine)
    # models.Base.metadata.create_all(bind=engine)

    print("🌱 Seeding database...")

    # 2. Create a Sample Provider
    provider = db.query(models.User).filter(models.User.email == "pro@example.com").first()
    if not provider:
        provider = models.User(
            email="pro@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Alex Expert",
            role=models.RoleEnum.provider
        )
        db.add(provider)
        db.commit()
        db.refresh(provider)

    # 3. Create Categories
    categories_data = ["Home Repair", "Tutoring", "Wellness", "Consulting"]
    categories = []
    for cat_name in categories_data:
        cat = db.query(models.Category).filter(models.Category.name == cat_name).first()
        if not cat:
            cat = models.Category(name=cat_name)
            db.add(cat)
            categories.append(cat)
    db.commit()

    # 4. Create Services
    services_data = [
        {"title": "Fix Leaky Faucet", "price": 45.0, "duration": 30, "cat_idx": 0, "desc": "Professional plumbing repair for kitchen or bathroom."},
        {"title": "Python Programming Help", "price": 60.0, "duration": 60, "cat_idx": 1, "desc": "1-on-1 session to debug your code and learn concepts."},
        {"title": "Deep Tissue Massage", "price": 80.0, "duration": 90, "cat_idx": 2, "desc": "Relaxing full-body massage by a certified therapist."},
        {"title": "Business Strategy Call", "price": 120.0, "duration": 45, "cat_idx": 3, "desc": "Optimize your startup operations and growth plan."},
    ]

    for s in services_data:
        existing = db.query(models.Service).filter(models.Service.title == s["title"]).first()
        if not existing:
            new_service = models.Service(
                title=s["title"],
                description=s["desc"],
                price=s["price"],
                duration_minutes=s["duration"],
                category_id=db.query(models.Category).all()[s["cat_idx"]].id,
                provider_id=provider.id
            )
            db.add(new_service)
    
    db.commit()
    print("✅ Database successfully seeded with sample services!")
    db.close()

if __name__ == "__main__":
    seed_data()