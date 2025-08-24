#!/usr/bin/env python3
"""
Script de desarrollo que permite elegir entre diferentes opciones
Uso: python dev.py
"""

import sys
import subprocess

def show_menu():
    """Muestra el menú de opciones"""
    print("🚀 Script de Desarrollo - Signa Backend")
    print("=" * 50)
    print("1. 🏃 Ejecutar solo la aplicación (sin migraciones)")
    print("2. 📋 Ejecutar migraciones de base de datos")
    print("3. 🔄 Ejecutar migraciones y luego la aplicación")
    print("4. 🚪 Salir")
    print("=" * 50)

def run_app_only():
    """Ejecuta solo la aplicación sin migraciones"""
    print("🚀 Iniciando aplicación Flask...")
    print("ℹ️  NOTA: Las migraciones NO se ejecutan automáticamente")
    print("🌐 Aplicación disponible en: http://localhost:5000")
    print("-" * 50)
    
    try:
        from app.main import create_app
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando la aplicación: {str(e)}")

def run_migrations():
    """Ejecuta solo las migraciones"""
    print("📋 Ejecutando migraciones...")
    try:
        subprocess.run([sys.executable, "run_migrations.py"], check=True)
        print("✅ Migraciones completadas exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando migraciones: {e}")
    except KeyboardInterrupt:
        print("\n👋 Migraciones interrumpidas por el usuario")

def run_migrations_and_app():
    """Ejecuta migraciones y luego la aplicación"""
    print("🔄 Ejecutando migraciones y luego la aplicación...")
    try:
        # Primero ejecutar migraciones
        subprocess.run([sys.executable, "run_migrations.py"], check=True)
        print("✅ Migraciones completadas, iniciando aplicación...")
        print("-" * 50)
        
        # Luego ejecutar la aplicación
        run_app_only()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando migraciones: {e}")
    except KeyboardInterrupt:
        print("\n👋 Proceso interrumpido por el usuario")

def main():
    """Función principal del script"""
    while True:
        show_menu()
        
        try:
            choice = input("Selecciona una opción (1-4): ").strip()
            
            if choice == "1":
                run_app_only()
                break
            elif choice == "2":
                run_migrations()
                input("\nPresiona Enter para continuar...")
            elif choice == "3":
                run_migrations_and_app()
                break
            elif choice == "4":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida. Por favor selecciona 1-4.")
                input("Presiona Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            input("Presiona Enter para continuar...")

if __name__ == '__main__':
    main()
