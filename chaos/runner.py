"""
Ejecutor de experimentos de Chaos Engineering.
Orquesta y coordina la ejecución de múltiples experimentos.
"""

import time
import threading
from typing import Dict, List, Optional, Callable
from enum import Enum
import logging
import uuid

from .experiments import (
    ChaosExperiment, ExperimentType, ExperimentStatus,
    LatencyMonkey, ResourceExhaustionMonkey, NetworkPartitionMonkey,
    ChaosGorilla, ChaosKong, DoctorMonkey
)

logger = logging.getLogger(__name__)

class ExperimentRunnerStatus(Enum):
    """Estados del runner de experimentos"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"

class ExperimentRunner:
    """
    Ejecutor principal de experimentos de Chaos Engineering.
    Maneja la programación, ejecución y coordinación de experimentos.
    """
    
    def __init__(self, name: str = "chaos-experiment-runner"):
        self.name = name
        self.status = ExperimentRunnerStatus.IDLE
        self.target_services = {}
        
        # Gestión de experimentos
        self.active_experiments: Dict[str, ChaosExperiment] = {}
        self.experiment_history: List[Dict] = []
        self.max_concurrent_experiments = 3
        
        # Configuración de seguridad
        self.safety_checks_enabled = True
        self.dry_run_mode = False
        self.require_confirmation = True
        
        # Threading
        self.runner_thread = None
        self.lock = threading.RLock()
        
        # Callbacks
        self.experiment_callbacks = {
            "on_start": [],
            "on_complete": [],
            "on_fail": [],
            "on_cancel": []
        }
        
        # Métricas
        self.total_experiments = 0
        self.successful_experiments = 0
        self.failed_experiments = 0
        
        logger.info(f"ExperimentRunner '{self.name}' inicializado")
    
    def register_service(self, service_name: str, service):
        """Registra un servicio como target para experimentos"""
        with self.lock:
            self.target_services[service_name] = service
            logger.info(f"Servicio '{service_name}' registrado en ExperimentRunner")
    
    def set_safety_mode(self, enabled: bool, dry_run: bool = False, require_confirmation: bool = True):
        """Configura el modo de seguridad"""
        self.safety_checks_enabled = enabled
        self.dry_run_mode = dry_run
        self.require_confirmation = require_confirmation
        
        logger.info(f"Modo seguridad: checks={enabled}, dry_run={dry_run}, confirmation={require_confirmation}")
    
    def create_latency_experiment(self, name: str, target_service: str, 
                                latency_ms: int = 500, duration_seconds: int = 300) -> str:
        """Crea un experimento de latencia"""
        experiment_id = str(uuid.uuid4())[:8]
        experiment = LatencyMonkey(
            name=f"{name}-{experiment_id}",
            target_service=target_service,
            target_services_dict=self.target_services,
            latency_ms=latency_ms,
            duration_seconds=duration_seconds
        )
        
        return self._register_experiment(experiment_id, experiment)
    
    def create_resource_exhaustion_experiment(self, name: str, target_service: str,
                                            resource_type: str = "cpu", 
                                            exhaustion_level: float = 0.9,
                                            duration_seconds: int = 300) -> str:
        """Crea un experimento de agotamiento de recursos"""
        experiment_id = str(uuid.uuid4())[:8]
        experiment = ResourceExhaustionMonkey(
            name=f"{name}-{experiment_id}",
            target_service=target_service,
            target_services_dict=self.target_services,
            resource_type=resource_type,
            exhaustion_level=exhaustion_level,
            duration_seconds=duration_seconds
        )
        
        return self._register_experiment(experiment_id, experiment)
    
    def create_network_partition_experiment(self, name: str, target_service: str,
                                          isolation_type: str = "partial",
                                          duration_seconds: int = 300) -> str:
        """Crea un experimento de partición de red"""
        experiment_id = str(uuid.uuid4())[:8]
        experiment = NetworkPartitionMonkey(
            name=f"{name}-{experiment_id}",
            target_service=target_service,
            target_services_dict=self.target_services,
            isolation_type=isolation_type,
            duration_seconds=duration_seconds
        )
        
        return self._register_experiment(experiment_id, experiment)
    
    def create_chaos_gorilla_experiment(self, name: str, target_zone: str,
                                      duration_seconds: int = 600) -> str:
        """Crea un experimento Chaos Gorilla (falla de datacenter)"""
        experiment_id = str(uuid.uuid4())[:8]
        experiment = ChaosGorilla(
            name=f"{name}-{experiment_id}",
            target_zone=target_zone,
            target_services_dict=self.target_services,
            duration_seconds=duration_seconds
        )
        
        return self._register_experiment(experiment_id, experiment)
    
    def create_chaos_kong_experiment(self, name: str, target_region: str,
                                   duration_seconds: int = 900) -> str:
        """Crea un experimento Chaos Kong (falla regional)"""
        experiment_id = str(uuid.uuid4())[:8]
        experiment = ChaosKong(
            name=f"{name}-{experiment_id}",
            target_region=target_region,
            target_services_dict=self.target_services,
            duration_seconds=duration_seconds
        )
        
        return self._register_experiment(experiment_id, experiment)
    
    def create_doctor_monkey_experiment(self, name: str, duration_seconds: int = 300) -> str:
        """Crea un experimento Doctor Monkey (diagnóstico)"""
        experiment_id = str(uuid.uuid4())[:8]
        experiment = DoctorMonkey(
            name=f"{name}-{experiment_id}",
            target_services_dict=self.target_services,
            duration_seconds=duration_seconds
        )
        
        return self._register_experiment(experiment_id, experiment)
    
    def _register_experiment(self, experiment_id: str, experiment: ChaosExperiment) -> str:
        """Registra un experimento en el runner"""
        with self.lock:
            self.active_experiments[experiment_id] = experiment
            self.total_experiments += 1
            
            logger.info(f"Experimento {experiment.name} registrado con ID {experiment_id}")
            return experiment_id
    
    def start_experiment(self, experiment_id: str) -> bool:
        """Inicia un experimento específico"""
        with self.lock:
            if experiment_id not in self.active_experiments:
                logger.error(f"Experimento {experiment_id} no encontrado")
                return False
            
            experiment = self.active_experiments[experiment_id]
            
            # Verificaciones de seguridad
            if self.safety_checks_enabled and not self._safety_check(experiment):
                logger.error(f"Experimento {experiment_id} falló verificaciones de seguridad")
                return False
            
            # Verificar límite de experimentos concurrentes
            running_experiments = [e for e in self.active_experiments.values() 
                                 if e.status == ExperimentStatus.RUNNING]
            
            if len(running_experiments) >= self.max_concurrent_experiments:
                logger.error(f"Límite de experimentos concurrentes alcanzado ({self.max_concurrent_experiments})")
                return False
            
            # Modo dry run
            if self.dry_run_mode:
                logger.info(f"DRY RUN: Experimento {experiment.name} se ejecutaría normalmente")
                return True
            
            # Ejecutar experimento
            success = experiment.start()
            if success:
                # Monitorear experimento en hilo separado
                monitor_thread = threading.Thread(
                    target=self._monitor_experiment, 
                    args=(experiment_id,), 
                    daemon=True
                )
                monitor_thread.start()
                
                # Notificar callbacks
                self._notify_callbacks("on_start", experiment_id, experiment)
            
            return success
    
    def stop_experiment(self, experiment_id: str) -> bool:
        """Detiene un experimento específico"""
        with self.lock:
            if experiment_id not in self.active_experiments:
                logger.error(f"Experimento {experiment_id} no encontrado")
                return False
            
            experiment = self.active_experiments[experiment_id]
            experiment.stop()
            
            logger.info(f"Experimento {experiment.name} detenido")
            return True
    
    def stop_all_experiments(self):
        """Detiene todos los experimentos activos"""
        with self.lock:
            experiment_ids = list(self.active_experiments.keys())
            
            for experiment_id in experiment_ids:
                self.stop_experiment(experiment_id)
            
            logger.info("Todos los experimentos detenidos")
    
    def _safety_check(self, experiment: ChaosExperiment) -> bool:
        """Realiza verificaciones de seguridad antes de ejecutar un experimento"""
        
        # Verificar que hay servicios registrados
        if not self.target_services:
            logger.error("No hay servicios registrados para experimentos")
            return False
        
        # Verificar que el servicio target existe y está saludable
        if experiment.target_service:
            if experiment.target_service not in self.target_services:
                logger.error(f"Servicio target {experiment.target_service} no registrado")
                return False
            
            service = self.target_services[experiment.target_service]
            healthy_instances = service.get_healthy_instances()
            
            if len(healthy_instances) < service.min_instances + 1:
                logger.warning(f"Servicio {experiment.target_service} tiene {len(healthy_instances)} instancias saludables, "
                             f"mínimo requerido: {service.min_instances + 1}. Permitiendo experimento con precaución.")
                # Solo bloquear si hay muy pocas instancias (menos que el mínimo absoluto)
                if len(healthy_instances) < service.min_instances:
                    logger.error(f"Muy pocas instancias saludables ({len(healthy_instances)} < {service.min_instances})")
                    return False
                # Si tenemos al menos min_instances, permitir el experimento con precaución
        
        # Verificaciones específicas por tipo de experimento
        if experiment.experiment_type == ExperimentType.CHAOS_GORILLA:
            # Verificar que no hay otros experimentos destructivos activos
            destructive_experiments = [
                e for e in self.active_experiments.values()
                if e.experiment_type in [ExperimentType.CHAOS_GORILLA, ExperimentType.CHAOS_KONG]
                and e.status == ExperimentStatus.RUNNING
            ]
            
            if destructive_experiments:
                logger.error("Ya hay experimentos destructivos activos")
                return False
        
        elif experiment.experiment_type == ExperimentType.CHAOS_KONG:
            # Chaos Kong requiere confirmación especial
            if self.require_confirmation:
                logger.warning("Chaos Kong requiere confirmación manual - usar force_experiment()")
                return False
        
        return True
    
    def force_experiment(self, experiment_id: str) -> bool:
        """Fuerza la ejecución de un experimento saltándose verificaciones de seguridad"""
        logger.warning(f"FORZANDO experimento {experiment_id} - SALTANDO VERIFICACIONES DE SEGURIDAD")
        
        old_safety = self.safety_checks_enabled
        old_confirmation = self.require_confirmation
        
        self.safety_checks_enabled = False
        self.require_confirmation = False
        
        result = self.start_experiment(experiment_id)
        
        self.safety_checks_enabled = old_safety
        self.require_confirmation = old_confirmation
        
        return result
    
    def _monitor_experiment(self, experiment_id: str):
        """Monitorea un experimento durante su ejecución"""
        if experiment_id not in self.active_experiments:
            return
        
        experiment = self.active_experiments[experiment_id]
        
        # Esperar a que termine el experimento
        while experiment.status == ExperimentStatus.RUNNING:
            time.sleep(5)
        
        # Mover a historial y limpiar
        with self.lock:
            experiment_status = experiment.get_status()
            self.experiment_history.append(experiment_status)
            
            # Actualizar métricas
            if experiment.status == ExperimentStatus.COMPLETED:
                self.successful_experiments += 1
                self._notify_callbacks("on_complete", experiment_id, experiment)
            elif experiment.status == ExperimentStatus.FAILED:
                self.failed_experiments += 1
                self._notify_callbacks("on_fail", experiment_id, experiment)
            elif experiment.status == ExperimentStatus.CANCELLED:
                self._notify_callbacks("on_cancel", experiment_id, experiment)
            
            # Remover de experimentos activos
            del self.active_experiments[experiment_id]
            
            # Mantener solo últimos 50 experimentos en historial
            if len(self.experiment_history) > 50:
                self.experiment_history.pop(0)
        
        logger.info(f"Monitoreo de experimento {experiment.name} completado")
    
    def _notify_callbacks(self, event_type: str, experiment_id: str, experiment: ChaosExperiment):
        """Notifica a los callbacks registrados"""
        for callback in self.experiment_callbacks[event_type]:
            try:
                callback(experiment_id, experiment)
            except Exception as e:
                logger.error(f"Error en callback {event_type}: {e}")
    
    def add_callback(self, event_type: str, callback: Callable):
        """Añade un callback para eventos de experimentos"""
        if event_type in self.experiment_callbacks:
            self.experiment_callbacks[event_type].append(callback)
        else:
            logger.error(f"Tipo de evento inválido: {event_type}")
    
    def get_experiment_status(self, experiment_id: str) -> Optional[Dict]:
        """Obtiene el estado de un experimento específico"""
        if experiment_id in self.active_experiments:
            return self.active_experiments[experiment_id].get_status()
        
        # Buscar en historial
        for experiment_data in self.experiment_history:
            if experiment_data.get("name", "").endswith(experiment_id):
                return experiment_data
        
        return None
    
    def get_all_experiments_status(self) -> Dict:
        """Obtiene el estado de todos los experimentos"""
        with self.lock:
            active = {
                exp_id: experiment.get_status()
                for exp_id, experiment in self.active_experiments.items()
            }
            
            return {
                "runner_status": self.status.value,
                "active_experiments": active,
                "experiment_history": self.experiment_history[-10:],  # Últimos 10
                "statistics": {
                    "total_experiments": self.total_experiments,
                    "successful_experiments": self.successful_experiments,
                    "failed_experiments": self.failed_experiments,
                    "success_rate": (self.successful_experiments / max(1, self.total_experiments)) * 100
                }
            }
    
    def create_experiment_batch(self, batch_config: List[Dict]) -> List[str]:
        """
        Crea un lote de experimentos basado en configuración.
        Útil para ejecutar múltiples experimentos coordinados.
        """
        experiment_ids = []
        
        for config in batch_config:
            experiment_type = config.get("type")
            name = config.get("name", "batch-experiment")
            
            try:
                if experiment_type == "latency":
                    exp_id = self.create_latency_experiment(
                        name=name,
                        target_service=config["target_service"],
                        latency_ms=config.get("latency_ms", 500),
                        duration_seconds=config.get("duration_seconds", 300)
                    )
                elif experiment_type == "resource_exhaustion":
                    exp_id = self.create_resource_exhaustion_experiment(
                        name=name,
                        target_service=config["target_service"],
                        resource_type=config.get("resource_type", "cpu"),
                        exhaustion_level=config.get("exhaustion_level", 0.9),
                        duration_seconds=config.get("duration_seconds", 300)
                    )
                elif experiment_type == "network_partition":
                    exp_id = self.create_network_partition_experiment(
                        name=name,
                        target_service=config["target_service"],
                        isolation_type=config.get("isolation_type", "partial"),
                        duration_seconds=config.get("duration_seconds", 300)
                    )
                elif experiment_type == "doctor_monkey":
                    exp_id = self.create_doctor_monkey_experiment(
                        name=name,
                        duration_seconds=config.get("duration_seconds", 300)
                    )
                else:
                    logger.error(f"Tipo de experimento desconocido: {experiment_type}")
                    continue
                
                experiment_ids.append(exp_id)
                
            except Exception as e:
                logger.error(f"Error creando experimento {name}: {e}")
        
        logger.info(f"Lote de {len(experiment_ids)} experimentos creado")
        return experiment_ids
    
    def start_experiment_batch(self, experiment_ids: List[str], stagger_seconds: int = 30) -> bool:
        """
        Inicia un lote de experimentos con retraso entre cada uno.
        """
        def start_batch():
            for i, exp_id in enumerate(experiment_ids):
                if i > 0:
                    time.sleep(stagger_seconds)
                
                success = self.start_experiment(exp_id)
                if not success:
                    logger.error(f"Error iniciando experimento {exp_id} en lote")
        
        batch_thread = threading.Thread(target=start_batch, daemon=True)
        batch_thread.start()
        
        logger.info(f"Iniciando lote de {len(experiment_ids)} experimentos con retraso de {stagger_seconds}s")
        return True
    
    def emergency_stop(self):
        """Parada de emergencia - detiene todos los experimentos inmediatamente"""
        logger.critical("🚨 PARADA DE EMERGENCIA - Deteniendo todos los experimentos")
        
        self.status = ExperimentRunnerStatus.STOPPING
        
        # Detener todos los experimentos activos
        with self.lock:
            for experiment in self.active_experiments.values():
                try:
                    experiment.stop()
                except Exception as e:
                    logger.error(f"Error en parada de emergencia: {e}")
        
        self.status = ExperimentRunnerStatus.IDLE
        logger.info("Parada de emergencia completada")
    
    def get_runner_metrics(self) -> Dict:
        """Obtiene métricas del runner"""
        with self.lock:
            active_count = len(self.active_experiments)
            running_count = len([e for e in self.active_experiments.values() 
                               if e.status == ExperimentStatus.RUNNING])
            
            return {
                "runner_name": self.name,
                "status": self.status.value,
                "active_experiments": active_count,
                "running_experiments": running_count,
                "total_experiments": self.total_experiments,
                "successful_experiments": self.successful_experiments,
                "failed_experiments": self.failed_experiments,
                "success_rate": (self.successful_experiments / max(1, self.total_experiments)) * 100,
                "registered_services": len(self.target_services),
                "safety_settings": {
                    "safety_checks_enabled": self.safety_checks_enabled,
                    "dry_run_mode": self.dry_run_mode,
                    "require_confirmation": self.require_confirmation,
                    "max_concurrent_experiments": self.max_concurrent_experiments
                }
            }
