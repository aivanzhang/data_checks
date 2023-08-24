class Item:
    def __init__(
        self,
        product_id,
        name,
        category,
        brand,
        price,
        discount=0,
        stock=0,
        size=None,
        color=None,
        material=None,
        description=None,
        features=None,
        rating=None,
        reviews=None,
        release_date=None,
        warranty=None,
        country_of_origin=None,
        dimensions: str = "",
        expiry_date=None,
    ):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.brand = brand
        self.price = price
        self.discount = discount
        self.stock = stock
        self.size = size
        self.color = color
        self.material = material
        self.description = description
        self.features = features
        self.rating = rating
        self.reviews = reviews
        self.release_date = release_date
        self.warranty = warranty
        self.country_of_origin = country_of_origin
        self.dimensions = dimensions
        self.expiry_date = expiry_date

    def __str__(self):
        return f"Product ID: {self.product_id}, Name: {self.name}, Category: {self.category}, Price: ${self.price}, Stock: {self.stock}"

    def __repr__(self):
        return self.__str__()
