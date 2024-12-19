from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis_om import HashModel
from config import redis
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: float
    status: str

    class Meta:
        database = redis


class CreateOrder(BaseModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: float
    status: str


def format_order(pk: str):
    order = Order.get(pk)
    return {
        "product_id": order.product_id,
        "price": order.price,
        "fee": order.fee,
        "total": order.total,
        "quantity": order.quantity,
        "status": order.status,
    }


@app.get("/orders", response_model=List[CreateOrder])
async def all_orders():
    return [format_order(order) for order in Order.all_pks()]


@app.post("/orders")
async def create_order(order: CreateOrder):
    to_save = Order(**order.dict())
    return to_save.save()

@app.get("/orders/{pk}")
async def get_order(pk: str):
    order = Order.get(pk)
    return format_order(order)
