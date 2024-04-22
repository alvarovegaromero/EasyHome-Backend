from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from groups.models import UserGroup, Group
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class GroupCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        currency = request.data.get('currency')

        if not name or not description or not currency:
            return Response({'error': 'Name, description and currency are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            group = Group.objects.create(
                name=name,
                description=description,
                currency=currency,
                owner=request.user,
            )

        #Send also group's information
        return Response({'success': 'Group created successfully'}, status=status.HTTP_201_CREATED) 