from decimal import Decimal
from .repositories import (
    ProductRepository,
    PurchaseRepository,
    PurchaseItemRepository,
    DenominationRepository,
)
from .builders import BillBuilder
from .factories import ChangeFactory
from .models import DenominationCount

class BillingService:
    @staticmethod
    def generate_bill(customer_email, items_data, paid_amount):
        builder = BillBuilder()

        # Build bill
        for pid, qty in items_data:
            product = ProductRepository.get_by_product_id(pid)
            builder.add_item(product, int(qty))

        bill = builder.build()

        # Save purchase
        purchase = PurchaseRepository.create(
            customer_email=customer_email,
            total_amount=bill["rounded_total"],
            paid_amount=Decimal(paid_amount),
        )
        
        purchase.customer_email = customer_email
        purchase.save()

        # Save items
        for item in bill["items"]:
            PurchaseItemRepository.create(
                purchase=purchase,
                product=item["product"],
                quantity=item["qty"],
                unit_price_with_tax=item["unit_price"],  # Store base unit price
            )

        # Balance calculation
        balance = Decimal(paid_amount) - bill["rounded_total"]
        
        # Only calculate change if balance is positive
        if balance > 0:
            denominations = DenominationRepository.all_desc()
            change = ChangeFactory.calculate(balance, denominations)
            
            # Save denomination counts
            for denom_value, count in change:
                denomination = denominations.get(value=denom_value)
                DenominationCount.objects.create(
                    purchase=purchase,
                    denomination=denomination,
                    count=count
                )
        else:
            change = []

        bill["balance"] = balance
        bill["change"] = change
        bill["purchase"] = purchase

        return bill