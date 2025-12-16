"""
Punto de entrada para Vercel Serverless Functions.
Vercel maneja Flask automáticamente cuando se exporta la app directamente.
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

# Importar la aplicación Flask con manejo de errores detallado
try:
    print(f"Intentando importar desde api.app...")
    from api.app import app
    print(f"✓ App importada exitosamente desde api.app")
except ImportError as e1:
    print(f"✗ Error al importar desde api.app: {e1}")
    try:
        print(f"Intentando importar desde app...")
        from app import app
        print(f"✓ App importada exitosamente desde app")
    except ImportError as e2:
        print(f"✗ Error al importar desde app: {e2}")
        print(f"Creando app de error...")
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def error(path):
            import traceback
            return jsonify({
                "error": "No se pudo importar la aplicación Flask",
                "import_error_1": str(e1),
                "import_error_2": str(e2),
                "base_path": base_path,
                "base_path_exists": os.path.exists(base_path),
                "sys_path": sys.path[:5],
                "files_in_api": os.listdir(os.path.join(base_path, 'api')) if os.path.exists(os.path.join(base_path, 'api')) else "No existe",
                "traceback": traceback.format_exc()
            }), 500
except Exception as e:
    print(f"✗ Error inesperado: {e}")
    import traceback
    traceback.print_exc()
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def error_handler(path):
        return jsonify({
            "error": "Error inesperado al cargar la aplicación",
            "message": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }), 500

print(f"Exportando app como handler y application...")
# Vercel busca 'handler' o 'application'
# Para Flask, simplemente exportamos la app - Vercel la maneja automáticamente
handler = app
application = app
print(f"✓ Handler y application exportados correctamente")
