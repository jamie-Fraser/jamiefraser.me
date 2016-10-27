from flask import render_template
import requests

API_KEY = "key-2ad500ff69c6f137d0094d9c12d24206"

def send_email(from_email, subject, text, html):
    return requests.post(
        "https://api.mailgun.net/v3/jamiefraser.me/messages",
        auth=("api", API_KEY),
        data={"from": from_email,
              "to": ["Jamie Fraser <jamie@jamiefraser.me>"],
              "subject": subject,
              "text": text,
              "html": html})
              
