from django.shortcuts import render, get_object_or_404, redirect
from .models import Purchase, Product, Denomination
from .services import BillingService
from decimal import Decimal


def billing_page(request):
    products = Product.objects.all()
    denominations = Denomination.objects.all().order_by("-value")
    
    if request.method == "POST":
        # Collect items
        items = []
        i = 0
        while request.POST.get(f"product_{i}"):
            product_id = request.POST.get(f"product_{i}")
            qty = request.POST.get(f"qty_{i}")

            if product_id and qty:
                items.append((product_id, int(qty)))
                print(f"Item {i}: {product_id}, qty: {qty}")

            i += 1

        print(f"Total items collected: {len(items)}")

        # Generate bill
        bill = BillingService.generate_bill(
            customer_email=request.POST.get("email"),
            items_data=items,
            paid_amount=request.POST.get("paid_amount"),
        )

        # Redirect to bill page
        return redirect("bill_detail", purchase_id=bill["purchase"].id)

    return render(request, "billing.html", {
        "products": products,
        "denominations": denominations,
    })


def bill_detail(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)

    items = []
    total_without_tax = Decimal("0")
    total_tax = Decimal("0")

    for pi in purchase.items.all():
        # Unit price (base price without tax)
        unit_price = pi.product.price
        
        # Purchase price = unit price * quantity (without tax)
        purchase_price = unit_price * pi.quantity
        
        # Tax percentage
        tax_percent = pi.product.tax_percentage
        
        # Tax amount = purchase price * tax percentage / 100
        tax_amount = (purchase_price * tax_percent) / Decimal("100")
        
        # Line total = purchase price + tax
        line_total = purchase_price + tax_amount

        items.append({
            "product": pi.product,
            "qty": pi.quantity,
            "unit_price": unit_price,
            "purchase_price": purchase_price,
            "tax_percent": tax_percent,
            "tax_amount": tax_amount,
            "line_total": line_total,
        })

        total_without_tax += purchase_price
        total_tax += tax_amount

    net_total = total_without_tax + total_tax
    rounded_total = purchase.total_amount
    balance = purchase.paid_amount - rounded_total
    
    # Get change from denomination counts
    change = [(dc.denomination.value, dc.count) 
              for dc in purchase.denomination_counts.all().select_related('denomination').order_by('-denomination__value')]

    context = {
        "purchase": purchase,
        "items": items,
        "total_without_tax": total_without_tax,
        "total_tax": total_tax,
        "net_total": net_total,
        "rounded_total": rounded_total,
        "balance": balance,
        "change": change,
    }

    return render(request, "bill_detail.html", context)


def customer_purchases(request):
    """View to search and list all purchases by customer email"""
    purchases = []
    search_email = None
    
    if request.method == "POST":
        search_email = request.POST.get("email")
        if search_email:
            purchases = Purchase.objects.filter(
                customer_email__iexact=search_email
            ).order_by('-created_at')
    
    context = {
        "purchases": purchases,
        "search_email": search_email,
    }
    
    return render(request, "customer_purchases.html", context)


def purchase_detail(request, purchase_id):
    """View to show detailed information about a specific purchase"""
    purchase = get_object_or_404(Purchase, id=purchase_id)

    items = []
    total_without_tax = Decimal("0")
    total_tax = Decimal("0")

    for pi in purchase.items.all():
        # Unit price (base price without tax)
        unit_price = pi.product.price
        
        # Purchase price = unit price * quantity (without tax)
        purchase_price = unit_price * pi.quantity
        
        # Tax percentage
        tax_percent = pi.product.tax_percentage
        
        # Tax amount = purchase price * tax percentage / 100
        tax_amount = (purchase_price * tax_percent) / Decimal("100")
        
        # Line total = purchase price + tax
        line_total = purchase_price + tax_amount

        items.append({
            "product": pi.product,
            "qty": pi.quantity,
            "unit_price": unit_price,
            "purchase_price": purchase_price,
            "tax_percent": tax_percent,
            "tax_amount": tax_amount,
            "line_total": line_total,
        })

        total_without_tax += purchase_price
        total_tax += tax_amount

    net_total = total_without_tax + total_tax
    rounded_total = purchase.total_amount
    balance = purchase.paid_amount - rounded_total
    
    # Get change from denomination counts
    change = [(dc.denomination.value, dc.count) 
              for dc in purchase.denomination_counts.all().select_related('denomination').order_by('-denomination__value')]

    context = {
        "purchase": purchase,
        "items": items,
        "total_without_tax": total_without_tax,
        "total_tax": total_tax,
        "net_total": net_total,
        "rounded_total": rounded_total,
        "balance": balance,
        "change": change,
    }

    return render(request, "purchase_detail.html", context)