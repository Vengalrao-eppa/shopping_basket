Shopping Cart Programming Exercise
===

## ProductStore

Products are stored in a `ProductStore` object. 
This can either be created from a list of product dictionaries or initialized from a JSON file.

```python
from product import ProductStore

products = [
	{"name": "Baked Beans" ,"price": 0.99},
	{"name": "Biscuits" ,"price": 1.2},
	{"name": "Sardines" ,"price": 1.89},
	{"name": "Shampoo Small" ,"price": 2},
	{"name": "Shampoo Medium" ,"price": 2.5},
	{"name": "Shampoo Large" ,"price": 3.5}
]

product_store = ProductStore(products)

# or

import os

json_path = os.path.abspath('products.json')
product_store = ProductStore.init_from_filepath(json_path)
```

`get_product_price()` - Returns the price of the product

```python
price = product_store.get_product_price('product')
```

## Cart

Carts should be created with a ProductStore instance from which the cart can derive prices.

```python
from cart import Cart

my_cart = Cart(product_store)
```

Products can be added to a cart by name

```python
cart.add('apple')
cart.add('strawberries', 3)
```

The total for the cart can be calculated with `get_total()`. This method optionally takes a list of [Offer](#offers) objects that are applied to items in the cart when calculating the total.

```python
total = cart.get_total()

# with offers
total_with_offers = cart.get_total(offers=[offer_one, offer_two, offer_three])
```

## Offers

Offer classes inherit from `AbstractOffer` and must implement the `calculate_line_total()` method.

Two example offer classes are provided; `MultiBuyOffer`, and `DependentDiscountOffer`.


### MultiBuyOffer

But a certain quantity of products and get one free

```python
# buy one get one free on strawberries
buy_one_free = MultiBuyOffer(product, 1, 1)

# buy two get third free on product
multibuy = MultiBuyOffer(product, 2, 1)
```

### DependentDiscountOffer

Discount can be applied to a product on purchase of another product.

```python
dep_discount_offer = DependentDiscountOffer('snickers bar', 'mars bar', Decimal('0.2'))
```
