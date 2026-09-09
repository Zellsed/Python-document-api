from sqlalchemy import select

from app.data.database import SessionLocal
from app.data.models import Base, Document

db = SessionLocal()

Base.metadata.create_all(bind=db.get_bind())

stmt = select(Document)
document = db.scalars(stmt).all()

for doc in document:
  print(doc)

db.close()