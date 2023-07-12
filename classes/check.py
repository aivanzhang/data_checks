from hamcrest import assert_that, equal_to


class CheckClass:
    data_str: str = "data"

    def get_data(self):
        return self.data_str

    def run_check(self):
        data = self.get_data()
        try:
            assert_that(data, equal_to("data"))
        except AssertionError:
            self.fail()
            return

        self.success()

    @classmethod
    def success(cls):
        print("YES!")

    @classmethod
    def fail(cls):
        print("NO!")
