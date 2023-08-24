from hamcrest import assert_that, equal_to, is_not, greater_than, less_than_or_equal_to
import pandas as pd
import re
from data_checks.data_check import DataCheck
from examples.operations.inventory.item import Item


class ItemCheck(DataCheck):
    def required_fields(self):
        item: Item = self.group["value"]
        assert_that(
            item.product_id,
            is_not(None),
            f"product_id is required for {item.name}",
        )
        assert_that(
            item.name,
            is_not(None),
            f"name is required for productId: {item.product_id}",
        )
        assert_that(
            item.category,
            is_not(None),
            f"category is required for productId: {item.product_id}",
        )
        assert_that(
            item.brand,
            is_not(None),
            f"brand is required for productId: {item.product_id}",
        )
        assert_that(
            item.price,
            is_not(None),
            f"price is required for productId: {item.product_id}",
        )
        assert_that(
            item.stock,
            is_not(None),
            f"stock is required for productId: {item.product_id}",
        )

    def reasonable_values(self):
        item: Item = self.group["value"]
        assert_that(
            item.price,
            greater_than(
                0,
            ),
            f"price should be a positive value for productId: {item.product_id}",
        )
        assert_that(
            item.discount,
            greater_than(
                -1,
            ),
            f"discount should be a non-negative value for productId: {item.product_id}",
        )
        assert_that(
            item.stock,
            greater_than(
                -1,
            ),
            f"stock should be a positive integer for productId: {item.product_id}",
        )

    def date_consistency(self):
        item: Item = self.group["value"]
        assert_that(
            item.release_date,
            is_not(None),
            f"release_date is required for productId: {item.product_id}",
        )
        assert_that(
            item.expiry_date,
            is_not(None),
            f"expiry_date is required for productId: {item.product_id}",
        )
        assert_that(
            item.expiry_date,
            greater_than(
                pd.to_datetime("today"),
            ),
            f"expiry_date should be in the future (i.e. has not expired) productId: {item.product_id}",
        )
        assert_that(
            item.release_date,
            less_than_or_equal_to(
                item.expiry_date,
            ),
            f"release_date should be before expiry_date for productId: {item.product_id}",
        )

    def ratings_reviews(self):
        item: Item = self.group["value"]
        assert_that(
            item.rating,
            less_than_or_equal_to(
                5,
            ),
            f"rating should be less than 5 for productId: {item.product_id}",
        )
        assert_that(
            item.rating,
            greater_than(
                0,
            ),
            f"rating should be greater than 0 for productId: {item.product_id}",
        )
        assert_that(
            item.reviews,
            greater_than(
                -1,
            ),
            f"reviews should be a non-negative integer for productId: {item.product_id}",
        )

    def discount_limit(self):
        item: Item = self.group["value"]
        assert_that(
            item.discount,
            less_than_or_equal_to(
                item.price,
            ),
            f"discount should not be greater than price for productId: {item.product_id}",
        )

    def dimensions_format(self):
        item: Item = self.group["value"]
        dimensions_regex = re.compile(r"^\d+x\d+x\d+ in$")
        matched = dimensions_regex.match(item.dimensions)
        assert_that(
            matched,
            is_not(None),
            f"dimensions is required for productId: {item.product_id}",
        )
