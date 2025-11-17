from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductCreate, Product as ProductSchema

router = APIRouter(prefix="/products", tags = ["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.post("/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/", response_model=list[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
    

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
    

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, data: ProductCreate, db: Session=Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code = 404, detail="Product not found")
        
    for key, value in data.dict().items():
        setattr(product, key, value)
        
    db.commit()
    db.refresh(product)
    return product
    

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code = 404, detail="Product not found")
        
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}