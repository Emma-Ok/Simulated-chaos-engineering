"""
Utilidades comunes para el simulador de Chaos Engineering.
"""

import json
import yaml
import time
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import os

def setup_logging(log_level: str = "INFO", log_file: str = None) -> logging.Logger:
    """
    Configura el sistema de logging para el simulador.
    """
    # Configurar formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Logger raíz
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo si se especifica
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Carga configuración desde archivo YAML o JSON.
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                return yaml.safe_load(f)
            elif config_path.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError("Formato de archivo no soportado. Use .yaml, .yml o .json")
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {config_path}")
    except Exception as e:
        raise RuntimeError(f"Error cargando configuración: {e}")

def save_config(config: Dict[str, Any], config_path: str):
    """
    Guarda configuración a archivo YAML o JSON.
    """
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            elif config_path.endswith('.json'):
                json.dump(config, f, indent=2, ensure_ascii=False)
            else:
                raise ValueError("Formato de archivo no soportado. Use .yaml, .yml o .json")
    except Exception as e:
        raise RuntimeError(f"Error guardando configuración: {e}")

def format_timestamp(timestamp: float = None) -> str:
    """
    Formatea un timestamp a string legible.
    """
    if timestamp is None:
        timestamp = time.time()
    
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def format_duration(seconds: float) -> str:
    """
    Formatea una duración en segundos a string legible.
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def calculate_availability(healthy_instances: int, total_instances: int) -> float:
    """
    Calcula el porcentaje de disponibilidad.
    """
    if total_instances == 0:
        return 0.0
    return (healthy_instances / total_instances) * 100

def calculate_error_rate(errors: int, total_requests: int) -> float:
    """
    Calcula la tasa de errores.
    """
    if total_requests == 0:
        return 0.0
    return (errors / total_requests) * 100

def generate_unique_id(prefix: str = "") -> str:
    """
    Genera un ID único con prefijo opcional.
    """
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}-{unique_id}" if prefix else unique_id

def validate_service_config(config: Dict[str, Any]) -> List[str]:
    """
    Valida la configuración de servicios.
    Retorna una lista de errores encontrados.
    """
    errors = []
    
    # Validar campos requeridos
    required_fields = ["type", "initial_instances", "min_instances", "max_instances"]
    for field in required_fields:
        if field not in config:
            errors.append(f"Campo requerido faltante: {field}")
    
    # Validar valores numéricos
    if "initial_instances" in config and config["initial_instances"] < 1:
        errors.append("initial_instances debe ser mayor a 0")
    
    if "min_instances" in config and config["min_instances"] < 1:
        errors.append("min_instances debe ser mayor a 0")
    
    if ("min_instances" in config and "max_instances" in config and 
        config["min_instances"] > config["max_instances"]):
        errors.append("min_instances no puede ser mayor que max_instances")
    
    if ("initial_instances" in config and "min_instances" in config and 
        config["initial_instances"] < config["min_instances"]):
        errors.append("initial_instances no puede ser menor que min_instances")
    
    return errors

def validate_experiment_config(config: Dict[str, Any]) -> List[str]:
    """
    Valida la configuración de experimentos.
    """
    errors = []
    
    # Validar probabilidades
    for experiment_type, experiment_config in config.items():
        if isinstance(experiment_config, dict) and "probability" in experiment_config:
            prob = experiment_config["probability"]
            if not (0.0 <= prob <= 1.0):
                errors.append(f"Probabilidad inválida en {experiment_type}: {prob}")
    
    return errors

def create_directory_if_not_exists(directory_path: str):
    """
    Crea un directorio si no existe.
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
    except Exception as e:
        raise OSError(f"Error creando directorio {directory_path}: {e}")

def safe_float_conversion(value: Any, default: float = 0.0) -> float:
    """
    Convierte un valor a float de manera segura.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int_conversion(value: Any, default: int = 0) -> int:
    """
    Convierte un valor a int de manera segura.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def merge_configs(base_config: Dict, override_config: Dict) -> Dict:
    """
    Combina dos configuraciones, donde override_config sobrescribe base_config.
    """
    merged = base_config.copy()
    
    for key, value in override_config.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    
    return merged

def get_system_info() -> Dict[str, Any]:
    """
    Obtiene información del sistema.
    """
    import platform
    import psutil
    
    try:
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "disk_total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
            "hostname": platform.node()
        }
    except ImportError:
        # Si psutil no está disponible
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": platform.python_version(),
            "hostname": platform.node()
        }

def format_bytes(bytes_value: int) -> str:
    """
    Formatea bytes a string legible.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def calculate_percentile(values: List[float], percentile: float) -> float:
    """
    Calcula el percentil de una lista de valores.
    """
    if not values:
        return 0.0
    
    sorted_values = sorted(values)
    index = (percentile / 100) * (len(sorted_values) - 1)
    
    if index.is_integer():
        return sorted_values[int(index)]
    else:
        lower_index = int(index)
        upper_index = lower_index + 1
        if upper_index >= len(sorted_values):
            return sorted_values[-1]
        
        weight = index - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

def generate_color_palette(count: int) -> List[str]:
    """
    Genera una paleta de colores para gráficos.
    """
    import colorsys
    
    colors = []
    for i in range(count):
        hue = i / count
        rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        hex_color = '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb)
        colors.append(hex_color)
    
    return colors

def retry_operation(operation, max_attempts: int = 3, delay_seconds: float = 1.0):
    """
    Ejecuta una operación con reintentos.
    """
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            return operation()
        except Exception as e:
            last_exception = e
            if attempt < max_attempts - 1:
                time.sleep(delay_seconds * (2 ** attempt))  # Backoff exponencial
    
    raise last_exception

class ColoredFormatter(logging.Formatter):
    """
    Formatter personalizado que añade colores a los logs.
    """
    
    # Códigos de color ANSI
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

def setup_colored_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configura logging con colores.
    """
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Limpiar handlers existentes
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Handler con colores
    console_handler = logging.StreamHandler()
    colored_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)
    
    return logger

def truncate_string(text: str, max_length: int = 50) -> str:
    """
    Trunca un string si es muy largo.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_table_data(headers: List[str], rows: List[List[str]]) -> str:
    """
    Formatea datos en formato tabla.
    """
    try:
        from tabulate import tabulate
        return tabulate(rows, headers=headers, tablefmt="grid")
    except ImportError:
        # Fallback sin tabulate
        result = " | ".join(headers) + "\n"
        result += "-" * len(result) + "\n"
        
        for row in rows:
            result += " | ".join(str(cell) for cell in row) + "\n"
        
        return result
