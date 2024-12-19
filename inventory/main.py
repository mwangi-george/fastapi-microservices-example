from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from redis_om import HashModel
from pydantic import BaseModel

from config import redis

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


class CreateProduct(BaseModel):
    name: str
    price: float
    quantity: int


def format_product(pk: str):

    _product = Product.get(pk)

    return {
        "id": _product.pk,
        "name": _product.name,
        "price": _product.price,
        "quantity": _product.quantity,
    }


@app.get("/products")
async def all_products():
    return [format_product(pk) for pk in Product.all_pks()]


@app.post("/products")
async def create_product(product: CreateProduct):
    to_save = Product(name=product.name, price=product.price, quantity=product.quantity)
    to_save.save()
    return to_save


@app.get("/products/{pk}")
async def single_product(pk):
    return Product.get(pk)


@app.delete("/products/{pk}")
async def delete_product(pk):
    return Product.delete(pk)

