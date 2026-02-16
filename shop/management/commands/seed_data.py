from django.core.management.base import BaseCommand
from shop.models import Product, Denomination
from decimal import Decimal


class Command(BaseCommand):
    help = "Seed initial products and denominations"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding data..."))
        products = [
            {
                "name": "Rice Bag",
                "product_id": "P001",
                "available_stocks": 50,
                "price": Decimal("1200.00"),
                "tax_percentage": Decimal("5.00"),
            },
            {
                "name": "Sugar Pack",
                "product_id": "P002",
                "available_stocks": 100,
                "price": Decimal("45.00"),
                "tax_percentage": Decimal("2.00"),
            },
            {
                "name": "Milk Packet",
                "product_id": "P003",
                "available_stocks": 200,
                "price": Decimal("25.00"),
                "tax_percentage": Decimal("1.00"),
            },
        ]

        for p in products:
            obj, created = Product.objects.get_or_create(
                product_id=p["product_id"],
                defaults=p,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added product {obj.name}"))
            else:
                self.stdout.write(f"Product {obj.name} already exists")

        denomination_values = [500, 200, 100, 50, 20, 10, 5, 2, 1]

        for value in denomination_values:
            obj, created = Denomination.objects.get_or_create(value=value)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added denomination ₹{value}"))
            else:
                self.stdout.write(f"Denomination ₹{value} already exists")

        self.stdout.write(self.style.SUCCESS("✅ Seeding completed."))
