import json

class NoSuchProductError(Exception):
    pass


class ProductStore(object):

    """ Class to Store the Products and map the prices """

    @classmethod
    def load_products(cls, filepath):
        """ Return a cls instance initialized from a JSON file of products data """
        with open(filepath, 'rb') as loader:
            json_data = json.load(loader)
            items = json_data
        return cls(items)

    def __init__(self, items):
        """
        Products data format

	    "products": [
            {"name": "Baked Beans" ,"price": 0.99},
            {"name": "Biscuits" ,"price": 1.2},
	        {"name": "Sardines" ,"price": 1.89},
	        {"name": "Shampoo" ,"price": 2},
	    ]
        """
        self.items = items

    def get_product_price(self, product_name):
        """ Return the price of the product """

        product_price = next((prod["price"] for prod in self.items if prod["name"] == product_name), None)
        if product_price is None:
            raise NoSuchProductError("Product '{product_name}' doesn't exists.".format(product_name=product_name))
        else:
            return product_price
