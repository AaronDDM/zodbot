import firebase_admin # type: ignore
import os
from firebase_admin import credentials
from firebase_admin import firestore
from zodbot.config import config

# Ensure that the service account key exists
service_account_key_path = os.path.abspath(config.firebase_service_account_key)
if not os.path.exists(service_account_key_path):
    raise FileNotFoundError(f"Service account key not found at {service_account_key_path}")

# Use a service account.
cred = credentials.Certificate(service_account_key_path)

app = firebase_admin.initialize_app(cred)

db = firestore.client()