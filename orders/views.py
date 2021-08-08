import json

from django.http      import JsonResponse
from django.views     import View
from django.db        import transaction
from django.db.models import Q, F

from products.models  import Item
from orders.models    import Order, OrderItem, Location, Cart
from users.models     import Member
from users.utils      import login

class OrderView(View):
    @login
    @transaction.atomic
    def post(self, request, item_id):
        data = json.loads(request.body)
        
        if Order.objects.filter(member_id = request.user.id, status_id = 1).exists():
            Order.objects.filter(member_id = request.user.id, status_id = 1).delete()

        order = Order.objects.create(member_id = request.user.id, status_id = 1, location_id = None)

        OrderItem.objects.create(
            item_id              = item_id,
            order_id             = order.id,
            order_item_status_id = 1,
            quantity             = data['quantity']
        )
        return JsonResponse({'MESSAGE': "SUCCESS"}, status=201)

    @login
    def get(self, request):
        order_id    = Order.objects.get(member_id=request.user.id, status_id =1).id
        order_items = OrderItem.objects.filter(order_id=order_id) 
        
        result = [
            {
        "order_number" : order_item.order_id,
        "quantity"     : order_item.quantity,
        "name"         : request.user.name,
        "phone_number" : request.user.phone_number,
        "address"      : request.user.address,
        "information"  : [
            {
            "product_name"     : order_item.item.name,
            "product_image"    : order_item.item.image_set.get(main=1).image_url,
            "product_price"    : order_item.item.price,
            "product_discount" : order_item.item.discount   
            }
            ]
        }
        for order_item in order_items]
        
        return JsonResponse({'RESULT': result}, status=200)


class PurchaseView(View):
    @login
    @transaction.atomic
    def post(self, request):
        try:
            data   = json.loads(request.body)
            member = Member.objects.get(id=request.user.id)
            if member.points < data['total_price']:
                return JsonResponse({"MESSAGE":"INSUFFICIENT_POINTS"}, status=400)

            location=Location.objects.create(
                name         = data['name'],
                phone_number = data['phone_number'],
                email        = data.get('email', None),
                address      = data['address'],
                content      = data.get('content', None)
            )
            
            member.points = member.points - data['total_price']
            member.save()            

            order             = Order.objects.get(id=data['order_id'])
            order.location_id = location.id
            order.status_id   = 2
            order.save()

            order_items = OrderItem.objects.filter(order_id=data['order_id']) 
            for order_item in order_items:
                order_item.order_item_status_id = 2
                item                            = Item.objects.get(id=order_item.item_id)
                item.order_quantity             += order_item.quantity
                item.stock                      -= order_item.quantity               
                order_item.save()
                item.save()

            return JsonResponse({'MESSAGE': "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)


class CartView(View):
    @login
    def post(self, request):
        try:
            data = json.loads(request.body)
            member = Member.objects.get(id=request.user.id)

            if Cart.objects.filter(Q(item_id = data['item_id'])&Q(member=member)).exists():
                return JsonResponse({"MESSAGE":"CART_EXIST"}, status=400)
            
            if data['quantity'] > Item.objects.get(id = data['item_id']).stock:
                return JsonResponse({"MESSAGE":"NO_STOCK"}, status=400)
                
            Cart.objects.create(item_id=data['item_id'], member = member, quantity = data['quantity'])
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

    @login
    def get(self, request):
        member = Member.objects.get(id=request.user.id)
        if not Cart.objects.filter(member=member).exists():
                return JsonResponse({"MESSAGE":"EMPTY_CART"}, status=400)

        carts = Cart.objects.filter(member = member)

        results = [{
            "cart_id" : cart.id,
            "item_id" : cart.item.id,
            "quantity" : cart.quantity,
            "name"    : cart.item.name,
            "image"   : cart.item.image_set.get(main=1).image_url,
            "price"   : cart.item.price,
            "discount" : cart.item.discount
        } for cart in carts]

        return JsonResponse({"RESULT" : results}, status=201)

    @login
    def patch(self, request):
        is_cart = request.GET.get("is_cart", None)
        item_id = request.GET.get("item_id", None)
        quantities = request.GET.getlist("quantity", None)
        carts_id = request.GET.getlist("cart_id", None)

        member = Member.objects.get(id=request.user.id)

        if not is_cart:
            cart = Cart.objects.get(Q(item_id = item_id) & Q(member = member))
            if cart.item.stock < cart.quantity + int(quantities[0]):
                return JsonResponse({"MESSAGE":"NO_STOCK"}, status=400)

            cart.quantity = F('quantity') + int(quantities[0])
            cart.save()
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
        
        for i in range(len(carts_id)):
            cart = Cart.objects.get(id=carts_id[i])
            if cart.item.stock < int(quantities[i]):
                return JsonResponse({"MESSAGE":"NO_STOCK"}, status=400)
            
            cart.quantity = int(quantities[i])
            cart.save()
        
        return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

    @login
    def delete(self, request):
        is_all = request.GET.get("is_all", None)
        cart_id = request.GET.get("cart_id", None)

        if not is_all:
            Cart.objects.get(id = cart_id).delete()
            return JsonResponse({"MESSAGE" : "DELETE"}, status=200)

        member = Member.objects.get(id = request.user.id)

        Cart.objects.filter(member = member).delete()
        return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

