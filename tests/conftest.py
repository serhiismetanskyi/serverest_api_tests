import random

import pytest

from config import *
from services.serverest_api.api.carts import Carts
from services.serverest_api.api.login import Login
from services.serverest_api.api.products import Products
from services.serverest_api.api.users import Users
from utils.calculator import Calculator
from utils.file_manager import FileManager
from utils.data_generator import DataGenerator


@pytest.fixture
def context():
    return {}


@pytest.fixture
def get_user_token(context):
    users_list = context.get("usuarios")

    def get_token(user_id):
        user = next((user for user in users_list if user["_id"] == user_id), None)
        if user:
            return user['authorization']
        else:
            raise ValueError(f"User with id {user_id} not found")

    return get_token


@pytest.fixture
def random_admin_token(context):
    users_list = context.get("usuarios")
    admins = [user for user in users_list if user["administrador"] == 'true']
    random_admin = random.choice(admins)
    authorization = random_admin['authorization']
    return authorization


@pytest.fixture
def get_product_ids(context):
    product_ids = context.get("produto_ids")
    return product_ids


@pytest.fixture
def get_product_price(context):
    products_list = context.get("produtos")

    def get_price(product_id):
        product = next((product for product in products_list if product["_id"] == product_id), None)
        if product:
            return product['preco']
        else:
            raise ValueError(f"Product with id {product_id} not found")

    return get_price


@pytest.fixture
def get_products_quantity(context):
    products = context.get("produtos")
    quantity_map = {product["_id"]: product["quantidade"] for product in products}
    return quantity_map


@pytest.fixture
def user_data_for_create():
    DataGenerator.generate_user_data_for_create(num_users=MAX_USERS_COUNT)
    return FileManager.read_file("create_user_data.json")


@pytest.fixture
def user_data_for_update():
    DataGenerator.generate_user_data_for_update(num_users=MAX_USERS_COUNT)
    return FileManager.read_file("update_user_data.json")


@pytest.fixture
def create_user(user_data_for_create, context):
    client = Users()
    users = user_data_for_create["usuarios"]
    responses = []

    for user_data in users:
        response = client.create_user(user_data)
        responses.append(response)

        user_data["_id"] = response.as_dict["_id"]

    context.update({
        "usuarios": users
    })

    return responses


@pytest.fixture
def login_user(create_user, context):
    client = Login()
    users = context.get("usuarios")
    responses = []

    for user_data in users:
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }

        response = client.login(login_data)
        responses.append(response)

        user_data["authorization"] = response.as_dict["authorization"]

    context["usuarios"] = users

    return responses


@pytest.fixture
def product_data_for_create():
    DataGenerator.generate_product_data_for_create(num_products=MAX_PRODUCTS_COUNT)
    return FileManager.read_file("create_product_data.json")


@pytest.fixture
def product_data_for_update():
    DataGenerator.generate_product_data_for_update(num_products=MAX_PRODUCTS_COUNT)
    return FileManager.read_file("update_product_data.json")


@pytest.fixture
def create_product(random_admin_token, product_data_for_create, context):
    client = Products()
    token = random_admin_token
    products = product_data_for_create["produtos"]
    product_ids = []
    responses = []

    for product_data in products:
        response = client.create_product(product_data, token)
        responses.append(response)

        product_data["_id"] = response.as_dict["_id"]
        product_ids.append(response.as_dict["_id"])

    context.update({
        "produto_ids": product_ids,
        "produtos": products
    })

    return responses


@pytest.fixture
def generate_cart_data_for_create(get_product_ids, get_products_quantity):
    DataGenerator.generate_cart_data_for_create(get_product_ids, get_products_quantity,
                                                num_carts=MAX_CARTS_COUNT,
                                                max_products_per_cart=MAX_PRODUCTS_PER_CART_COUNT,
                                                max_quantity_per_product=MAX_QUANTITY_PER_PRODUCT)
    return FileManager.read_file("create_cart_data.json")


@pytest.fixture
def create_cart(create_product, generate_cart_data_for_create, context, get_product_price):
    client = Carts()
    users = context.get("usuarios")
    carts = generate_cart_data_for_create["carrinhos"]
    responses = []

    for user_data, cart_data in zip(users, carts):
        user_id = user_data["_id"]
        token = user_data["authorization"]

        response = client.create_cart(cart_data, token)
        responses.append(response)

        cart_data["_id"] = response.as_dict["_id"]

        products = cart_data["produtos"]
        quantity_total = Calculator.calculate_quantity_total_in_cart(products)
        price_total = 0

        for product in products:
            _id = product["idProduto"]
            quantity = product["quantidade"]
            price = get_product_price(_id)
            price_total += Calculator.calculate_price_total_in_cart(price, quantity)

        cart_data["quantidadeTotal"] = quantity_total
        cart_data["precoTotal"] = price_total
        cart_data["idUsuario"] = user_id

    context.update({
        "carrinhos": carts
    })

    return responses
