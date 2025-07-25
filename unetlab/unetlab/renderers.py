from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response", None)
        request = renderer_context.get("request", None)
        command = request.resolver_match.view_name
        status_code = response.status_code
        status_type = "success" if status_code < 400 else "error"

        wrapped = {
            "status": status_type,
            "http": {
                "code": status_code,
                "message": response.status_text,
                "url": request.get_full_path(),
            },
            "type": "reponse",
            "command": command,
            "data": data,
        }
        return super().render(wrapped, accepted_media_type, renderer_context)
