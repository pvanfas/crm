from rest_framework import serializers
from sales.models import Sale, SaleItem


class SaleSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    sale_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Sale
        fields = ['id','customer','customer_name','date','sale_items','subtotal','discount','total']
    
    def get_customer_name(self,instance):
        if instance.customer:
            return instance.customer.name
        else:
            return ""
            
    def get_sale_items(self,instance):
        items = SaleItem.objects.filter(sale=instance)
        serialized = SaleItemSerializer(items,many=True)
        return serialized.data    

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = SaleItem
        fields = ['id','product','product_name','product_price','qty','subtotal',]
    
    def get_product_name(self,instance):
        if instance.product:
            return instance.product.name
        else:
            return ""
    
    def get_product_price(self,instance):
        if instance.product:
            return instance.product.price
        else:
            return ""
                
    def get_subtotal(self,instance):
        if instance.product:
            return instance.product.price * instance.qty
        else:
            return 0