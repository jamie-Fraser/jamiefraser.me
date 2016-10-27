#!/bin/bash
cd /var/www/jamiefraser.me
source /var/venvs/jamiefraser.me/bin/activate

exec gunicorn app:app --workers 3 --user=govhack --bind=unix:/var/www/jamiefraser.me/jamie.sock
