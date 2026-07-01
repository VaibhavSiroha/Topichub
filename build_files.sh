#!/bin/bash
# Vercel build step: install deps, apply migrations, and collect static files.
# Vercel's build image is an "externally managed" (PEP 668) Python env, so pip
# needs --break-system-packages to install into it.
set -e

python3 -m pip install --break-system-packages -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput --clear
