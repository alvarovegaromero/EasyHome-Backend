from venv import logger
from groups.models import Group, UserGroup
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GroupAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, group_id):
        try:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({'error': "Group wasn't found"},
                                status=status.HTTP_404_NOT_FOUND)

            if not UserGroup.objects.filter(
                    user=request.user, group=group).exists():
                return Response(
                    {'error': 'You do not belong to this group.'}, status=status.HTTP_403_FORBIDDEN)

            group_data = {
                'id': group.id,
                'name': group.name,
                'description': group.description,
                'currency': group.currency,
                'creation_date': group.creation_date,
                'owner': group.owner.username,
            }

            return Response(group_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                "An error occurred during group retrieval: %s" %
                str(e))
            return Response({'error': "Internal Server Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, group_id):
        try:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({'error': "Group wasn't found"},
                                status=status.HTTP_404_NOT_FOUND)

            if request.user != group.owner:
                return Response(
                    {
                        'error': 'You do not have permission to delete this group.'},
                    status=status.HTTP_403_FORBIDDEN)

            group.delete()

            return Response(
                {'success': 'Group deleted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                "An error occurred during group deletion: %s" %
                str(e))
            return Response({'error': "Internal Server Error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
