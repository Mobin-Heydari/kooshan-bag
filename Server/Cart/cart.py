from Products.models import Product



# Cart Session Id
CART_SESSION_ID = "Cart"


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
    
    def unique_id_generator(self, product_id, color):
        result = f'{product_id}--{color}'
        return result
    
    def add(self, product, color, price, quantity=1):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        unique_id = self.unique_id_generator(product_id, color)
        if unique_id not in self.cart:
            self.cart[unique_id] = {
                'price' : str(price),
                'product_id' : product_id,
                'quantity' : quantity,
                'color' : str(color)
            }
        else:
            self.cart[unique_id]['quantity'] += int(quantity)
        self.save()
        
    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True
        
                  
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(pk=int(item['product_id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * int(item['price'])
            item['unique_id'] = self.unique_id_generator(
                product_id = product.id,
                color = item['color']
            )
            yield item
    
    def cart_len(self):
        """
        Count all items in the cart.
        """
        return sum(int(item['quantity']) for item in self.cart.values())


    def get_total_price(self):
        return sum(int(item['price']) for item in self.cart.values())
    
    
    def remove(self, unique_id):
        if unique_id in self.cart:
            del self.cart[unique_id]
            self.save()
    
    def clear(self):
        # remove cart from session
        del self.session[CART_SESSION_ID]
        self.save()