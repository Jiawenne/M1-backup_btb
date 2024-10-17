from django.core.management.base import BaseCommand
from monTiGMagasin.models import InfoProduct
from monTiGMagasin.views import update_product_promotion

class Command(BaseCommand):
    help = 'Updates promotions for all products'

    def handle(self, *args, **options):
        products = InfoProduct.objects.all()
        for product in products:
            update_product_promotion(product)
        self.stdout.write(self.style.SUCCESS('Successfully updated promotions'))

