from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from groups.models import Group
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class GroupCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description', '') #empty string if not provided
        currency = request.data.get('currency')

        if not name or not currency:
            return Response({'error': 'Name and currency are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:        
            with transaction.atomic():
                group = Group.objects.create(
                    name=name,
                    description=description,
                    currency=currency,
                    owner=request.user,
                )

                group_data = {
                    'id': group.id,
                    'name': group.name,
                    'description': group.description,
                    'currency': group.currency,
                    'creation_date': group.creation_date,
                    'owner': group.owner.username,
                }

            return Response(group_data, status=status.HTTP_201_CREATED) 
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)