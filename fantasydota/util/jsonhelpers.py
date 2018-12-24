import datetime
from pyramid.renderers import JSON


def custom_json_renderer():
    """
    Return a custom json renderer that can deal with some datetime objects.
    """
    def datetime_adapter(obj, request):
        return obj.isoformat()

    def time_adapter(obj, request):
        return str(obj)

    json_renderer = JSON()
    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    json_renderer.add_adapter(datetime.time, time_adapter)
    return json_renderer