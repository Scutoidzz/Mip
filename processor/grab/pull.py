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
    path = parsed.path if parsed.path else "/"

    def receive_response(sock):
        header_end = b"\r\n\r\n"
        data = b""
        while header_end not in data:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        
        headers, _, body = data.partition(header_end)
        headers_str = headers.decode("utf-8", errors="ignore")
        
        content_length = 0
        for line in headers_str.split("\r\n"):
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":")[1].strip())
                break
        
        body_len = len(body)
        while body_len < content_length:
            chunk = sock.recv(4096)
            if not chunk:
                break
            body += chunk
            body_len += len(chunk)
        
        return body
    
    if https_status:
        with open(os.path.join(os.path.dirname(__file__), "info.json"), "r") as f:
            info = json.load(f)
        context = ssl.create_default_context()
        sock = socket.create_connection((host, 443))
    
        sock = context.wrap_socket(sock, server_hostname=host)
    
        sock.sendall(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\nUser-Agent: " + info["ua"].encode() + b"\r\nConnection: close\r\n\r\n")
        response = receive_response(sock)
    
        if "Name or service not known" in response.decode():
            logging.error("Name or service not known")
            response = b"<!DOCTYPE html><html><head><title>404</title></head><body><h1>404 Not Found</h1><p>Couldn't find the site you were looking for.</p></body></html>"
        return response, https_status
   
    else:
        sock = None
        try:
            with open(os.path.join(os.path.dirname(__file__), "info.json"), "r") as f:
                info = json.load(f)
            sock = socket.create_connection((host, 80))
            sock.sendall(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\nUser-Agent: " + info["ua"].encode() + b"\r\nConnection: close\r\n\r\n")
            response = receive_response(sock)
        except Exception as e:
            logging.error(e)
            response = b"<!DOCTYPE html><html><head><title>500</title></head><body><h1>500 Internal Server Error</h1><p>Couldn't find the site you were looking for.</p></body></html>"
            return response, False
        finally:
            if sock:
                sock.close()
        if "Name or service not known" in response.decode():
            logging.error("Name or service not known")
        return response, False