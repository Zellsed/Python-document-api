import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger
from sqlalchemy.orm import Session

from src.app.data.database import get_db
from src.app.data.models import Document as DocumentModel
from src.app.pydantic.document import DocumentSchema, DocumentResponse
from src.app.redis.redis_client import redis_client

app = FastAPI()

@app.post("/documents", response_model=DocumentResponse)
def create_document(data: DocumentSchema, db: Session = Depends(get_db)):
  try:
    db_document = DocumentModel(
      title = data.title,
      content = data.content
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail="Error creating document")

@app.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
  try:
    cache_key = f"document:{document_id}"

    cached_document = redis_client.get(cache_key)

    if cached_document:
      return json.loads(cached_document)
    
    db_document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()

    if not db_document:
      raise HTTPException(status_code=404, detail="Document not found")

    dict_data = jsonable_encoder(db_document)

    redis_client.set(cache_key, json.dumps(dict_data), ex=60)

    return db_document
  except HTTPException:
    raise
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail="Error getting document")

@app.get("/documents", response_model=list[DocumentResponse])
def get_list_documents(db: Session = Depends(get_db)):
  try:
    return db.query(DocumentModel).all()
  except HTTPException:
    raise
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail="Error getting documents")

@app.put("/documents/{document_id}", response_model=DocumentResponse)
def update_document(document_id: int, data: DocumentSchema, db: Session = Depends(get_db)):
  try:
    db_document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()

    if not db_document:
      raise HTTPException(status_code=404, detail="Document not found")

    db_document.title = data.title
    db_document.content = data.content

    db.commit()
    db.refresh(db_document)

    cache_key = f"document:{document_id}"

    redis_client.delete(cache_key)

    return db_document
  except HTTPException:
    raise
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail="Error updating document")

@app.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
  try:
    db_document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()

    if not db_document:
      raise HTTPException(status_code=404, detail="Document not found")

    db.delete(db_document)
    db.commit()

    cache_key = f"document:{document_id}"

    redis_client.delete(cache_key)

    return {"message": "Document deleted successfully"}
  except HTTPException:
    raise
  except Exception as e:
    logger.error(e)
    raise HTTPException(status_code=500, detail="Error deleting document")