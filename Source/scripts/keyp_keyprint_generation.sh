#!/bin/sh

openssl x509 -noout -fingerprint -sha256 < "$1" | cut -d '=' -f 2 | tr -dc "[A-F][0-9]" | python -c "import sys; import base64; print base64.b32encode(base64.b16decode(sys.stdin.readline()))" | tr -d "="