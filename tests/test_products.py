from assertpy import assert_that, soft_assertions

from services.serverest_api.api.products import Products


class TestProducts:
    client = Products()

    def test_if_product_can_be_created(self, login_user, create_product, context):
        responses = create_product

        with soft_assertions():
            for response in responses:
                assert_that(response.status_code).is_equal_to(201)
                assert_that(response.as_dict).is_not_empty()
                assert_that(response.as_dict["message"]).contains("Cadastro realizado com sucesso")
                assert_that(response.as_dict).contains("_id")
                assert_that(response.as_dict["_id"]).is_not_none()

    def test_if_product_can_be_fetched(self, login_user, create_product, context):
        products = context.get("produtos")

        with soft_assertions():
            for product_data in products:
                _id = product_data["_id"]
                name = product_data["nome"]
                price = product_data["preco"]
                description = product_data["descricao"]
                quantity = product_data["quantidade"]

                response = self.client.get_product(_id=_id, nome=name, preco=price, descricao=description,
                                                   quantidade=quantity)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()

                for product in response.as_dict["produtos"]:
                    assert_that(product["nome"]).is_equal_to(name)
                    assert_that(product["preco"]).is_equal_to(price)
                    assert_that(product["descricao"]).is_equal_to(description)
                    assert_that(product["quantidade"]).is_equal_to(quantity)

    def test_if_product_can_be_fetched_by_id(self, login_user, create_product, context):
        products = context.get("produtos")

        with soft_assertions():
            for product_data in products:
                _id = product_data["_id"]
                name = product_data["nome"]
                price = product_data["preco"]
                description = product_data["descricao"]
                quantity = product_data["quantidade"]

                response = self.client.get_product_by_id(_id)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()

                assert_that(response.as_dict['_id']).is_equal_to(_id)
                assert_that(response.as_dict['nome']).is_equal_to(name)
                assert_that(response.as_dict['preco']).is_equal_to(price)
                assert_that(response.as_dict['descricao']).is_equal_to(description)
                assert_that(response.as_dict['quantidade']).is_equal_to(quantity)

    def test_if_product_can_be_updated(self, login_user, random_admin_token, create_product, context,
                                        product_data_for_update):
        token = random_admin_token
        products = context.get("produtos")

        with soft_assertions():
            for index, product_data in enumerate(products):
                _id = product_data["_id"]
                update_data = product_data_for_update["produtos"][index]

                response = self.client.update_product(_id, update_data, token)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()
                assert_that(response.as_dict["message"]).contains("Registro alterado com sucesso")

                products[index].update(update_data)

        context.update({
            "produtos": products
        })

    def test_if_product_can_be_deleted(self, login_user, random_admin_token, create_product, context):
        token = random_admin_token
        product_ids = context.get("produto_ids")

        with soft_assertions():
            for product_id in product_ids:
                _id = product_id

                response = self.client.delete_product(_id, token)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()
                assert_that(response.as_dict["message"]).contains("Registro excluído com sucesso")

