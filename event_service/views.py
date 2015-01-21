from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

events = {
    'event1': 1,
    'event2': 2,
    'event3': 3,
    'event4': 4,
    'event5': 5,
    'event6': 6,
    'event7': 7,
    'event8': 8,
    'event9': 9,
    'event10': 10,
    'event11': 11,

}

class EventsList(APIView):

    def get(self, request, *args, **kwargs):
        print kwargs['org']
        print request.GET['host_id']

        return Response(events, status=status.HTTP_200_OK)

class EventByHost(APIView):

    def get(self, request, *args, **kwargs):
        print kwargs['org']
        print kwargs['host_id']

        return Response(events, status=status.HTTP_200_OK)