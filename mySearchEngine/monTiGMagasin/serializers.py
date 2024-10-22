from rest_framework.serializers import ModelSerializer, SerializerMethodField
from monTiGMagasin.models import InfoProduct
from monTiGMagasin.models import Transaction

class InfoProductSerializer(ModelSerializer):
    class Meta:
        model = InfoProduct
        fields = ('id','tig_id', 'name', 'category', 'price', 'unit', 'availability', 'sale', 'discount', 'comments', 'owner', 'quantityInStock','discount_price')
class TransactionSerializer(ModelSerializer):
    category = SerializerMethodField()
    discount = SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('id', 'quantity', 'price', 'date', 'sale_type', 'product', 'sale_type', 'category', 'discount')

    def get_category(self, obj):
        return obj.product.category
    
    def get_discount(self, obj):
        return obj.product.discount