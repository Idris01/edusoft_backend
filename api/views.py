from rest_framework.generics import ListCreateAPIView
from backend.models import University, Country
from .serializers import UniversitySerializer

class UniversityListCreateAPIView(ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

    def post(request, *args, **kwargs):
        data = request.data
        if "country" in data:
            country_code = data.get("country")

