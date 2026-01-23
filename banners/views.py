from rest_framework.views import APIView
from django.utils import timezone
from .models import Banner
from rest_framework.response import Response
from .serializers import BannerSerializer


class HomepageBannerAPIView(APIView):
    def get(self, request):
        now = timezone.now()

        banners = Banner.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).select_related('slot').order_by('priority')

        data = {}

        for banner in banners:
            slot_key = banner.slot.key
            data.setdefault(slot_key, []).append(BannerSerializer(banner,context={'request':request}).data)

        return Response(data)

