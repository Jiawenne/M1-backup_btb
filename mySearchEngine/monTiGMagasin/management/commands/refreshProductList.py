from django.core.management.base import BaseCommand
from monTiGMagasin.models import InfoProduct
from monTiGMagasin.serializers import InfoProductSerializer
import requests
import time
from django.db import transaction

class Command(BaseCommand):
    help = 'Refresh  '

    def handle(self, *args, **options):
        self.stdout.write(f"[{time.ctime()}] refreshing")
        
        try:
            response = requests.get('http://51.255.166.155:1352/tig/products/')
            response.raise_for_status()  # 如果响应状态码不是200，将引发异常
            jsondata = response.json()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"[{time.ctime()}] error: {str(e)}"))
            return
        except ValueError as e:
            self.stderr.write(self.style.ERROR(f"[{time.ctime()}] JSON error: {str(e)}"))
            self.stderr.write(f"reponse: {response.text}")
            return

        with transaction.atomic():
            InfoProduct.objects.all().delete()
            for product in jsondata:
                serializer = InfoProductSerializer(data={
                    'tig_id': str(product['id']),
                    'name': str(product['name']),
                    'category': str(product['category']),
                    'price': str(product['price']),
                    'unit': str(product['unit']),
                    'availability': str(product['availability']),
                    'sale': str(product['sale']),
                    'discount': str(product['discount']),
                    'comments': str(product['comments']),
                    'owner': str(product['owner']),
                    'quantityInStock': '0',
                })
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(self.style.SUCCESS(f"[{time.ctime()}] success add product id='{product['id']}'"))
                else:
                    self.stderr.write(self.style.WARNING(f"[{time.ctime()}] success add product id='{product['id']}': {serializer.errors}"))

        self.stdout.write(f"[{time.ctime()}] ")
