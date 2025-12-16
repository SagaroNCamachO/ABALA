"""
Punto de entrada para Vercel Serverless Functions.
Wrapper para Flask que convierte eventos de Vercel a WSGI.
"""

import sys
import os

# Configurar paths
if os.path.exists('/var/task'):
    base_path = '/var/task'
else:
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if base_path not in sys.path:
    sys.path.insert(0, base_path)

# Importar la aplicación Flask
try:
    from api.app import app
except ImportError:
    try:
        from app import app
    except ImportError:
        # Crear una app de error si no se puede importar
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def error(path):
            return jsonify({
                "error": "No se pudo importar la aplicación Flask",
                "base_path": base_path,
                "sys_path": sys.path[:5]
            }), 500

# Wrapper para Vercel - convertir eventos de Vercel a WSGI
def handler(event, context):
    """
    Handler para Vercel Serverless Functions.
    Convierte el evento de Vercel al formato WSGI que Flask espera.
    """
    from werkzeug.serving import WSGIRequestHandler
    from werkzeug.wrappers import Request, Response
    from werkzeug.test import Client
    
    # Extraer información del evento de Vercel
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    headers = event.get('headers', {}) or {}
    body = event.get('body', '') or ''
    query_string = event.get('queryStringParameters', {}) or {}
    
    # Convertir headers a formato WSGI
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'SCRIPT_NAME': '',
        'QUERY_STRING': '&'.join([f'{k}={v}' for k, v in query_string.items()]),
        'SERVER_NAME': headers.get('host', 'localhost'),
        'SERVER_PORT': '80',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': headers.get('x-forwarded-proto', 'https'),
        'wsgi.input': None,
        'wsgi.errors': None,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Agregar headers HTTP
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value
    
    # Agregar body si existe
    if body:
        environ['CONTENT_LENGTH'] = str(len(body))
        environ['wsgi.input'] = type('obj', (object,), {
            'read': lambda: body.encode() if isinstance(body, str) else body
        })()
    
    # Crear request de Werkzeug
    request = Request(environ)
    
    # Ejecutar la aplicación Flask
    with app.request_context(environ):
        try:
            response = app.full_dispatch_request()
        except Exception as e:
            from flask import jsonify
            response = app.make_response(jsonify({
                "error": "Error al procesar la solicitud",
                "message": str(e)
            }))
            response.status_code = 500
    
    # Convertir respuesta de Flask a formato de Vercel
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True)
    }

# También exportar la aplicación para compatibilidad
application = app
