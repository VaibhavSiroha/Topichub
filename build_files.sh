#!/bin/bash
# Vercel build step: install deps and collect static files into STATIC_ROOT.
pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
