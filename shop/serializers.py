from rest_framework import serializers


class BillingItemSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)



class BillingSerializer(serializers.Serializer):
    customer_email = serializers.EmailField()
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    items = BillingItemSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required.")
        return value