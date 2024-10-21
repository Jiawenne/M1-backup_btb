from django.core.management.base import BaseCommand
from monTiGMagasin.models import InfoProduct
from monTiGMagasin.serializers import InfoProductSerializer
from monTiGMagasin.config import baseUrl
import requests
import time
from django.db import connection

class Command(BaseCommand):
    help = 'Refresh the list of products from TiG server.'

    def handle(self, *args, **options):
        self.stdout.write('[' + time.ctime() + '] Refreshing data...')
        # Supprimer tous les produits
        InfoProduct.objects.all().delete()
        
        # Réinitialiser l'auto-incrémentation de l'ID
        with connection.cursor() as cursor:
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'monTiGMagasin_infoproduct';")
        
        
        # Obtenir les données des produits depuis l'API TiG
        response = requests.get(baseUrl + 'products/')
        jsondata = response.json()

        for product in jsondata:
            # Chercher un produit avec le même tig_id dans la base de données
            existing_product = InfoProduct.objects.filter(tig_id=product['id']).first()
            
            # Si le produit existe, on le met à jour
            if existing_product:
                serializer = InfoProductSerializer(existing_product, data={
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
                action = 'updated'
            # Si le produit n'existe pas, on le crée
            else:
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
                action = 'created'

            if serializer.is_valid():
                serializer.save()
                self.stdout.write(self.style.SUCCESS(f"[{time.ctime()}] Successfully {action} product id='{product['id']}'"))
            else:
                self.stdout.write(self.style.ERROR(f"[{time.ctime()}] Validation Error for product id='{product['id']}': {serializer.errors}"))

        self.stdout.write('[' + time.ctime() + '] Data refresh terminated.')
