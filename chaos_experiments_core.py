#!/usr/bin/env python3
"""
Sistema centralizado de experimentos de Chaos Engineering.
Este módulo unifica y simplifica todos los experimentos de chaos.
"""

import time
import threading
import logging
import random
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Importaciones locales
from core.service import Service, ServiceType
from core.load_balancer import LoadBalancer
from core.monitoring import MonitoringSystem
from utils.helpers import format_timestamp, format_duration

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# TIPOS Y CONFIGURACIONES CENTRALIZADAS
# ═══════════════════════════════════════════════════════════════════

class ExperimentType(Enum):
    """Tipos de experimentos disponibles simplificados."""
    LATENCY = "latency"
    TERMINATION = "termination"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    NETWORK_PARTITION = "network_partition"
    HEALTH_CHECK = "health_check"

class ExperimentStatus(Enum):
    """Estados de un experimento."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class ExperimentConfig:
    """Configuración centralizada para experimentos."""
    name: str
    experiment_type: ExperimentType
    target_service: Optional[str] = None
    duration_seconds: int = 120
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}

@dataclass
class ExperimentResult:
    """Resultado estandarizado de experimentos."""
    experiment_id: str
    name: str
    experiment_type: ExperimentType
    status: ExperimentStatus
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    results: Dict[str, Any] = None
    error_message: Optional[str] = None
    
    def __post_init__(self):
        if self.results is None:
            self.results = {}
        if self.end_time and self.start_time:
            self.duration = self.end_time - self.start_time

# ═══════════════════════════════════════════════════════════════════
# EXPERIMENTO BASE SIMPLIFICADO
# ═══════════════════════════════════════════════════════════════════

class BaseExperiment(ABC):
    """Clase base simplificada para todos los experimentos."""
    
    def __init__(self, config: ExperimentConfig, services: Dict[str, Service]):
        self.config = config
        self.services = services
        self.status = ExperimentStatus.PENDING
        self.start_time = time.time()
        self.end_time = None
        self.results = {}
        self.error_message = None
        self.should_stop = threading.Event()
        
        # Validar que el servicio objetivo existe
        if config.target_service and config.target_service not in services:
            raise ValueError(f"Servicio objetivo '{config.target_service}' no encontrado")
        
        logger.info(f"🧪 Experimento '{config.name}' creado: {config.experiment_type.value}")
    
    def start(self) -> bool:
        """Inicia el experimento."""
        if self.status != ExperimentStatus.PENDING:
            logger.warning(f"Experimento {self.config.name} no está en estado PENDING")
            return False
        
        self.status = ExperimentStatus.RUNNING
        self.start_time = time.time()
        
        # Ejecutar en hilo separado
        experiment_thread = threading.Thread(target=self._run_experiment, daemon=True)
        experiment_thread.start()
        
        logger.info(f"🚀 Experimento '{self.config.name}' INICIADO")
        return True
    
    def stop(self):
        """Detiene el experimento."""
        self.should_stop.set()
        if self.status == ExperimentStatus.RUNNING:
            self.status = ExperimentStatus.CANCELLED
            self.end_time = time.time()
        logger.info(f"🛑 Experimento '{self.config.name}' DETENIDO")
    
    def _run_experiment(self):
        """Ejecuta el experimento con manejo de errores."""
        try:
            self.execute()
            if not self.should_stop.is_set():
                self.status = ExperimentStatus.COMPLETED
        except Exception as e:
            self.status = ExperimentStatus.FAILED
            self.error_message = str(e)
            logger.error(f"❌ Experimento {self.config.name} falló: {e}")
        finally:
            self.end_time = time.time()
            self.cleanup()
    
    @abstractmethod
    def execute(self):
        """Implementar la lógica específica del experimento."""
        pass
    
    def cleanup(self):
        """Limpieza después del experimento."""
        pass
    
    def get_result(self) -> ExperimentResult:
        """Obtiene el resultado del experimento."""
        return ExperimentResult(
            experiment_id=f"{self.config.name}-{id(self)}",
            name=self.config.name,
            experiment_type=self.config.experiment_type,
            status=self.status,
            start_time=self.start_time,
            end_time=self.end_time,
            results=self.results,
            error_message=self.error_message
        )

# ═══════════════════════════════════════════════════════════════════
# EXPERIMENTOS ESPECÍFICOS SIMPLIFICADOS
# ═══════════════════════════════════════════════════════════════════

class LatencyExperiment(BaseExperiment):
    """Experimento de latencia simplificado."""
    
    def execute(self):
        target_service = self.services[self.config.target_service]
        latency_ms = self.config.parameters.get('latency_ms', 500)
        
        logger.info(f"🌐 Añadiendo {latency_ms}ms latencia a {self.config.target_service}")
        
        # Aplicar latencia
        original_latencies = {}
        for instance_id, instance in target_service.instances.items():
            original_latencies[instance_id] = instance.base_response_time
            instance.base_response_time += latency_ms
        
        start_time = time.time()
        end_time = start_time + self.config.duration_seconds
        
        # Monitorear durante la duración
        while time.time() < end_time and not self.should_stop.is_set():
            time.sleep(5)
        
        # Restaurar latencias originales
        for instance_id, original_latency in original_latencies.items():
            if instance_id in target_service.instances:
                target_service.instances[instance_id].base_response_time = original_latency
        
        self.results = {
            'target_service': self.config.target_service,
            'latency_added_ms': latency_ms,
            'duration_seconds': time.time() - start_time,
            'instances_affected': len(original_latencies)
        }

class TerminationExperiment(BaseExperiment):
    """Experimento de terminación de instancias."""
    
    def execute(self):
        if self.config.target_service:
            target_service = self.services[self.config.target_service]
        else:
            # Seleccionar servicio aleatorio
            target_service = random.choice(list(self.services.values()))
        
        # Encontrar instancia para terminar
        healthy_instances = target_service.get_healthy_instances()
        if len(healthy_instances) <= target_service.min_instances:
            raise Exception(f"No se puede terminar instancia: {target_service.name} tiene {len(healthy_instances)} instancias saludables (mínimo: {target_service.min_instances})")
        
        # Terminar una instancia aleatoria
        instance_to_kill = random.choice(healthy_instances)
        instance_id = instance_to_kill.instance_id
        
        logger.info(f"💀 Terminando instancia {instance_id} del servicio {target_service.name}")
        instance_to_kill.terminate()
        
        self.results = {
            'target_service': target_service.name,
            'terminated_instance': instance_id,
            'remaining_instances': len(target_service.get_healthy_instances())
        }

class ResourceExhaustionExperiment(BaseExperiment):
    """Experimento de agotamiento de recursos."""
    
    def execute(self):
        target_service = self.services[self.config.target_service]
        resource_type = self.config.parameters.get('resource_type', 'cpu')
        exhaustion_level = self.config.parameters.get('exhaustion_level', 0.8)
        
        logger.info(f"💾 Agotando {resource_type} al {exhaustion_level*100}% en {self.config.target_service}")
        
        # Aplicar agotamiento
        affected_instances = []
        for instance in target_service.get_healthy_instances():
            if resource_type == 'cpu':
                instance.metrics.cpu_usage = exhaustion_level * 100
            elif resource_type == 'memory':
                instance.metrics.memory_usage = exhaustion_level * 100
            affected_instances.append(instance.instance_id)
        
        start_time = time.time()
        end_time = start_time + self.config.duration_seconds
        
        # Mantener agotamiento durante la duración
        while time.time() < end_time and not self.should_stop.is_set():
            time.sleep(10)
        
        # Restaurar recursos
        for instance in target_service.instances.values():
            if resource_type == 'cpu':
                instance.metrics.cpu_usage = random.uniform(10, 30)
            elif resource_type == 'memory':
                instance.metrics.memory_usage = random.uniform(20, 40)
        
        self.results = {
            'target_service': self.config.target_service,
            'resource_type': resource_type,
            'exhaustion_level': exhaustion_level,
            'duration_seconds': time.time() - start_time,
            'instances_affected': len(affected_instances)
        }

class HealthCheckExperiment(BaseExperiment):
    """Experimento de diagnóstico del sistema."""
    
    def execute(self):
        logger.info("🩺 Ejecutando diagnóstico completo del sistema")
        
        health_report = {}
        total_instances = 0
        healthy_instances = 0
        
        # Analizar cada servicio
        for service_name, service in self.services.items():
            instances = list(service.instances.values())
            healthy = service.get_healthy_instances()
            
            service_health = {
                'total_instances': len(instances),
                'healthy_instances': len(healthy),
                'availability': (len(healthy) / len(instances)) * 100 if instances else 0,
                'avg_response_time': sum(i.base_response_time for i in healthy) / len(healthy) if healthy else 0,
                'avg_cpu_usage': sum(i.metrics.cpu_usage for i in instances) / len(instances) if instances else 0,
                'avg_memory_usage': sum(i.metrics.memory_usage for i in instances) / len(instances) if instances else 0
            }
            
            health_report[service_name] = service_health
            total_instances += len(instances)
            healthy_instances += len(healthy)
        
        # Calcular salud general del sistema
        overall_health = (healthy_instances / total_instances) * 100 if total_instances > 0 else 0
        
        # Determinar estado del sistema
        if overall_health >= 90:
            system_status = "EXCELENTE"
        elif overall_health >= 70:
            system_status = "BUENO"
        elif overall_health >= 50:
            system_status = "DEGRADADO"
        else:
            system_status = "CRÍTICO"
        
        self.results = {
            'system_status': system_status,
            'overall_health': overall_health,
            'total_instances': total_instances,
            'healthy_instances': healthy_instances,
            'services_health': health_report,
            'diagnosis_timestamp': format_timestamp()
        }
        
        logger.info(f"📊 Diagnóstico completado - Estado: {system_status} ({overall_health:.1f}%)")

# ═══════════════════════════════════════════════════════════════════
# GESTOR CENTRALIZADO DE EXPERIMENTOS
# ═══════════════════════════════════════════════════════════════════

class ChaosExperimentManager:
    """Gestor centralizado y simplificado de experimentos de chaos."""
    
    def __init__(self, services: Dict[str, Service]):
        self.services = services
        self.active_experiments: Dict[str, BaseExperiment] = {}
        self.completed_experiments: List[ExperimentResult] = []
        self.lock = threading.RLock()
        
        # Configuración de seguridad
        self.max_concurrent_experiments = 3
        self.safety_checks_enabled = True
        
        logger.info("🔥 ChaosExperimentManager inicializado")
    
    def create_and_run_experiment(self, config: ExperimentConfig) -> str:
        """Crea y ejecuta un experimento inmediatamente."""
        experiment_id = f"{config.name}-{int(time.time())}"
        
        # Verificaciones de seguridad
        if self.safety_checks_enabled:
            if not self._safety_check(config):
                raise Exception("Experimento falló verificaciones de seguridad")
        
        # Verificar límite de experimentos concurrentes
        with self.lock:
            if len(self.active_experiments) >= self.max_concurrent_experiments:
                raise Exception(f"Límite de experimentos concurrentes alcanzado ({self.max_concurrent_experiments})")
        
        # Crear experimento
        experiment = self._create_experiment(config)
        
        # Registrar y ejecutar
        with self.lock:
            self.active_experiments[experiment_id] = experiment
        
        if experiment.start():
            # Monitorear en hilo separado
            monitor_thread = threading.Thread(
                target=self._monitor_experiment, 
                args=(experiment_id,), 
                daemon=True
            )
            monitor_thread.start()
            
            logger.info(f"✅ Experimento {experiment_id} iniciado exitosamente")
            return experiment_id
        else:
            # Limpiar si falló el inicio
            with self.lock:
                del self.active_experiments[experiment_id]
            raise Exception("Error iniciando experimento")
    
    def _create_experiment(self, config: ExperimentConfig) -> BaseExperiment:
        """Factory method para crear experimentos."""
        if config.experiment_type == ExperimentType.LATENCY:
            return LatencyExperiment(config, self.services)
        elif config.experiment_type == ExperimentType.TERMINATION:
            return TerminationExperiment(config, self.services)
        elif config.experiment_type == ExperimentType.RESOURCE_EXHAUSTION:
            return ResourceExhaustionExperiment(config, self.services)
        elif config.experiment_type == ExperimentType.HEALTH_CHECK:
            return HealthCheckExperiment(config, self.services)
        else:
            raise ValueError(f"Tipo de experimento no soportado: {config.experiment_type}")
    
    def _safety_check(self, config: ExperimentConfig) -> bool:
        """Verificaciones de seguridad simplificadas."""
        # Verificar que hay servicios
        if not self.services:
            logger.error("No hay servicios registrados")
            return False
        
        # Verificar servicio objetivo si es especificado
        if config.target_service:
            if config.target_service not in self.services:
                logger.error(f"Servicio objetivo {config.target_service} no encontrado")
                return False
            
            service = self.services[config.target_service]
            healthy_instances = service.get_healthy_instances()
            
            # Para experimentos de terminación, verificar instancias mínimas
            if config.experiment_type == ExperimentType.TERMINATION:
                if len(healthy_instances) <= service.min_instances:
                    logger.error(f"Servicio {config.target_service} no tiene suficientes instancias para terminación")
                    return False
        
        return True
    
    def _monitor_experiment(self, experiment_id: str):
        """Monitorea un experimento hasta su finalización."""
        experiment = self.active_experiments.get(experiment_id)
        if not experiment:
            return
        
        # Esperar a que termine
        while experiment.status == ExperimentStatus.RUNNING:
            time.sleep(5)
        
        # Mover a historial
        with self.lock:
            result = experiment.get_result()
            self.completed_experiments.append(result)
            
            # Limpiar de experimentos activos
            if experiment_id in self.active_experiments:
                del self.active_experiments[experiment_id]
        
        logger.info(f"📋 Experimento {experiment.config.name} completado con estado: {experiment.status.value}")
    
    def stop_experiment(self, experiment_id: str) -> bool:
        """Detiene un experimento específico."""
        with self.lock:
            if experiment_id not in self.active_experiments:
                logger.error(f"Experimento {experiment_id} no encontrado")
                return False
            
            experiment = self.active_experiments[experiment_id]
            experiment.stop()
            return True
    
    def stop_all_experiments(self):
        """Detiene todos los experimentos activos."""
        with self.lock:
            for experiment in self.active_experiments.values():
                experiment.stop()
        logger.info("🛑 Todos los experimentos detenidos")
    
    def get_experiment_status(self, experiment_id: str) -> Optional[Dict]:
        """Obtiene el estado de un experimento."""
        with self.lock:
            if experiment_id in self.active_experiments:
                result = self.active_experiments[experiment_id].get_result()
                return {
                    'name': result.name,
                    'type': result.experiment_type.value,
                    'status': result.status.value,
                    'duration': result.duration,
                    'results': result.results
                }
            
            # Buscar en historial
            for result in self.completed_experiments:
                if result.experiment_id == experiment_id:
                    return {
                        'name': result.name,
                        'type': result.experiment_type.value,
                        'status': result.status.value,
                        'duration': result.duration,
                        'results': result.results
                    }
        
        return None
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen del estado del sistema de experimentos."""
        with self.lock:
            return {
                'active_experiments': len(self.active_experiments),
                'completed_experiments': len(self.completed_experiments),
                'success_rate': self._calculate_success_rate(),
                'registered_services': len(self.services),
                'safety_enabled': self.safety_checks_enabled
            }
    
    def _calculate_success_rate(self) -> float:
        """Calcula la tasa de éxito de experimentos."""
        if not self.completed_experiments:
            return 100.0
        
        successful = sum(1 for result in self.completed_experiments 
                        if result.status == ExperimentStatus.COMPLETED)
        return (successful / len(self.completed_experiments)) * 100

