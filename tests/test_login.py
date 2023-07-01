from assertpy import assert_that, soft_assertions

from services.serverest_api.api.login import Login


class TestLogin:
    client = Login()

    def test_if_user_can_be_login(self, login_user, context):
        responses = login_user

        with soft_assertions():
            for response in responses:
                assert_that(response.status_code).is_equal_to(200)
                assert_that(response.as_dict).is_not_empty()
                assert_that(response.as_dict["message"]).contains("Login realizado com sucesso")
                assert_that(response.as_dict).contains("authorization")
                assert_that(response.as_dict["authorization"]).is_not_none()