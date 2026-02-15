from .models import Product, Purchase, PurchaseItem, Denomination


class ProductRepository:
    @staticmethod
    def get_by_product_id(pid: str) -> Product:
        return Product.objects.get(product_id=pid)


class PurchaseRepository:
    @staticmethod
    def create(customer_email, total_amount, paid_amount):
        return Purchase.objects.create(
           customer_email=customer_email,
            total_amount=total_amount,
            paid_amount=paid_amount,
        )


class PurchaseItemRepository:
    @staticmethod
    def create(**kwargs):
        return PurchaseItem.objects.create(**kwargs)


class DenominationRepository:
    @staticmethod
    def all_desc():
        return Denomination.objects.all().order_by("-value")
