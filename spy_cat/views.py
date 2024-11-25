from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer


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


class TargetViewSet(viewsets.ViewSet):
    def list(self, request, mission_id=None):
        targets = Target.objects.filter(mission_id=mission_id)
        serializer = TargetSerializer(targets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, mission_id=None, pk=None):
        try:
            target = Target.objects.get(mission_id=mission_id, pk=pk)
        except Target.DoesNotExist:
            return Response(
                {'error': 'Target not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TargetSerializer(target)
        return Response(serializer.data)

    def create(self, request, mission_id=None):
        data = request.data
        data['mission'] = mission_id
        serializer = TargetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, mission_id=None, pk=None):
        try:
            target = Target.objects.get(mission_id=mission_id, pk=pk)
        except Target.DoesNotExist:
            return Response(
                {'error': 'Target not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TargetSerializer(
            target,
            data=request.data,
            partial=False
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['patch'], url_path='mark-complete')
    def mark_complete(self, request, mission_id=None, pk=None):
        try:
            target = Target.objects.get(mission_id=mission_id, pk=pk)
        except Target.DoesNotExist:
            return Response(
                {'error': 'Target not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if target.complete:
            return Response(
                {'error': 'Target already marked as complete'},
                status=status.HTTP_400_BAD_REQUEST
            )

        target.complete = True
        target.save()
        return Response(
            {'message': 'Target marked as complete'},
            status=status.HTTP_200_OK
        )
