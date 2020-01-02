from rest_framework import routers, serializers, viewsets
from sales.models import Sale, SaleItem


class SaleSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    sale_items = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id','customer','customer_name','date','sub_total','discount','total','sale_items']

    def get_customer_name(self, instance):
        if instance.customer:
            return instance.customer.name
        else:
            return ""

    def get_sale_items(self, instance):
        items = SaleItem.objects.filter(sale=instance)
        serialized = SaleItemSerializer(items,many=True)
        return serialized.data


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = SaleItem
        fields = ['id','product','product_name','qty','sub_total','product_price']

    def get_product_name(self, instance):
        if instance.product:
            return instance.product.name
        else:
            return ""

    def get_product_price(self, instance):
        if instance.product:
            return instance.product.price
        else:
            return ""

    def get_sub_total(self, instance):
        if instance.product:
            return instance.product.price * instance.qty
        else:
            return 0
