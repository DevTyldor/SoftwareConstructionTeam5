import socketserver

from processors import notification_processor
from request_handler import RequestHandler


# SERVER STARTUP
if __name__ == "__main__":
    PORT = 3000
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        notification_processor.start()
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()

# dit is een dev ruleset test