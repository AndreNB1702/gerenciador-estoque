from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProdutoBD(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False, default=0)
    preco = Column(Float, nullable=False, default=0.0)

Base.metadata.create_all(bind=engine)

class ProdutoSchema(BaseModel):
    nome: str
    quantidade: int = Field(..., ge=0, description="A quantidade não pode ser negativa")
    preco: float = Field(..., ge=0.0, description="O preço não pode ser negativo")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def rota_verificacao():
    return {"status": "rodando", "banco_configurado": True, "sistema": "estoque"}

@app.get("/produtos")
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoBD).all()

@app.post("/produtos")
def criar_produto(produto: ProdutoSchema, db: Session = Depends(get_db)):
    novo_produto = ProdutoBD(
        nome=produto.nome,
        quantidade=produto.quantidade,
        preco=produto.preco
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoBD).filter(ProdutoBD.id == produto_id).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    db.delete(produto)
    db.commit()
    return {"status": "sucesso", "mensagem": "Produto removido do estoque"}

@app.put("/produtos/{produto_id}/comprar")
def comprar_produto(produto_id: int, quantidade_comprada: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoBD).filter(ProdutoBD.id == produto_id).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    if produto.quantidade < quantidade_comprada:
        raise HTTPException(status_code=400, detail="Quantidade insuficiente em estoque")
        
    produto.quantidade -= quantidade_comprada
    db.commit()
    db.refresh(produto)
    return {"status": "sucesso", "mensagem": "Compra realizada", "estoque_atual": produto.quantidade}