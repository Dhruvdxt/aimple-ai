from fastapi import Request, HTTPException, status
import requests



def get_ip_info(request: Request):
    try:
        forwarded_for = request.headers.get("X-Forwarded-For")
        real_ip = request.headers.get("X-Real-IP")
        client_ip = request.client.host

        ip = forwarded_for.split(",")[0] if forwarded_for else real_ip or client_ip

        if ip.startswith(("192.168.", "10.", "172.16.", "127.0.0.1")):
            ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
        
        response = requests.get(f"https://ipinfo.io/{ip}/json").json()
        
        return response;
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

