from hamcrest import assert_that, equal_to


def get_data():
    return "data"


def run_check():
    data = get_data()
    try:
        assert_that(data, equal_to("data"))
    except AssertionError:
        fail()
        return

    success()


def success():
    print("YES!")


def fail():
    print("NO!")
