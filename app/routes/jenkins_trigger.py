import os
import logging
from urllib.parse import urljoin
import requests
from app.controller.config import JENKINS_BASE_URL

logger = logging.getLogger(__name__)

BASE = JENKINS_BASE_URL.rstrip('/')
GENERIC_TOKEN = os.getenv("JENKINS_GENERIC_TOKEN", "MYTOKEN")

session = requests.Session()
session.headers.update({"User-Agent": "upload-service/1.0", "Accept": "application/json"})

def trigger_via_generic(zip_name: str, s3_key: str, deploy_id: int, token: str = GENERIC_TOKEN):

    url = urljoin(BASE + "/", "generic-webhook-trigger/invoke")
    payload = {"ZIP_NAME": zip_name, "S3_KEY": s3_key, "DEPLOY_ID": deploy_id}

    try:
        r = session.post(url, params={"token": token}, json=payload, timeout=10)
        logger.info("Trigger Jenkins via Generic: %s -> %s %s", url, r.status_code, r.text[:120])
        return {"ok": r.ok, "status.html": r.status_code, "body": r.text}
    except requests.RequestException as e:
        logger.exception("Trigger Jenkins failed")
        return {"ok": False, "status.html": 0, "error": str(e)}
