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

product_store = ProductStore.load_products(json_products_file)
```

`get_product_price()` to get the product price
```python
price = product_store.get_product_price('product')
```

## Cart

Carts can be created by passing the ProductStore Instance as an argument

```python
from cart import Cart

my_cart = Cart(product_store)
```

Products can be added to a cart by name

```python
cart.add('Biscuits')
cart.add('Sardines', 3)
```

`get_total()` to get the cart total
Also a list of Offer Class objects can be passed to the method to apply offers on Cart total

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
Discount can also be applied on a single product 

```python
dep_discount_offer = DependentDiscountOffer('snickers bar', 'mars bar', Decimal('0.2'))
discount_product = DependentDiscountOffer('snickers bar', 'snickers bar', Decimal('0.2'))
```

To run unittest cases for the shopping cart, run the below command from command prompt
``` python -m unittest tests.py ```
