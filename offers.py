
class AbstractOffer(object):

    """ An interface for the offer classes """

    def __init__(self, target_product):
        self.target_product = target_product

    def calculate_line_total(self, cart_item, store, *args):
        """ Returns the subtotal of the cart items """
        raise NotImplementedError()


class MultiBuyOffer(AbstractOffer):

    """
    But X quantity one item to get another item free

    eg. a Buy One Get One Free offer would look like:
        bogof_offer = MultiBuyOffer(1, 1, 'strawberries')
    and a buy two get one free would look like:
        multibuy_offer = MultiBuyOffer(2, 1, 'strawberries')
    """

    def __init__(self, target_product, charge_for_quantity, free_quantity, *args, **kwargs):
        self.charge_for_quantity = charge_for_quantity
        self.free_quantity = free_quantity
        super(MultiBuyOffer, self).__init__(target_product, *args, **kwargs)

    def calculate_line_total(self, cart_item, store, *args):
        """Charge for multiples of the quotient and add remainder."""
        bundles, remainder = divmod(
            cart_item.quantity, self.charge_for_quantity + self.free_quantity)
        if remainder > self.charge_for_quantity:
            bundles += 1
            remainder = 0
        charge_quantity = (bundles * self.charge_for_quantity) + remainder
        return store.get_product_price(cart_item.product) * charge_quantity


class DependentDiscountOffer(AbstractOffer):

    """
    A certain amount of discount applied to the items dependent on other items
    """

    def __init__(self, target_product, dependent_product, discount, *args, **kwargs):
        self.dependent_product = dependent_product
        self.discount = discount
        super(DependentDiscountOffer, self).__init__(
            target_product, *args, **kwargs)

    def calculate_line_total(self, cart_item, store, cart, *args):
        """
        Return total for cart_item taking into account the eligible
        discount that may apply in the presence of dependent products in the
        cart
        """
        try:
            dependent_quantity = cart.get_item(self.dependent_product).quantity
        except AttributeError:
            return cart_item.get_line_total(store)
        else:
            discount_eligibility = min(dependent_quantity, cart_item.quantity)
            total_item_price = store.get_product_price(cart_item.product)
            total_amount = discount_eligibility * total_item_price
            discounted_total = total_amount - \
                (total_amount * self.discount)
            remainder_total = (
                cart_item.quantity - discount_eligibility) * total_item_price

            return discounted_total + remainder_total
