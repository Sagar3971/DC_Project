from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
import re


app = FastAPI()

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