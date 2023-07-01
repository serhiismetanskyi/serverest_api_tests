from assertpy import assert_that, soft_assertions

from services.serverest_api.api.users import Users


class TestUsers:
    client = Users()

    def test_if_user_can_be_created(self, create_user, context):
        responses = create_user

        with soft_assertions():
            for response in responses:
                assert_that(response.status_code).is_equal_to(201)
                assert_that(response.as_dict).is_not_empty()
                assert_that(response.as_dict["message"]).contains("Cadastro realizado com sucesso")
                assert_that(response.as_dict).contains("_id")
                assert_that(response.as_dict["_id"]).is_not_none()

    def test_if_user_can_be_fetched(self, create_user, context):
        users = context.get("usuarios")

        with soft_assertions():
            for user_data in users:
                _id = user_data["_id"]
                name = user_data["nome"]
                email = user_data["email"]
                is_admin = user_data["administrador"]

                response = self.client.get_user(_id=_id, nome=name, email=email, administrador=is_admin)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()

                for user in response.as_dict["usuarios"]:
                    assert_that(user["_id"]).is_equal_to(_id)
                    assert_that(user["nome"]).is_equal_to(name)
                    assert_that(user["email"]).is_equal_to(email)
                    assert_that(user["administrador"]).is_equal_to(is_admin)

    def test_if_user_can_be_fetched_by_id(self, create_user, context):
        users = context.get("usuarios")

        with soft_assertions():
            for user_data in users:
                _id = user_data["_id"]
                name = user_data["nome"]
                email = user_data["email"]
                is_admin = user_data["administrador"]

                response = self.client.get_user_by_id(_id)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()

                assert_that(response.as_dict["_id"]).is_equal_to(_id)
                assert_that(response.as_dict["nome"]).is_equal_to(name)
                assert_that(response.as_dict["email"]).is_equal_to(email)
                assert_that(response.as_dict["administrador"]).is_equal_to(is_admin)

    def test_if_user_can_be_updated(self, create_user, context, user_data_for_update):
        users = context.get("usuarios")

        with soft_assertions():
            for index, user_data in enumerate(users):
                _id = user_data["_id"]
                update_data = user_data_for_update["usuarios"][index]

                response = self.client.update_user(_id, update_data)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()
                assert_that(response.as_dict["message"]).contains("Registro alterado com sucesso")

                users[index].update(update_data)

        context.update({
            "usuarios": users
        })

    def test_if_user_can_be_deleted(self, create_user, context):
        users = context.get("usuarios")

        with soft_assertions():
            for user_data in users:
                _id = user_data["_id"]

                response = self.client.delete_user(_id)

                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()
                assert_that(response.as_dict["message"]).contains("Registro excluído com sucesso")


