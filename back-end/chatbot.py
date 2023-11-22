import re
from sqlalchemy.orm import Session, sessionmaker
import db_models
from db_connect import db_engine


def get_db_session(engine):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except Exception as ex:
        print("Error getting DB session : ", ex)
        return None


in_progress_carts = {}


def process_intent(intent, response_parameters, session_id: str):
    match intent:
        case 'track.order':
            return ###
        case 'add.items':
            return add_order(response_parameters, session_id)
        case 'order.brand':
            return get_available_brands(response_parameters, session_id)
        case 'view.cart':
            return ###
        case 'place.the.order':
            return ###
        case 'remove.from.cart':
            return ###
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


def add_order(order_parameters: dict, session_id: str):
    grocery_items = order_parameters['grocery-item']
    grocery_quantity = order_parameters["number"]

    if len(grocery_items) == len(grocery_quantity):
        new_cart_item = {item: {'quantity': int(qty)} for item, qty in zip(grocery_items, grocery_quantity)}
        if session_id in in_progress_carts:
            current_grocery_cart = in_progress_carts[session_id]
            current_grocery_cart.update(new_cart_item)
            in_progress_carts[session_id] = current_grocery_cart
        else:
            in_progress_carts[session_id] = new_cart_item

        list_of_items = list(in_progress_carts[session_id].keys())
        list_of_items_without_brand = []

        for item in list_of_items:
            if "brand" not in in_progress_carts[session_id][item].keys():
                list_of_items_without_brand.append(item)

        response_text = get_item_choices(list_of_items_without_brand)
    else:
        response_text = "Sorry, I did not get that. Please specify grocery items and their quantities clearly."

    return response_text


def get_available_brands(order_parameters: dict, session_id: str):
    grocery_items = order_parameters['grocery-item']
    grocery_brands = order_parameters['brand']

    if len(grocery_items) != len(grocery_brands):
        return f"Sorry, Please specify brands for all your grocery items at ones"

    for item in grocery_items:
        cart_item = in_progress_carts[session_id]
        if item in cart_item:
            index = grocery_items.index(item)
            cart_item[item]['brand'] = grocery_brands[index]
            brand_name = cart_item[item]['brand'] if cart_item[item]['brand'] != "great\xa0value" else "great value"
            cart_item[item]['price'] = get_item_prices(item_name=item, item_brand=brand_name)[0]
            in_progress_carts[session_id] = cart_item

    cart_item_info_str = convert_cart_items_to_str(in_progress_carts[session_id])
    response_text = f"In your cart, you have {cart_item_info_str}. "

    unbranded_items = []

    for key in in_progress_carts[session_id]:
        if "brand" not in in_progress_carts[session_id][key].keys():
            unbranded_items.append(key)

    if len(unbranded_items) > 0:
        response_text += f"You need to specify brands for {unbranded_items}"
    else:
        response_text += "Do you need anything else?"
    return response_text


def convert_cart_items_to_str(grocery_cart: dict):
    cart_items_str = ", ".join([f"{int(value['quantity'])} {value['brand']} {key} " +
                                str('for $' + str(value['price'] * int(value['quantity'])) if value['price'] else '') +
                                f"" for key, value in grocery_cart
                               .items()])
    return cart_items_str


def get_item_choices(items):
    db_session = get_db_session(engine=db_engine)
    available_items = db_session.query(db_models.Item.name, db_models.Item.company, db_models.Item.price).filter(
        db_models.Item.name.in_(items)).all()
    available_items_dict = {}

    for item, brand, price in available_items:
        available_items_dict.setdefault(item, set()).add((brand, price))
    available_items_str = ""
    for item, options in available_items_dict.items():
        available_items_str += f"For {item} we have options from: "
        options_list = []
        for brand, price in options:
            options_list.append(f"{brand} for {price}")
        available_items_str += ', '.join(options_list)
        available_items_str += ". "

    return available_items_str


def get_item_prices(item_name: str, item_brand: str):
    db_session = get_db_session(engine=db_engine)
    item_price = (db_session.query(db_models.Item.price)
                  .filter(db_models.Item.name == item_name and db_models.Item.company == item_brand).first())
    if item_price:
        result = item_price
    else:
        result = -1
    return result


def get_total_cart_value(session_id: str):
    total_price = 0
    current_cart = in_progress_carts[session_id]
    for item in current_cart.keys():
        if current_cart[item]['price'] and current_cart[item]['price'] > 0:
            item_price = current_cart[item]['price']
        else:
            item_price = 0
        total_price += item_price * current_cart[item]['quantity']

    return total_price


