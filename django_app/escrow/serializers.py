from rest_framework import serializers
from .models import Advertisement, AdvertisementApplication, Escrow

class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer to display advertisement details along with the number of applicants"""
    applicant_count = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ['id', 'seller', 'title', 'description', 'budget', 'duration', 'is_active', 'applicant_count']
        read_only_fields = ['id', 'seller', 'is_active']

    def get_applicant_count(self, obj):
        """Ensure `applications` exists before counting"""
        return obj.applications.count() if hasattr(obj, 'applications') else 0

    def create(self, validated_data):
        """Ensure the seller is set from the request"""
        seller = self.context['request'].user
        return Advertisement.objects.create(seller=seller, **validated_data)


class EscrowSerializer(serializers.ModelSerializer):
    """Serializer for managing escrow transactions"""
    advertisement_title = serializers.CharField(source="advertisement.title", read_only=True)
    seller_name = serializers.CharField(source="seller.username", read_only=True)
    buyer_name = serializers.CharField(source="buyer.username", read_only=True)

    class Meta:
        model = Escrow
        fields = ['id', 'advertisement', 'advertisement_title', 'seller', 'seller_name', 'buyer', 'buyer_name', 'amount', 'status']
        read_only_fields = ['id', 'seller', 'status']


class AdvertisementApplicationSerializer(serializers.ModelSerializer):
    """Serializer for buyers applying to advertisements"""
    advertiser_name = serializers.CharField(source="advertiser.username", read_only=True)
    advertisement_title = serializers.CharField(source="advertisement.title", read_only=True)

    class Meta:
        model = AdvertisementApplication
        fields = ['id', 'advertiser', 'advertiser_name', 'advertisement', 'advertisement_title', 'engagement_stats', 'is_completed', 'approved']
        read_only_fields = ['id', 'advertiser', 'approved']

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user:
            validated_data["advertiser"] = request.user
        return super().create(validated_data)
