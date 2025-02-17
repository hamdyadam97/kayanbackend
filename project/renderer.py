from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """
    Custom renderer to format API responses with a consistent structure.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response', None)
        success = response is not None and 200 <= response.status_code < 300

        # Ensure data is properly formatted for errors
        if not success:
            errors = data if isinstance(data, dict) else {"error": data}
            result = {"success": False, **errors}
        else:
            result = {"success": True, "data": data if data is not None else None}

        return super().render(result, accepted_media_type, renderer_context)
