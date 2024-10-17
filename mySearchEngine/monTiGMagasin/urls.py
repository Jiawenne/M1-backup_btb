from django.urls import path
from monTiGMagasin import views

urlpatterns = [
    path('infoproducts/', views.InfoProductList.as_view()),
    path('infoproduct/<int:id>/', views.InfoProductDetail.as_view()),
    path('putonsale/<int:id>/<str:newprice>/', views.PutOnSale.as_view()),
    path('removesale/<int:id>/', views.RemoveSale.as_view()),
    path('incrementStock/<int:id>/<int:number>/', views.IncrementStock.as_view()),
    path('decrementStock/<int:id>/<int:number>/', views.DecrementStock.as_view()),
]
    