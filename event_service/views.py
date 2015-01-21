from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from event_service.models import Event, Organization
from event_service.serializers import EventSerializer
from dateutil import parser


class EventsList(APIView):

    def get(self, request, *args, **kwargs):

        # Get the org first
        org = self._get_org(kwargs)
        if not org:
            return Response('Org not found',
                            status=status.HTTP_404_NOT_FOUND)

        # Setup the base query, filter by org and always have desc created
        # sorting
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

    def post(self, request, *args, **kwargs):

        # Get the org first
        org = self._get_org(kwargs)
        if not org:
            return Response('Org not found',
                            status=status.HTTP_404_NOT_FOUND)

        # Verify we have the data for the event
        if ('hostname' not in request.data or
            'string' not in request.data or
            'created_on' not in request.data):
            return Response('Event data not provided correctly',
                            status=status.HTTP_400_BAD_REQUEST)

        # Convert this to a date
        try:
            created_on = parser.parse(request.data['created_on'])
        except ValueError:
            return Response('Malformed date',
                            status=status.HTTP_400_BAD_REQUEST)

        # Let's create an event
        e = Event.objects.create(org=org, hostname=request.data['hostname'],
                                 string=request.data['string'],
                                 created_on=created_on)

        # Send the created event representation back to the user
        serializer = EventSerializer(e)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_org(self, kwargs):
        org_name = kwargs.get('org', None)
        if not org_name or not Organization.objects.filter(name=org_name).exists():
            return None

        return Organization.objects.get(name=org_name)

