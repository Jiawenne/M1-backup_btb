from rest_framework.serializers import ModelSerializer
from monTiGMagasin.models import InfoProduct

class InfoProductSerializer(ModelSerializer):
    class Meta:
        model = InfoProduct
        fields = ('id', 'name', 'category', 'price', 'unit', 'availability', 'sale', 'discount', 'comments', 'owner', 'quantityInStock')
