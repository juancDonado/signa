#!/usr/bin/env python3
"""
Script principal para ejecutar la aplicación Flask
Uso: python run.py
"""

from app.main import create_app

if __name__ == '__main__':
    """ print("🚀 Iniciando aplicación Flask...")
    print("ℹ️  NOTA: Las migraciones NO se ejecutan automáticamente")
    print("📋 Para ejecutar migraciones use: python run_migrations.py")
    print("🌐 Aplicación disponible en: http://localhost:5000")
    print("-" * 50)
     """
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)