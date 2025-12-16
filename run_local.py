"""
Script para ejecutar la aplicación Flask localmente.
Ejecuta: python run_local.py
"""

from app import app

if __name__ == '__main__':
    print("="*80)
    print("SISTEMA DE GESTIÓN DE CAMPEONATOS DE BÁSQUETBOL")
    print("="*80)
    print("\nIniciando servidor Flask...")
    print("Abre tu navegador en: http://localhost:5000")
    print("Presiona Ctrl+C para detener el servidor\n")
    print("="*80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

