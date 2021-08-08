from django.urls    import path
from orders.views import OrderView, PurchaseView, CartView

urlpatterns = [
    path('/<int:item_id>', OrderView.as_view()),
    path('', OrderView.as_view()),
    path('/purchase', PurchaseView.as_view()),
    path('/cart', CartView.as_view()),
]