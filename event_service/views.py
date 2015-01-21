from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from event_service.models import Event, Organization
from event_service.serializers import EventSerializer


class EventsList(APIView):

    def get(self, request, *args, **kwargs):
        org_name = kwargs.get('org', None)
        if not org_name or not Organization.objects.filter(name=org_name).exists():
            return Response('Org not found',
                            status=status.HTTP_404_NOT_FOUND)

        # Setup the base query, filter by org and always have desc created
        # sorting
        org = Organization.objects.get(name=org_name)
        query = Event.objects.filter(org=org).order_by('-created_on')

        # filter by hostname if it has been provided
        if 'hostname' in request.GET:
            query = query.filter(hostname=request.GET['hostname'])

        # filter by page size if it has been provided, default to 100
        page_size = 100
        if 'page_size' in request.GET:
            try:
                page_size = int(request.GET['page_size'])
            except ValueError:
                # TODO: report this error?
                pass

        serializer = EventSerializer(query[0:page_size], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
