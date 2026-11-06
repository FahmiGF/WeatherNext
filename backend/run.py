"""WeatherNext AI — Backend Entry Point."""
import os
import socket
import uvicorn

def is_port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0

if __name__ == "__main__":
    requested_port = int(os.getenv("PORT", 8001))
    port = requested_port if is_port_available(requested_port) else 8002
    print(f"Starting WeatherNext AI Backend on http://localhost:{port}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
