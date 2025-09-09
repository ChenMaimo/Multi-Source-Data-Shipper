import logging
import os

def setup_logging()->None:
    root = logging.getLogger()
    if root.handlers:
        return
    
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    root.setLevel(getattr(logging, level_name, logging.INFO))

    ch = logging.StreamHandler()
    ch.setLevel(root.level)
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s"))
    root.addHandler(ch)


    token = os.getenv("LOGIZ_IO_TOKEN") or os.getenv("LOGZIO_TOKEN")
    listener = os.getenv("LOGIZ_LISENTER_HOST") or os.getenv("LOGZIO_LISTENER_HOST")
    if token and listener:
        try:
            from logzio.handler import LogzioHandler
            url = listener.strip()
            if not url.startswith("http"):
                url = "https://" + url.lstrip("/")

            lz = LogzioHandler(
                token=token,
                url=url,
                logzio_type="python-logs",
                logs_drain_timeout=5,
            )
            lz.setLevel(root.level)
            root.addHandler(lz)
            logging.getLogger(__name__).info("Logz.io handler enabled (url=%s)", url)
        except Exception as e:
            logging.getLogger(__name__).warning("Failed to enable Logz.io handler: %s", e)
