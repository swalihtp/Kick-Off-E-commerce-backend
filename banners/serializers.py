from rest_framework import serializers
from .models import BannerSlot, Banner

class BannerSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerSlot
        fields = ['id', 'key', 'description']
        ordering = ['priority']
        
class BannerSerializer(serializers.ModelSerializer):
    slot = serializers.CharField(source='slot.key', read_only=True)

    image_desktop = serializers.SerializerMethodField()
    image_mobile = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = [
            'id',
            'slot',
            'title',
            'subtitle',
            'image_desktop',
            'image_mobile',
            'link_type',
            'link_value',
            'priority',
            'template_type'
        ]

    def get_image_desktop(self, obj):
        request = self.context.get('request')
        if obj.image_desktop and request:
            return request.build_absolute_uri(obj.image_desktop.url)
        return None

    def get_image_mobile(self, obj):
        request = self.context.get('request')
        if obj.image_mobile and request:
            return request.build_absolute_uri(obj.image_mobile.url)
        return None
    
    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data


class BannerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
