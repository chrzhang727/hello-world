class TestCase1:
    def set_up(self):
        pass
    """
        pytest --alluredir=/tmp/my_allure_results
        allure serve /tmp/my_allure_results
    """
    def test_1(self):
        assert 1==2, "Failed to execute test_1"

    def test_2(self):
        print("function in test_2")
        assert 3==2, "Failed to execute test_2"


