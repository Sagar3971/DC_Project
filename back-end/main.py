from fastapi import FastAPI,Request,Depends, status
from fastapi.responses import JSONResponse
import re
from pydantic import BaseModel
import db_models
from db_connect import db_engine, session_local
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from typing import Annotated

app = FastAPI()
db_models.declarative_base.metadata.create_all(bind=db_engine)


class ItemBaseModel(BaseModel):
    name: str
    company: str
    price: float


class OrderBaseModel(BaseModel):
    id: int
    items: str
    total_price: float
    status: str


def connect_to_db():
    db_connection = session_local()
    try:
        yield db_connection
    finally:
        db_connection.close()


# https://youtu.be/zzOwU41UjTM?t=1040

db_dependancy = Annotated[Session, Depends(connect_to_db)]


def get_db_session(engine):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except Exception as ex:
        print("Error getting DB session : ", ex)
        return None


@app.post("/order/", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderBaseModel, db: db_dependancy):
    db_user = db_models.Order(**order.model_dump())
    db.add(db_user)
    db.commit()


@app.get("/order/{id}", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderBaseModel, db: db_dependancy):
    db_user = db_models.Order(**order.model_dump())
    db.add(db_user)
    db.commit()


@app.post("/item/", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemBaseModel, db: db_dependancy):
    db_user = db_models.Item(**item.model_dump())
    db.add(db_user)
    db.commit()

@app.post("/")
async def df_request_handler(request: Request):
    print("RECEIVED")
    df_response = await request.json()
    response_intents = df_response['queryResult']['intent']['displayName']
    response_parameters = df_response['queryResult']['parameters']
    response_contexts = df_response['queryResult']['outputContexts']
    df_session_id = get_session_id_from_context(response_contexts[0]['name'])

    return JSONResponse(content={"fulfillmentText": process_intent(
        intent=response_intents,
        response_parameters=response_parameters,
        session_id=df_session_id)
    })


def process_intent(intent, response_parameters, session_id: str):
    match intent:
        case 'track.order':
            return #####
        case 'add.items':
            return #####
        case 'order.brand':
            return #####
        case 'view.cart':
            return #####
        case 'place.the.order':
            return #####
        case 'remove.from.cart':
            return #####
        case default:
            return ('I couldn\'t understand you. Please say "New Order" for placing a new order or "track order" to '
                    'track an order. also, only items available to add in your orders are "Milk", "Bread", "eggs", '
                    '"Sugar", "Salt", "Oil", "tomato Ketchup", "water" and "noodles". for example, you can say "add '
                    'two eggs".')


def get_session_id_from_context(context: str):
    extracted_session_id = re.search(r"/sessions/(.*?)/contexts/", context)
    if extracted_session_id:
        return extracted_session_id.group(1)
    return ""