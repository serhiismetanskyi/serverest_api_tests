from assertpy import assert_that, soft_assertions

from services.serverest_api.api.carts import Carts


class TestCarts:
    client = Carts()

    def test_if_cart_can_be_created(self, login_user, create_cart, context):
        responses = create_cart

        with soft_assertions():
            for response in responses:
                assert_that(response.status_code).is_equal_to(201)
                assert_that(response.as_dict).is_not_empty()
                assert_that(response.as_dict["message"]).contains("Cadastro realizado com sucesso")
                assert_that(response.as_dict).contains("_id")
                assert_that(response.as_dict["_id"]).is_not_none()

    def test_if_cart_can_be_fetched(self, login_user, create_cart, context, get_product_price):
        carts = context.get("carrinhos")

        with soft_assertions():
            for cart_data in carts:
                _id = cart_data["_id"]
                price_total = cart_data["precoTotal"]
                quantity_total = cart_data["quantidadeTotal"]
                user_id = cart_data["idUsuario"]

                response = self.client.get_carts(_id=_id, precoTotal=price_total, quantidadeTotal=quantity_total,
                                                 idUsuario=user_id)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()

                for cart in response.as_dict["carrinhos"]:
                    assert_that(cart["_id"]).is_equal_to(_id)
                    assert_that(cart["precoTotal"]).is_equal_to(price_total)
                    assert_that(cart["quantidadeTotal"]).is_equal_to(quantity_total)
                    assert_that(cart["idUsuario"]).is_equal_to(user_id)

                    for product in cart["produtos"]:
                        product_id = product["idProduto"]
                        product_price = get_product_price(product_id)
                        product_quantity = product["quantidade"]

                        assert_that(product["idProduto"]).is_equal_to(product_id)
                        assert_that(product["precoUnitario"]).is_equal_to(product_price)
                        assert_that(product["quantidade"]).is_equal_to(product_quantity)

    def test_if_cart_can_be_fetched_by_id(self, login_user, create_cart, context, get_product_price):
        carts = context.get("carrinhos")

        with soft_assertions():
            for cart_data in carts:
                _id = cart_data["_id"]
                price_total = cart_data["precoTotal"]
                quantity_total = cart_data["quantidadeTotal"]
                user_id = cart_data["idUsuario"]

                response = self.client.get_cart_by_id(_id)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()

                assert_that(response.as_dict["_id"]).is_equal_to(_id)
                assert_that(response.as_dict["precoTotal"]).is_equal_to(price_total)
                assert_that(response.as_dict["quantidadeTotal"]).is_equal_to(quantity_total)
                assert_that(response.as_dict["idUsuario"]).is_equal_to(user_id)

                for product in response.as_dict["produtos"]:
                    product_id = product["idProduto"]
                    product_price = get_product_price(product_id)
                    product_quantity = product["quantidade"]

                    assert_that(product["idProduto"]).is_equal_to(product_id)
                    assert_that(product["precoUnitario"]).is_equal_to(product_price)
                    assert_that(product["quantidade"]).is_equal_to(product_quantity)

    def test_if_cart_can_be_checkout(self, login_user, create_cart, context, get_user_token):
        carts = context.get("carrinhos")

        with soft_assertions():
            for cart_data in carts:
                user_id = cart_data["idUsuario"]
                token = get_user_token(user_id)

                response = self.client.checkout(token)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()
                assert_that(response.as_dict["message"]).contains("Registro excluído com sucesso")

    def test_if_cart_can_be_deleted(self, login_user, create_cart, context, get_user_token):
        carts = context.get("carrinhos")

        with soft_assertions():
            for cart_data in carts:
                user_id = cart_data["idUsuario"]
                token = get_user_token(user_id)

                response = self.client.delete_cart(token)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()
                assert_that(response.as_dict["message"]).contains(
                    "Registro excluído com sucesso. Estoque dos produtos reabastecido")
