import os

import unittest
from cart import Cart, CartItem
from product import ProductStore, NoSuchProductError
from offers import NoOffer, MultiBuyOffer, DependentDiscountOffer


class CartTest(unittest.TestCase):

    def _create_product_store(self):
        '''Helper method to create populated ProductStore.'''
        products = [
            {"name": "apple" ,"price": 0.15},
            {"name": "ice cream" ,"price": 3.49},
            {"name": "dairy milk" ,"price": 2.00},
            {"name": "kitkat" ,"price": 2},
            ]
        return ProductStore(products)

    def test_get_total_is_float(self):
        '''Cart.get_total() returns a float.'''
        cart = Cart()
        self.assertTrue(type(cart.get_total()) is float)

    def test_add_single_item(self):
        '''Cart.add() a single item is successful.'''
        cart = Cart()
        cart.add('apple')
        self.assertEqual(len(cart), 1)

    def test_add_item_is_cartitem(self):
        '''Cart contains a single CartItem after cart.add().'''
        cart = Cart()
        cart.add('apple')
        self.assertTrue(type(cart) is Cart)

    def test_add_two_items(self):
        '''Adding more than one item increases cart length.'''
        cart = Cart()
        cart.add('apple')
        cart.add('kitkat')
        self.assertEqual(len(cart), 2)

    def test_add_two_same_item(self):
        '''Adding more than one of the same item does not create duplicate
        CartItems.'''
        cart = Cart()
        cart.add('apple')
        cart.add('apple')
        self.assertEqual(len(cart), 1)

    def test_add_two_same_item_increases_quantity(self):
        '''Adding an item that is already in the cart increases its
        quantity.'''
        cart = Cart()
        cart.add('apple')
        cart.add('apple')
        cartitem = cart.get_item('apple')
        self.assertEqual(cartitem.quantity, 2)

    def test_add_with_no_quantity(self):
        '''Adding an item without defining a quantity creates an item with a
        quantity of 1.'''
        cart = Cart()
        cart.add('apple')
        self.assertEqual(cart.get_item('apple').quantity, 1)

    def test_add_with_quantity(self):
        '''Adding an item with a quantity creates cart item with appropriate
        quantity.'''
        cart = Cart()
        cart.add('apple', 3)
        self.assertEqual(cart.get_item('apple').quantity, 3)

    def test_add_with_quantity_to_existing_item(self):
        '''Adding an item with a quantity increases the quantity of an
        existing item.'''
        cart = Cart()
        cart.add('apple', 2)
        cart.add('apple', 3)
        self.assertEqual(cart.get_item('apple').quantity, 5)

    def test_get_item(self):
        '''cart.get_item() returns expected CartItem.'''
        cart = Cart()
        cart.add('apple')
        cart.add('kitkat')
        returned_cart_item = cart.get_item('apple')
        self.assertTrue(type(returned_cart_item) is CartItem)
        self.assertEqual(returned_cart_item.product, 'apple')

    def test_get_item_not_in_cart(self):
        '''Attempt to get item with no corresponding CartItem returns None.'''
        cart = Cart()
        self.assertEqual(cart.get_item('apple'), None)

    def test_get_total_one_item(self):
        '''Correct total for one item in cart.'''
        cart = Cart(self._create_product_store())
        cart.add('apple')
        self.assertEqual(cart.get_total(), float('0.15'))

    def test_get_total_one_item_multiple_quantity(self):
        '''Correct total for one item with multiple quantity in cart.'''
        cart = Cart(self._create_product_store())
        cart.add('apple', 3)
        self.assertEqual(round(cart.get_total(), 2), float('0.45'))

    def test_get_total_multiple_items_multiple_quantity(self):
        '''Correct total for multiple items with multiple quantities in
        cart.'''
        cart = Cart(self._create_product_store())
        cart.add('apple', 2)
        cart.add('kitkat', 3)
        self.assertEqual(cart.get_total(), float('6.30'))


