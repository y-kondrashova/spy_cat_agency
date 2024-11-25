from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import SpyCat, Mission
from .serializers import SpyCatSerializer, MissionSerializer


class SpyCatListCreateView(ListCreateAPIView):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class SpyCatDetailView(RetrieveUpdateDestroyAPIView):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response({'error': 'Cannot delete mission assigned to a cat.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.complete:
            return Response({'error': 'Cannot update completed mission.'}, status=status.HTTP_400_BAD_REQUEST)

        for target in instance.targets.all():
            if target.complete:
                return Response({'error': 'Cannot update notes of completed targets.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=['patch'], url_path='assign-cat')
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        if mission.cat:
            return Response({'error': 'Mission is already assigned to a cat.'}, status=status.HTTP_400_BAD_REQUEST)

        cat_id = request.data.get('cat_id')
        try:
            cat = SpyCat.objects.get(id=cat_id)
        except SpyCat.DoesNotExist:
            return Response({'error': 'Cat not found.'}, status=status.HTTP_404_NOT_FOUND)

        mission.cat = cat
        mission.save()
        return Response({'message': 'Cat assigned successfully.'})


