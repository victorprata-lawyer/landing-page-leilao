import os
import sys

# Correção mínima: adiciona /backend ao sys.path e configura handler com Mangum para strip /api

dir_path = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(dir_path, '..', 'backend')
sys.path.insert(0, backend_path)

from main import app
from mangum import Mangum

handler = Mangum(app)

def main(request: dict):
    path = request.get('path', '')
    if path == '/api':
        request['path'] = '/'
    elif path.startswith('/api/'):
        request['path'] = path[5:]

    if 'rawPath' in request:
        raw_path = request['rawPath']
        if raw_path == '/api':
            request['rawPath'] = '/'
        elif raw_path.startswith('/api/'):
            request['rawPath'] = raw_path[5:]

    return handler(request)