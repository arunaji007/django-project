from decimal import Decimal


class BillBuilder:
    def __init__(self):
        self.items = []
        self.total_without_tax = Decimal("0")
        self.total_tax = Decimal("0")

    def add_item(self, product, qty):
        # Base price (unit price without tax)
        unit_price = product.price
        
        # Tax percentage
        tax_percent = product.tax_percentage
        
        # Purchase price = unit price * quantity (without tax)
        purchase_price = unit_price * qty
        
        # Tax amount = purchase price * tax percentage / 100
        tax_amount = (purchase_price * tax_percent) / Decimal("100")
        
        # Total price for this line item = purchase price + tax
        line_total = purchase_price + tax_amount

        self.total_without_tax += purchase_price
        self.total_tax += tax_amount

        self.items.append({
            "product": product,
            "qty": qty,
            "unit_price": unit_price,
            "purchase_price": purchase_price,
            "tax_percent": tax_percent,
            "tax_amount": tax_amount,
            "line_total": line_total,
        })
        return self

    def build(self):
        net = self.total_without_tax + self.total_tax
        rounded = int(net)  # Round down to nearest integer

        return {
            "items": self.items,
            "total_without_tax": self.total_without_tax,
            "total_tax": self.total_tax,
            "net_total": net,
            "rounded_total": Decimal(rounded),
        }