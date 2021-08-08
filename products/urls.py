from django.urls    import path
from products.views import PageView

urlpatterns = [
    path('', PageView.as_view()),
]