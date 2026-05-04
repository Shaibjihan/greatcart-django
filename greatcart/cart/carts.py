from django.conf import settings

from .models import Coupon
from product.models import Product


class Cart(object):
    def __init__(self, request) ->None:
        self.session = request.session
        self.cart_id = settings.CART_ID
        self.coupon_id = settings.COUPON_ID
        cart = self.session.get(self.cart_id)
        coupon = self.session.get(self.coupon_id)
        self.cart =self.session [self.cart_id] = cart if  cart else {}
        self.coupon =self.session [self.coupon_id] = coupon if  coupon else None


    def update(self, product_id, quantity=1):
        product = Product.objects.get(id=product_id)
        self.session[self.cart_id].setdefault(str(product_id), {"quantity": 0})
        updated_quantity = self.session[self.cart_id][str(product_id)]['quantity'] + quantity
        self.session[self.cart_id][str(product_id)]['quantity'] = updated_quantity
        self.session[self.cart_id][str(product_id)]['subtotal'] = updated_quantity  * float(product.price)

        if updated_quantity < 1:
            del  self.session[self.cart_id] [str(product_id)]
        
        self.save()

    def add_coupon(self, coupon_id):
        self.session[self.coupon_id] = coupon_id
        self.save()


    def __iter__(self):
        products = Product.objects.filter(id__in=list(self.cart.keys()))
        cart = self.cart.copy()

        for item in products:
            product = Product.objects.get(id=item.id)
            cart[str(item.id)]['product'] = {
                "id":item.id,
                "title":item.title,
                "category": item.category.title,
                "price": float(item.price),
                "thumbnail":item.thumbnail,
                "slug": item.slug,
            }
            yield cart[str(item.id)]

    def save (self):
        self.session.modified = True
        
    def __len__(self):
        return len(list(self.cart.keys()))
    
    def clear (self):
        try:
            del self.session[self.cart_id]
            del self.session[self.coupon_id]
        except:
            pass
        self.save()



    def restore_after_logout(self, cart=None, coupon=None):
        if cart is None:
            cart = {}
        self.cart = self.session[self.cart_id] = cart
        self.coupon = self.session[self.coupon_id] = coupon
        self.save()

        # def restore_after_logout(self, cart={}, coupon=None):
        #     self.cart = self.session[self.cart_id] =cart
        #     self.coupon = self.session[self.coupon_id] = coupon
        #     self.save()


    def total(self):
        amount = sum (product['subtotal'] for product in self.cart.values())

        if self.coupon:
            coupon = Coupon.objects.get(id=self.coupon)
            amount -= amount * (coupon.discount / 100)
            
        return amount
        


#  # Another  way
# from django.conf import settings
# from product.models import Product

# class Cart(object):
#     def __init__(self, request) -> None:
#         self.session = request.session
#         self.cart_id = settings.CART_ID
#         cart = self.session.get(self.cart_id)
#         if not cart:
#             cart = self.session[self.cart_id] = {}
#         self.cart = cart

#     def update(self, product_id, quantity=1):
#         product = Product.objects.get(id=product_id)
#         product_id_str = str(product_id)

#         # 1. Update self.cart directly (it's linked to the session)
#         self.cart.setdefault(product_id_str, {"quantity": 0})
#         updated_quantity = self.cart[product_id_str]['quantity'] + quantity
#         self.cart[product_id_str]['quantity'] = updated_quantity
        
#         # We handle subtotal in the __iter__ method to keep session data small
#         if updated_quantity < 1:
#             del self.cart[product_id_str]
        
#         self.save()

#     def __iter__(self):
#         product_ids = self.cart.keys()
#         # Fetch actual product objects from database
#         products = Product.objects.filter(id__in=product_ids)
        
#         cart_copy = self.cart.copy()

#         for product in products:
#             # Match the database product with the session data
#             item = cart_copy[str(product.id)]
            
#             # This allows you to use 'item.product' in HTML
#             item['product'] = product 
            
#             # This allows you to use 'item.subtotal' in HTML
#             item['subtotal'] = float(product.price) * item['quantity']
            
#             yield item


#     def save(self):
#         self.session.modified = True
        
#     def __len__(self):
#         # Counts the total number of items (e.g., 2 shirts + 1 hat = 3)
#         return sum(item['quantity'] for item in self.cart.values())
