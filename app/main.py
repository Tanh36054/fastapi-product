from fastapi import FastAPI
from app.database import Base, engine
from app.routers.product_router import router as product_router

app = FastAPI()

# tao bang trong database
Base.metadata.create_all(bind=engine)

#dang ky router
app.include_router(product_router)

@app.get("/")
def home():
    return {"message:" "FastAPI Product API is running!"}