class CartItemTest(unittest.TestCase):

    def _create_product_store(self):
        '''Helper method to create populated ProductStore.'''
        products = [
            {"name": "apple" ,"price": 0.15},
            {"name": "ice cream" ,"price": 3.49},
            {"name": "dairy milk" ,"price": 2.00},
            {"name": "kitkat" ,"price": 0.70},
            ]
        return ProductStore(products)

    def test_get_line_total_is_float(self):
        '''Cart.get_line_total() returns a float.'''
        product_store = self._create_product_store()
        cartitem = CartItem('apple')
        self.assertTrue(
            type(round(cartitem.get_line_total(product_store), 2) is float))

    def test_quantity_on_create_with_no_value(self):
        '''Creating a CartItem without passing a quantity initialises quantity
        with 1.'''
        cartitem = CartItem('apple')
        self.assertEqual(cartitem.quantity, 1)

    def test_quantity_on_create_with_value(self):
        '''Creating a CartItem with a passed quantity initialises with that
        quantity.'''
        cartitem = CartItem('apple', 3)
        self.assertEqual(cartitem.quantity, 3)

    def test_get_line_total(self):
        '''Cart.get_line_total() returns the correct price for product.'''
        product_store = self._create_product_store()
        cartitem = CartItem('apple')
        self.assertEqual(
            round(cartitem.get_line_total(product_store), 2), float('0.15'))

    def test_get_line_total_multiple_quantity(self):
        '''get_line_total returns the correct price for item with multiple
        quantity.'''
        product_store = self._create_product_store()
        cartitem = CartItem('apple', 3)
        self.assertEqual(
            round(cartitem.get_line_total(product_store), 2), float('0.45'))


class ProductStoreTest(unittest.TestCase):

    def _create_product_store(self):
        '''Helper method to create populated ProductStore.'''
        products = [
            {"name": "apple" ,"price": 0.15},
            {"name": "ice cream" ,"price": 3.49},
            {"name": "dairy milk" ,"price": 2.00},
            {"name": "kitkat" ,"price": 0.70}
            ]
        return ProductStore(products)

    def test_get_product_price(self):
        '''ProductStore returns corresponding price for product.'''
        product_store = self._create_product_store()
        self.assertEqual(
            product_store.get_product_price('kitkat'), float('0.7'))

    def test_get_product_price_no_product(self):
        '''ProductStore raises exception when no product matches.'''
        product_store = self._create_product_store()
        self.assertRaises(NoSuchProductError, product_store.get_product_price, 'bike')

    def test_init_from_filepath(self):
        '''ProductStore object can be created from json file.'''
        json_file = os.path.abspath('test_products.json')
        product_store = ProductStore.init_from_filepath(json_file)
        self.assertEqual(len(product_store.items), 4)

    def test_item_after_init_from_filepath(self):
        '''An item's price can be retrieved from a ProductStore that's been
        created from a json file.'''
        json_file = os.path.abspath('test_products.json')
        product_store = ProductStore.init_from_filepath(json_file)
        self.assertEqual(
            product_store.get_product_price('apple'), float('0.15'))


class NoOfferTest(unittest.TestCase):

    '''Tests for the NoOffer offer class.'''

    def _create_product_store(self):
        '''Helper method to create populated ProductStore.'''
        products = [
            {"name": "apple" ,"price": 0.15},
            {"name": "ice cream" ,"price": 3.49},
            {"name": "dairy milk" ,"price": 2.00},
            {"name": "kitkat" ,"price": 0.70}
            ]
        return ProductStore(products)

    def test_nooffer_target(self):
        '''NoOffer's target is correctly assigned.'''
        no_offer_kitkat = NoOffer('kitkat')
        self.assertEqual(no_offer_kitkat.target_product, 'kitkat')

    def test_nooffer_total(self):
        '''NoOffer's calculate_line_total returns same value as cart item line
        total.'''
        product_store = self._create_product_store()
        no_offer_kitkat = NoOffer('kitkat')
        cartitem = CartItem('kitkat')
        self.assertEqual(cartitem.get_line_total(
            product_store), no_offer_kitkat.calculate_line_total(cartitem, product_store))


