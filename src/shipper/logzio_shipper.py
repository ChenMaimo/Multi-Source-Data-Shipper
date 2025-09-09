import os
import json
import logging
import requests
from typing import Iterable, Dict, Any
from tenacity import retry, wait_exponential_jitter, stop_after_attempt,retry_if_exception_type

class LogzioShipper:
    def __init__(self)->None:
        self.log = logging.getLogger("shipper.logzio")
        token = os.getenv("LOGIZ_IO_TOKEN") or ""
        listener  = os.getenv("LOGIZ_LISENTER_HOST") or "https://listener.logz.io:8071"
        if not token:
            raise RuntimeError("Missing Logzio_Token (LOGIZ_IO_TOKEN)")
        
        
        listener = listener.strip()
        if listener.startswith("http://"):
            listener = "https://" + listener[len("http://"):]
        elif not listener.startswith("https://"):
            listener = "https://" + listener.lstrip("/")

        self.url = f"{listener}/?token={token}&type=weather-pipeline"
        self.session = requests.Session()
        self.log.info("Configured Logzio url=%s", self.url)


    @retry(
        wait= wait_exponential_jitter(initial=1, max=20),
        stop= stop_after_attempt(int(os.getenv("MAX_RETRIES", "5"))),
        retry= retry_if_exception_type((requests.RequestException))
    )
    def _post(self, payload: str)-> None:
        self.log.debug("POST bytes=%d", len(payload))
        resp = self.session.post(
            self.url,
            data=payload.encode("utf-8"),
            timeout=8,
            headers={"Content-Type": "application/json"},
        )

        if 500 <= resp.status_code < 600:
            self.log.warning("Server 5xx: %s", resp.text)
            raise requests.RequestException(f"Server error {resp.status_code}: {resp.text}")
        
        if 400 <= resp.status_code < 500:
            self.log.error("Client 4xx: %s", resp.text)
            raise RuntimeError(f"Client error {resp.status_code}: {resp.text}")
        
        resp.raise_for_status()
    
    def ship(self, events: Iterable[Dict[str,Any]])->None:
        body = "\n".join(json.dumps(e, ensure_ascii=False) for e in events)
        if body and not body.endswith("\n"):
            body += "\n"
        if body.strip():
            self._post(body)
            self.log.info("Posted %d events", len(body.strip().splitlines()))
