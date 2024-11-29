
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import Throttled
from datetime import datetime


class CustomAnonRateThrottle(AnonRateThrottle):
    rate = '3/hour'  # Define the throttle rate for anonymous users

    def allow_request(self, request, view):
        """
        Check if the request should be throttled.
        """
        # Check if the request should be throttled based on the super class method
        allowed = super().allow_request(request, view)

        # If the request is throttled (not allowed), raise Throttled exception
        if not allowed:
            
            raise Throttled(wait=7200)
        return True
    
    

    