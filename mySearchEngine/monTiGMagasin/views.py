from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from monTiGMagasin.config import baseUrl
from monTiGMagasin.models import InfoProduct
from monTiGMagasin.serializers import InfoProductSerializer
from monTiGMagasin.models import Transaction
from monTiGMagasin.serializers import TransactionSerializer
from django.db.models import F

# Create your views here.
class InfoProductList(APIView):
    def get(self, request, format=None):
        products = InfoProduct.objects.all()
        serializer = InfoProductSerializer(products, many=True)
        return Response(serializer.data)

class InfoProductDetail(APIView):
    def get_object(self, id):
        try:
            return InfoProduct.objects.get(pk=id)
        except InfoProduct.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        product = self.get_object(id)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)

class PutOnSale(APIView):
    def get_object(self, id):
        try:
            return InfoProduct.objects.get(pk=id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def put(self, request, id, newprice, format=None):
        product = self.get_object(id)
        product.sale = True
        try:
            product.discount = float(newprice)
        except ValueError:
            return Response({"error": "Invalid price format"}, status=400)
        product.save()
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)

class RemoveSale(APIView):
    def get_object(self, id):
        try:
            return InfoProduct.objects.get(pk=id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        product = self.get_object(id)
        product.sale = False
        product.save()
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)

class IncrementStock(APIView):
    def get_object(self, id):
        try:
            return InfoProduct.objects.get(pk=id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, id, number, format=None):
        product = self.get_object(id)
        product.quantityInStock += int(number)
        product.save()
        update_product_promotion(product)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)

class DecrementStock(APIView):
    def get_object(self, id):
        try:
            return InfoProduct.objects.get(pk=id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, id, number, format=None):
        product = self.get_object(id)
        print(product.quantityInStock)
        print(number)
        if product.quantityInStock < int(number):
            return Response({"error": "Not enough stock"}, status=400)
        product.quantityInStock = max(0, product.quantityInStock - int(number))
        product.save()
        update_product_promotion(product)
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)

def update_product_promotion(product):
    if product.quantityInStock > 16:
        product.sale = True
        if 16 < product.quantityInStock <= 64:
            product.discount = product.price * 0.8
        else:
            product.discount = product.price * 0.5
    else:
        product.sale = False
        product.discount = 0
    product.save()

class TransactionList(APIView):
    def get_queryset(self):
        return Transaction.objects.all()

    def get(self, request, format=None):
        transactions = self.get_queryset()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
class TransactionView(APIView):
    def get_object(self, id):
        try:
            return InfoProduct.objects.get(pk=id)
        except InfoProduct.DoesNotExist:
            raise Http404

    def get(self, request, id, sale_type, number, format=None):
        product = self.get_object(id)
        number = int(number)
        
        if sale_type == 'purchase':
            self.increment_stock(product, number)
        elif sale_type in ['sale', 'unsold']:
            self.decrement_stock(product, number, sale_type)
        else:
            return Response({"error": "Invalid sale type"}, status=400)
        
        serializer = InfoProductSerializer(product)
        return Response(serializer.data)

    def increment_stock(self, product, number):
        product.quantityInStock += number
        product.save()
        self.create_transaction(product, number, product.price, 'purchase')
        update_product_promotion(product)

    def decrement_stock(self, product, number, sale_type):
        if product.quantityInStock < number:
            raise Http404("Not enough stock")
        product.quantityInStock = max(0, product.quantityInStock - number)
        product.save()
        price = 0 if sale_type == 'unsold' else product.price
        self.create_transaction(product, number, price, sale_type)
        update_product_promotion(product)

    def create_transaction(self, product, quantity, price, sale_type):
        Transaction.objects.create(
            quantity=quantity,
            price=price,
            sale_type=sale_type,
            product=product
        )