class BogofOfferTest(unittest.TestCase):

    def _create_product_store(self):
        '''Helper method to create populated ProductStore.'''
        products = [
            {"name": "apple" ,"price": 0.15},
            {"name": "ice cream" ,"price": 3.49},
            {"name": "dairy milk" ,"price": 2.00},
            {"name": "kitkat" ,"price": 0.70}
            ]
        return ProductStore(products)

    def test_bogof_one_item(self):
        '''Correct line total for item with 1 quantity.'''
        product_store = self._create_product_store()
        bogof_apples = MultiBuyOffer('apple', 1, 1)
        cartitem = CartItem('apple')
        self.assertEqual(round(bogof_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.15'))

    def test_bogof_one_item_two_quantity(self):
        '''Correct line total for item with 2 quantity.'''
        product_store = self._create_product_store()
        bogof_apples = MultiBuyOffer('apple', 1, 1)
        cartitem = CartItem('apple', 2)
        self.assertEqual(round(bogof_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.15'))

    def test_bogof_one_item_three_quantity(self):
        '''Correct line total for item with 3 quantity.'''
        product_store = self._create_product_store()
        bogof_apples = MultiBuyOffer('apple', 1, 1)
        cartitem = CartItem('apple', 3)
        self.assertEqual(round(bogof_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.30'))

    def test_bogof_one_item_four_quantity(self):
        '''Correct line total for item with 4 quantity.'''
        product_store = self._create_product_store()
        bogof_apples = MultiBuyOffer('apple', 1, 1)
        cartitem = CartItem('apple', 4)
        self.assertEqual(round(bogof_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.30'))

    def test_bogof_one_item_five_quantity(self):
        '''Correct line total for item with 5 quantity.'''
        product_store = self._create_product_store()
        bogof_apples = MultiBuyOffer('apple', 1, 1)
        cartitem = CartItem('apple', 5)
        self.assertEqual(round(bogof_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.45'))

    def test_bogof_one_item_six_quantity(self):
        '''Correct line total for item with 6 quantity.'''
        product_store = self._create_product_store()
        bogof_apples = MultiBuyOffer('apple', 1, 1)
        cartitem = CartItem('apple', 6)
        self.assertEqual(round(bogof_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.45'))


class BuyTwoGetThirdFreeOfferTest(unittest.TestCase):

    def _create_product_store(self):
        '''Helper method to create populated ProductStore.'''
        products = [
            {"name": "apple" ,"price": 0.15},
            {"name": "ice cream" ,"price": 3.49},
            {"name": "dairy milk" ,"price": 2.00},
            {"name": "kitkat" ,"price": 0.70}
            ]
        return ProductStore(products)

    def test_multibuy_one_item_buy_2_1_free(self):
        '''Correct line total for item with 1 quantity (buy 2 get 1 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 2, 1)
        cartitem = CartItem('apple')
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.15'))

    def test_multibuy_two_item_buy_2_1_free(self):
        '''Correct line total for item with 2 quantity (buy 2 get 1 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 2, 1)
        cartitem = CartItem('apple', 2)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.30'))

    def test_multibuy_three_item_buy_2_1_free(self):
        '''Correct line total for item with 3 quantity (buy 2 get 1 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 2, 1)
        cartitem = CartItem('apple', 3)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.30'))

    def test_multibuy_four_item_buy_2_1_free(self):
        '''Correct line total for item with 4 quantity (buy 2 get 1 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 2, 1)
        cartitem = CartItem('apple', 4)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.45'))

    def test_multibuy_five_item_buy_2_1_free(self):
        '''Correct line total for item with 5 quantity (buy 2 get 1 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 2, 1)
        cartitem = CartItem('apple', 5)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.60'))

    def test_multibuy_six_item_buy_2_1_free(self):
        '''Correct line total for item with 6 quantity (buy 2 get 1 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 2, 1)
        cartitem = CartItem('apple', 6)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.60'))

    def test_multibuy_seven_item_buy_2_1_free(self):
        '''Correct line total for item with 7 quantity (buy 2 get 1 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 2, 1)
        cartitem = CartItem('apple', 7)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.75'))


class MultiBuyOfferTest(unittest.TestCase):

    def _create_product_store(self):
        '''Helper method to create populated ProductStore.'''
        products = [
            {"name": "apple" ,"price": 0.15},
            {"name": "ice cream" ,"price": 3.49},
            {"name": "dairy milk" ,"price": 2.00},
            {"name": "kitkat" ,"price": 0.70}
            ]
        return ProductStore(products)

    def test_multibuy_one_item_buy_5_2_free(self):
        '''Correct line total for item with 1 quantity (buy 5 get 2 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 5, 2)
        cartitem = CartItem('apple')
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.15'))

    def test_multibuy_two_item_buy_5_2_free(self):
        '''Correct line total for item with 2 quantity (buy 5 get 2 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 5, 2)
        cartitem = CartItem('apple', 2)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.30'))

    def test_multibuy_three_item_buy_5_2_free(self):
        '''Correct line total for item with 3 quantity (buy 5 get 2 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 5, 2)
        cartitem = CartItem('apple', 3)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.45'))

    def test_multibuy_four_item_buy_5_2_free(self):
        '''Correct line total for item with 4 quantity (buy 5 get 2 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 5, 2)
        cartitem = CartItem('apple', 4)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.60'))

    def test_multibuy_five_item_buy_5_2_free(self):
        '''Correct line total for item with 5 quantity (buy 5 get 2 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 5, 2)
        cartitem = CartItem('apple', 5)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.75'))

    def test_multibuy_six_item_buy_5_2_free(self):
        '''Correct line total for item with 6 quantity (buy 5 get 2 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 5, 2)
        cartitem = CartItem('apple', 6)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.75'))

    def test_multibuy_seven_item_buy_5_2_free(self):
        '''Correct line total for item with 7 quantity (buy 5 get 2 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 5, 2)
        cartitem = CartItem('apple', 7)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.75'))

    def test_multibuy_eight_item_buy_5_2_free(self):
        '''Correct line total for item with 8 quantity (buy 5 get 2 free).'''
        product_store = self._create_product_store()
        multibuy_apples = MultiBuyOffer('apple', 5, 2)
        cartitem = CartItem('apple', 8)
        self.assertEqual(round(multibuy_apples.calculate_line_total(
            cartitem, product_store), 2), float('0.90'))


class DependentDiscountOfferTest(unittest.TestCase):

    def _create_product_store(self):
        '''Helper method to create populated ProductStore.'''
        products = [
            {"name": "apple" ,"price": 0.15},
            {"name": "ice cream" ,"price": 3.49},
            {"name": "dairy milk" ,"price": 2.00},
            {"name": "kitkat" ,"price": 0.70}
            ]
        return ProductStore(products)

    def test_one_without_dependent(self):
        '''One target product in the absence of its dependent product doesn't
        trigger discount.'''
        product_store = self._create_product_store()
        mars_snickers_20_discount = DependentDiscountOffer(
            'ice cream', 'dairy milk', float('0.2'))
        cart = Cart(product_store)
        mars_cartitem = cart.add('ice cream')
        self.assertEqual(round(mars_snickers_20_discount.calculate_line_total(
            mars_cartitem, product_store, cart), 2), float('3.49'))

    def test_one_with_one_dependent(self):
        '''One target product in the presence of one dependent product
        triggers discount.'''
        product_store = self._create_product_store()
        mars_snickers_20_discount = DependentDiscountOffer(
            'ice cream', 'dairy milk', float('0.2'))
        cart = Cart(product_store)
        mars_cartitem = cart.add('ice cream')
        cart.add('dairy milk')
        self.assertEqual(round(mars_snickers_20_discount.calculate_line_total(
            mars_cartitem, product_store, cart), 2), float('2.79'))

    def test_one_with_two_dependent(self):
        '''One target product in the presence of two dependent products
        triggers discount.'''
        product_store = self._create_product_store()
        mars_snickers_20_discount = DependentDiscountOffer(
            'ice cream', 'dairy milk', float('0.2'))
        cart = Cart(product_store)
        mars_cartitem = cart.add('ice cream')
        cart.add('dairy milk', 2)
        self.assertEqual(round(mars_snickers_20_discount.calculate_line_total(
            mars_cartitem, product_store, cart), 2), float('2.79'))

    def test_two_with_one_dependent(self):
        '''Two target product in the presence of one dependent product
        triggers discount.'''
        product_store = self._create_product_store()
        mars_snickers_20_discount = DependentDiscountOffer(
            'ice cream', 'dairy milk', float('0.2'))
        cart = Cart(product_store)
        mars_cartitem = cart.add('ice cream', 2)
        cart.add('dairy milk')
        self.assertEqual(round(mars_snickers_20_discount.calculate_line_total(
            mars_cartitem, product_store, cart), 2), float('6.28'))


class CartOffersTest(unittest.TestCase):

    '''Test Cart containing cart items with offers applied.'''

    def _create_product_store(self):
        '''Helper method to create populated ProductStore.'''
        products = [
            {"name": "apple" ,"price": 0.15},
            {"name": "ice cream" ,"price": 3.49},
            {"name": "dairy milk" ,"price": 2.00},
            {"name": "kitkat" ,"price": 0.70}
            ]
        return ProductStore(products)

    def test_get_total_with_one_offer(self):
        '''Cart get_total returns correct value with a bogof offer applied.'''
        product_store = self._create_product_store()
        bogof_kitkat = MultiBuyOffer('kitkat', 1, 1)
        cart = Cart(product_store)
        cart.add('kitkat', 2)
        cart.add('apple')
        self.assertEqual(
            cart.get_total(offers=[bogof_kitkat]), float('0.85'))

    def test_get_total_with_dependent_discount_offer(self):
        '''Cart get_total returns correct value with a dependent discount
        offer applied.'''
        product_store = self._create_product_store()
        kitkat_apple_20_discount = DependentDiscountOffer(
            'kitkat', 'apple', float('0.2'))
        cart = Cart(product_store)
        cart.add('kitkat', 2)
        cart.add('apple')
        self.assertEqual(
            round(cart.get_total(offers=[kitkat_apple_20_discount]), 2), float('1.41'))

    def test_get_total_with_two_offers_on_same_target(self):
        '''Cart get_total returns cheapest total when two offers are
        applicable for the same target.'''
        product_store = self._create_product_store()
        bogof_kitkat = MultiBuyOffer('kitkat', 1, 1)
        kitkat_apple_20_discount = DependentDiscountOffer(
            'kitkat', 'apple', float('0.2'))
        cart = Cart(product_store)
        cart.add('kitkat', 2)
        cart.add('apple')
        self.assertEqual(cart.get_total(
            offers=[bogof_kitkat, kitkat_apple_20_discount]), float('0.85'))
