from products.models import Product


def update_stock(pk, qty, status):
    product = Product.objects.get(pk=pk)
    stock = product.stock
    if status == "increase":
        balance_stock = stock + qty
    elif status == "decrease":
        balance_stock = stock - qty

    product.stock = balance_stock
    product.save()
