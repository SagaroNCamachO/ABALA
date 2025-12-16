"""
Punto de entrada para Vercel Serverless Functions.
Handler que convierte eventos de Vercel a WSGI para Flask.
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
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def error(path):
            return jsonify({
                "error": "No se pudo importar la aplicación Flask"
            }), 500

# Handler para Vercel - debe ser una función, no la app directamente
def handler(event, context):
    """
    Handler para Vercel Serverless Functions.
    Convierte eventos de Vercel al formato WSGI.
    """
    # Extraer información del evento
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    headers = event.get('headers', {}) or {}
    body = event.get('body', '') or ''
    query_params = event.get('queryStringParameters', {}) or {}
    
    # Construir query string
    query_string = '&'.join([f'{k}={v}' for k, v in query_params.items()])
    
    # Crear entorno WSGI
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'SCRIPT_NAME': '',
        'QUERY_STRING': query_string,
        'SERVER_NAME': headers.get('host', 'localhost').split(':')[0],
        'SERVER_PORT': headers.get('host', 'localhost').split(':')[1] if ':' in headers.get('host', '') else '80',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': headers.get('x-forwarded-proto', 'https'),
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Agregar headers HTTP
    for key, value in headers.items():
        key_upper = key.upper().replace('-', '_')
        if key_upper in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[key_upper] = value
        else:
            environ[f'HTTP_{key_upper}'] = value
    
    # Agregar body
    if body:
        body_bytes = body.encode('utf-8') if isinstance(body, str) else body
        environ['CONTENT_LENGTH'] = str(len(body_bytes))
        environ['wsgi.input'] = type('obj', (object,), {
            'read': lambda: body_bytes,
            'readline': lambda: body_bytes,
        })()
    else:
        environ['CONTENT_LENGTH'] = '0'
        environ['wsgi.input'] = type('obj', (object,), {
            'read': lambda: b'',
            'readline': lambda: b'',
        })()
    
    # Agregar variables de entorno estándar
    environ['wsgi.errors'] = sys.stderr
    
    # Ejecutar la aplicación Flask
    response_headers = {}
    status_code = 500
    response_body = b''
    
    try:
        with app.request_context(environ):
            response = app.full_dispatch_request()
            status_code = response.status_code
            response_body = response.get_data()
            response_headers = dict(response.headers)
    except Exception as e:
        from flask import jsonify
        try:
            with app.app_context():
                error_response = app.make_response(jsonify({
                    "error": "Error al procesar la solicitud",
                    "message": str(e)
                }))
                status_code = 500
                response_body = error_response.get_data()
                response_headers = dict(error_response.headers)
        except:
            status_code = 500
            response_body = f'{{"error": "Error crítico: {str(e)}"}}'.encode('utf-8')
            response_headers = {'Content-Type': 'application/json'}
    
    # Convertir a formato de Vercel
    return {
        'statusCode': status_code,
        'headers': response_headers,
        'body': response_body.decode('utf-8') if isinstance(response_body, bytes) else str(response_body)
    }

# Exportar también la aplicación para compatibilidad (aunque Vercel usará handler)
application = app
