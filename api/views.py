from rest_framework.generics import ListCreateAPIView
from backend.models import University
from .serializers import UniversitySerializer

class UniversityListCreateAPIView(ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

