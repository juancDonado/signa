from contextlib import contextmanager
from typing import Generator, Any, Callable
from flask import current_app
from ..infrastructure.database.models import db
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class TransactionService:
    """Servicio para manejo de transacciones de base de datos (similar a QueryRunner de TypeORM)"""
    
    @staticmethod
    @contextmanager
    def transaction() -> Generator[Any, None, None]:
        """
        Context manager para transacciones automáticas.
        Similar al QueryRunner de TypeORM.
        
        Uso:
            with TransactionService.transaction() as session:
                # Hacer operaciones en la transacción
                user = User(name="Juan")
                session.add(user)
                # Si no hay excepción, se hace commit automático
                # Si hay excepción, se hace rollback automático
        """
        session = db.session
        try:
            logger.info("🚀 Iniciando transacción de base de datos")
            yield session
            
            # Si llegamos aquí, no hubo excepciones, hacer commit
            session.commit()
            logger.info("✅ Transacción completada exitosamente")
            
        except SQLAlchemyError as e:
            # Error de base de datos, hacer rollback
            session.rollback()
            logger.error(f"❌ Error en transacción, rollback ejecutado: {str(e)}")
            raise
            
        except Exception as e:
            # Otro tipo de error, hacer rollback
            session.rollback()
            logger.error(f"❌ Error inesperado en transacción, rollback ejecutado: {str(e)}")
            raise
    
    @staticmethod
    @contextmanager
    def read_only_transaction() -> Generator[Any, None, None]:
        """
        Context manager para transacciones de solo lectura.
        Útil para consultas que no modifican datos.
        """
        session = db.session
        try:
            logger.info("📖 Iniciando transacción de solo lectura")
            yield session
            
            # Para transacciones de solo lectura, no necesitamos commit
            logger.info("✅ Transacción de solo lectura completada")
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error en transacción de solo lectura: {str(e)}")
            raise
    
    @staticmethod
    def execute_in_transaction(operation: Callable) -> Any:
        """
        Ejecuta una operación dentro de una transacción.
        Similar al execute() del QueryRunner de TypeORM.
        
        Args:
            operation: Función que contiene la lógica de la transacción
            
        Returns:
            Resultado de la operación
            
        Raises:
            Exception: Si la transacción falla
        """
        with TransactionService.transaction() as session:
            return operation(session)
    
    @staticmethod
    def execute_read_only(operation: Callable) -> Any:
        """
        Ejecuta una operación de solo lectura dentro de una transacción.
        
        Args:
            operation: Función que contiene la lógica de consulta
            
        Returns:
            Resultado de la consulta
        """
        with TransactionService.read_only_transaction() as session:
            return operation(session)
    
    @staticmethod
    def rollback_on_error(operation: Callable) -> Any:
        """
        Ejecuta una operación con rollback automático en caso de error.
        Útil para operaciones que pueden fallar parcialmente.
        
        Args:
            operation: Función que contiene la lógica
            
        Returns:
            Resultado de la operación
        """
        try:
            return operation()
        except Exception as e:
            # Hacer rollback de cualquier cambio pendiente
            db.session.rollback()
            logger.error(f"❌ Operación falló, rollback ejecutado: {str(e)}")
            raise

# Alias para uso más simple
TransactionRunner = TransactionService
