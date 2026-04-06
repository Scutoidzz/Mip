import ssl
import socket
import logging
import json
import os
from urllib.parse import urlparse

def pull_raw(url):
    parsed = urlparse(url)
    https_status = parsed.scheme == "https"
    host = parsed.netloc

    if https_status:
        with open(os.path.join(os.path.dirname(__file__), "info.json"), "r") as f:
            info = json.load(f)
        context = ssl.create_default_context()
        sock = socket.create_connection((host, 443))
    
        sock = context.wrap_socket(sock, server_hostname=host)
    
        sock.sendall(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\nUser-Agent: " + info["ua"].encode() + b"\r\n\r\n")
    
        response = sock.recv(4096)
    
        if "Name or service not known" in response.decode():
            logging.error("Name or service not known")
            response = b"<!DOCTYPE html><html><head><title>404</title></head><body><h1>404 Not Found</h1><p>Couldn't find the site you were looking for.</p></body></html>"
        return response, https_status
   
    else:
        try:
            with open(os.path.join(os.path.dirname(__file__), "info.json"), "r") as f:
                info = json.load(f)
            sock = socket.create_connection((host, 80))
            sock.sendall(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\nUser-Agent: " + info["ua"].encode() + b"\r\n\r\n")
            response = sock.recv(4096)
        except Exception as e:
            logging.error(e)
            response = b"<!DOCTYPE html><html><head><title>500</title></head><body><h1>500 Internal Server Error</h1><p>Couldn't find the site you were looking for.</p></body></html>"
            return response, False
        if "Name or service not known" in response.decode():
            logging.error("Name or service not known")
            response = b"<!DOCTYPE html><html><head><title>404</title></head><body><h1>404 Not Found</h1><p>Couldn't find the site you were looking for.</p></body></html>"
            # For now until I implement actual rendering
            sock.close()
        return response, False