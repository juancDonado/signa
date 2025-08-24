#!/usr/bin/env python3
"""
Script para ejecutar migraciones de la base de datos
Uso: python run_migrations.py
"""

from migrations.migration_manager import run_migrations

if __name__ == '__main__':
    print("🔄 Ejecutando migraciones de la base de datos...")
    run_migrations()
