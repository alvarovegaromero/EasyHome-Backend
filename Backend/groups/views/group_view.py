from django.shortcuts import get_object_or_404
from groups.models import Group, UserGroup
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GroupAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)

        if not UserGroup.objects.filter(user=request.user, group=group).exists():
            return Response({'error': 'You do not belong to this group.'}, status=status.HTTP_403_FORBIDDEN)
        
        group_data = {
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'currency': group.currency,
            'creation_date': group.creation_date,
            'owner': group.owner.username,
        }
        
        return Response(group_data, status=status.HTTP_200_OK)


    def post(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)

        if request.user != group.owner:
            return Response({'error': 'You do not have permission to delete this group.'}, status=status.HTTP_403_FORBIDDEN)

        group.delete()

        return Response({'success': 'Group deleted successfully'}, status=status.HTTP_200_OK)
        
