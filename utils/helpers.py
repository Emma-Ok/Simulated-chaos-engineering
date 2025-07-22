"""
Utilidades simplificadas para el simulador de Chaos Engineering.
Solo contiene las funciones esenciales sin duplicación.
"""

import json
import yaml
import time
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import os

def setup_logging(log_level: str = "INFO", log_file: str = None, colors: bool = True) -> logging.Logger:
    """
    Configura el sistema de logging simplificado.
    
    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
        log_file: Archivo opcional para logging
        colors: Si True, usa colores en la consola
    """
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Limpiar handlers existentes
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    
    if colors:
        try:
            colored_formatter = ColoredFormatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(colored_formatter)
        except:
            # Fallback a formato normal
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(formatter)
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # Handler para archivo si se especifica
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def load_config(config_path: str) -> Dict[str, Any]:
    """Carga configuración desde archivo YAML o JSON."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            elif config_path.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError("Formato no soportado. Use .yaml, .yml o .json")
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {config_path}")
    except Exception as e:
        raise RuntimeError(f"Error cargando configuración: {e}")

def format_timestamp(timestamp: float = None) -> str:
    """Formatea un timestamp a string legible."""
    if timestamp is None:
        timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def format_duration(seconds: float) -> str:
    """Formatea una duración en segundos a string legible."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def generate_unique_id(prefix: str = "") -> str:
    """Genera un ID único con prefijo opcional."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}-{unique_id}" if prefix else unique_id

class ColoredFormatter(logging.Formatter):
    """Formatter que añade colores a los logs."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cian
        'INFO': '\033[32m',     # Verde
        'WARNING': '\033[33m',  # Amarillo
        'ERROR': '\033[31m',    # Rojo
        'CRITICAL': '\033[91m', # Rojo brillante
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Añadir color al nivel de log
        level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{level_color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

# Función de compatibilidad
def setup_colored_logging(log_level: str = "INFO") -> logging.Logger:
    """Configuración de logging con colores (mantiene compatibilidad)."""
    return setup_logging(log_level=log_level, colors=True)
