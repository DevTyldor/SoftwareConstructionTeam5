import json

from providers import auth_provider


def read_json(request):
    """Read the request body and parse it as JSON."""
    content_length = int(request.headers["Content-Length"])
    post_data = request.rfile.read(content_length)
    return json.loads(post_data.decode())


def discard_body(request):
    """Read and throw away the request body."""
    # Dit is een fix voor connection timed out (Stefano)
    length = int(request.headers.get("Content-Length", 0) or 0)
    if length:
        request.rfile.read(length)


def send_status(request, status):
    """Send an empty response with only a status code."""
    request.send_response(status)
    request.end_headers()


def send_json(request, data):
    """Send data as a 200 JSON response."""
    request.send_response(200)
    request.send_header("Content-type", "application/json")
    request.end_headers()
    request.wfile.write(json.dumps(data).encode("utf-8"))


def check_access(request, user, resource, method):
    """Return True if the user may use this resource, otherwise send 403."""
    if auth_provider.has_access(user, [resource], method):
        return True

    discard_body(request)
    request.send_response(403)
    request.send_header("Content-Type", "text/plain")
    request.end_headers()
    request.wfile.write(b"Access denied to this resource.")
    return False