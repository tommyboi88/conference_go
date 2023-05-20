from django.http import JsonResponse
from .models import Attendee
from common.json import ModelEncoder
from events.api_views import ConferenceListEncoder


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = ["name"]


def api_list_attendees(request, conference_id):
    attendees = Attendee.objects.filter(conference=conference_id)
    return JsonResponse(
        {"attendees": attendees},
        encoder=AttendeeListEncoder,
    )
    """
    Lists the attendees names and the link to the attendee
    for the specified conference id.

    Returns a dictionary with a single key "attendees" which
    is a list of attendee names and URLS. Each entry in the list
    is a dictionary that contains the name of the attendee and
    the link to the attendee's information.

    {
        "attendees": [
            {
                "name": attendee's name,
                "href": URL to the attendee,
            },
            ...
        ]
    }
    """


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]

    encoders = {
        "conference": ConferenceListEncoder(),
    }


def api_show_attendee(request, id):
    attendee = Attendee.objects.get(id=id)
    return JsonResponse(
        attendee,
        encoder=AttendeeDetailEncoder,
        safe=False,
    )

    """
    Returns the details for the Attendee model specified
    by the id parameter.

    This should return a dictionary with email, name,
    company name, created, and conference properties for
    the specified Attendee instance.

    {
        "email": the attendee's email,
        "name": the attendee's name,
        "company_name": the attendee's company's name,
        "created": the date/time when the record was created,
        "conference": {
            "name": the name of the conference,
            "href": the URL to the conference,
        }
    }
    """
