from ecommercial.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists.
        cart = self.session.get('session_key')

        # If thr user is new, no session key Create one.
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of the site.
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Logic.
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True


    def cart_total(self):
        product_ids = self.cart.keys()
        # Look up those keys in our products database model.
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities.
        quantities = self.cart
        # Start counting at 0.
        total = 0
        for key, value in quantities.items():
            # Convert key string into int so we can...
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

                return total


    def __len__(self):
        return len(self.cart)


    def get_prods(self):
        # Get ids fro cart.
        product_ids = self.cart.keys()

        # Use ids to look up products in database model.
        products = Product.objects.filter(id__in=product_ids)
        return products


    def get_quants(self):
        quantities =self.cart
        return quantities



    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # Get our cart.
        ourcart = self.cart
        # Update Dictionary/cart.
        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing


    def delete(self, product):
        product_id = str(product)
        # Delete from cart.
        if product_id in self.cart:
            del self.cart[product_id]

            self.session.modified = True