# ═══════════════════════════════════════════════════════════════════
# FUNCIONES DE CONVENIENCIA PARA EXPERIMENTOS COMUNES
# ═══════════════════════════════════════════════════════════════════

def create_latency_experiment(name: str, target_service: str, latency_ms: int = 500, 
                            duration_seconds: int = 120) -> ExperimentConfig:
    """Crea configuración para experimento de latencia."""
    return ExperimentConfig(
        name=name,
        experiment_type=ExperimentType.LATENCY,
        target_service=target_service,
        duration_seconds=duration_seconds,
        parameters={'latency_ms': latency_ms}
    )

def create_termination_experiment(name: str, target_service: str = None) -> ExperimentConfig:
    """Crea configuración para experimento de terminación."""
    return ExperimentConfig(
        name=name,
        experiment_type=ExperimentType.TERMINATION,
        target_service=target_service,
        duration_seconds=1  # Terminación es instantánea
    )

def create_resource_experiment(name: str, target_service: str, resource_type: str = 'cpu',
                             exhaustion_level: float = 0.8, duration_seconds: int = 120) -> ExperimentConfig:
    """Crea configuración para experimento de recursos."""
    return ExperimentConfig(
        name=name,
        experiment_type=ExperimentType.RESOURCE_EXHAUSTION,
        target_service=target_service,
        duration_seconds=duration_seconds,
        parameters={
            'resource_type': resource_type,
            'exhaustion_level': exhaustion_level
        }
    )

def create_health_check_experiment(name: str, duration_seconds: int = 60) -> ExperimentConfig:
    """Crea configuración para experimento de diagnóstico."""
    return ExperimentConfig(
        name=name,
        experiment_type=ExperimentType.HEALTH_CHECK,
        duration_seconds=duration_seconds
    )
