
class Cart(object):

    """
    Shopping Cart Class to handle the products
    Returns the total amount based on offers

    ...

    Methods
    -------
    __init__(store=None)
        Initialises the object for Cart Class
        store - an instance of the ProductStore Class

    get_total(offers=None)
        Returns the total amount for the products in the cart

    add(item, quantity)
        Add product/item of quantity to the cart

    remove(item, quantity)
        Remove product/item of quantity to the cart
        
    get_item(item)
        Returns the product item object


    Attributes
    ----------
    store : instance
        an instance of the product store class

    offers : list
        list of offers class object

    item : str
        name of the item

    quantity : int
        number of items added to the cart

    """
    

    def __init__(self, store=None):
        self.items = []
        self.total = 0
        self.product_store = store

    def __len__(self):
        return len(self.items)        

    def get_total(self, offers=None):
        """
        Return the total amount of items in the cart
        """

        amounts = []
        for item in self.items:
            
            # Cart total without any offers applied
            line_total = item.get_line_total(self.product_store)

            if offers is not None:
                for offer in offers:
                    if offer.target_product == item.product:
                        offer_total = offer.calculate_line_total(
                            item, self.product_store, self)

                        if offer_total < line_total:
                            line_total = offer_total

            amounts.append(line_total)
            
        cart_total = float(sum(amounts))
        if cart_total <= 0.0:
            cart_total = 0
            
        return cart_total

    def add(self, item, quantity=1):
        """
        Add an item to the cart. Return the cart item.

        Add the item multiple times will return the total quantity
        """
        cart_item = self.get_item(item)
        if cart_item is None:
            cart_item = CartItem(item, quantity)
            self.items.append(cart_item)
        else:
            cart_item.quantity += quantity
        return cart_item

    def remove(self, item, quantity=1):
        """
        Remove the item(s) from the cart
        """
        cart_item = self.get_item(item)
        if cart_item is None:
            raise Exception("Product '{}' not exists in the cart".format(item))
        else:
            if cart_item.quantity >= quantity:
                cart_item.quantity -= quantity
            else:
                raise Exception("Quantity is greater than the cart item ")
                
        
    def get_item(self, item_name):
        """ Return CartItem where product corresponds with item_name. """
        return next((item for item in self.items if item.product == item_name), None)


class CartItem(object):

    def __init__(self, product, quantity=1):
        self.product = product
        self.quantity = quantity

    def get_line_total(self, store):
        """ Return total derived from product in store."""
        return store.get_product_price(self.product) * self.quantity
    
