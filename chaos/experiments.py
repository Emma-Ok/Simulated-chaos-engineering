"""
Experimentos de Chaos Engineering.
Implementa diferentes tipos de fallas y experimentos.
"""

import random
import time
import threading
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ExperimentType(Enum):
    """Tipos de experimentos disponibles"""
    INSTANCE_TERMINATION = "instance_termination"
    NETWORK_LATENCY = "network_latency"
    NETWORK_PARTITION = "network_partition"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    DATABASE_FAILURE = "database_failure"
    DEPENDENCY_FAILURE = "dependency_failure"
    CHAOS_GORILLA = "chaos_gorilla"
    CHAOS_KONG = "chaos_kong"

class ExperimentStatus(Enum):
    """Estados de un experimento"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ChaosExperiment:
    """Clase base para experimentos de chaos"""
    
    def __init__(self, name: str, experiment_type: ExperimentType, 
                 target_service: str = None, duration_seconds: int = 300):
        self.name = name
        self.experiment_type = experiment_type
        self.target_service = target_service
        self.duration_seconds = duration_seconds
        self.status = ExperimentStatus.PENDING
        
        # Timestamps
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None
        
        # Resultados
        self.results = {}
        self.error_message = None
        
        # Threading
        self.experiment_thread = None
        self.should_stop = threading.Event()
        
        logger.info(f"Experimento '{name}' creado: {experiment_type.value}")
    
    def start(self) -> bool:
        """Inicia el experimento"""
        if self.status != ExperimentStatus.PENDING:
            logger.warning(f"Experimento {self.name} no está en estado PENDING")
            return False
        
        self.status = ExperimentStatus.RUNNING
        self.started_at = time.time()
        
        # Ejecutar experimento en hilo separado
        self.experiment_thread = threading.Thread(target=self._run_experiment, daemon=True)
        self.experiment_thread.start()
        
        logger.info(f"🧪 Experimento '{self.name}' INICIADO")
        return True
    
    def stop(self):
        """Detiene el experimento"""
        self.should_stop.set()
        if self.experiment_thread:
            self.experiment_thread.join(timeout=10)
        
        if self.status == ExperimentStatus.RUNNING:
            self.status = ExperimentStatus.CANCELLED
            self.completed_at = time.time()
        
        logger.info(f"🧪 Experimento '{self.name}' DETENIDO")
    
    def _run_experiment(self):
        """Ejecuta el experimento (implementado en subclases)"""
        try:
            self.execute()
            if not self.should_stop.is_set():
                self.status = ExperimentStatus.COMPLETED
        except Exception as e:
            self.status = ExperimentStatus.FAILED
            self.error_message = str(e)
            logger.error(f"Experimento {self.name} falló: {e}")
        finally:
            self.completed_at = time.time()
            self.cleanup()
    
    def execute(self):
        """Implementar en subclases"""
        raise NotImplementedError
    
    def cleanup(self):
        """Limpieza después del experimento"""
        pass
    
    def get_status(self) -> Dict:
        """Retorna el estado del experimento"""
        runtime = None
        if self.started_at:
            end_time = self.completed_at or time.time()
            runtime = end_time - self.started_at
        
        return {
            "name": self.name,
            "type": self.experiment_type.value,
            "target_service": self.target_service,
            "status": self.status.value,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "runtime_seconds": runtime,
            "results": self.results,
            "error_message": self.error_message
        }

class LatencyMonkey(ChaosExperiment):
    """
    Introduce latencia variable en servicios.
    Simula problemas de red o sobrecarga.
    """
    
    def __init__(self, name: str, target_service: str, target_services_dict: Dict,
                 latency_ms: int = 500, variance_ms: int = 100, duration_seconds: int = 300):
        super().__init__(name, ExperimentType.NETWORK_LATENCY, target_service, duration_seconds)
        self.target_services_dict = target_services_dict
        self.latency_ms = latency_ms
        self.variance_ms = variance_ms
        self.original_latencies = {}
    
    def execute(self):
        """Introduce latencia en el servicio target"""
        if self.target_service not in self.target_services_dict:
            raise ValueError(f"Servicio {self.target_service} no encontrado")
        
        service = self.target_services_dict[self.target_service]
        
        # Guardar latencias originales
        for instance_id, instance in service.instances.items():
            self.original_latencies[instance_id] = instance.base_response_time
        
        logger.info(f"💥 LATENCY MONKEY: Introduciendo {self.latency_ms}ms latencia "
                   f"en {self.target_service}")
        
        # Aplicar latencia
        service.chaos_introduce_latency(self.latency_ms)
        
        # Monitorear durante la duración
        start_time = time.time()
        affected_requests = 0
        
        while not self.should_stop.is_set() and time.time() - start_time < self.duration_seconds:
            # Variar la latencia dinámicamente
            current_latency = self.latency_ms + random.randint(-self.variance_ms, self.variance_ms)
            current_latency = max(0, current_latency)
            
            # Aplicar nueva latencia a instancias aleatorias
            healthy_instances = service.get_healthy_instances()
            if healthy_instances:
                target_instance = random.choice(healthy_instances)
                additional_latency = current_latency - self.latency_ms
                target_instance.introduce_latency(additional_latency)
                affected_requests += 1
            
            time.sleep(10)  # Revisar cada 10 segundos
        
        self.results = {
            "latency_introduced_ms": self.latency_ms,
            "variance_ms": self.variance_ms,
            "affected_requests": affected_requests,
            "affected_instances": len(self.original_latencies)
        }
    
    def cleanup(self):
        """Restaura las latencias originales"""
        if self.target_service in self.target_services_dict:
            service = self.target_services_dict[self.target_service]
            
            # Restaurar latencias originales
            for instance_id, original_latency in self.original_latencies.items():
                if instance_id in service.instances:
                    service.instances[instance_id].base_response_time = original_latency
            
            logger.info(f"🔧 Latencias restauradas en {self.target_service}")

class ResourceExhaustionMonkey(ChaosExperiment):
    """
    Simula agotamiento de recursos (CPU, memoria).
    """
    
    def __init__(self, name: str, target_service: str, target_services_dict: Dict,
                 resource_type: str = "cpu", exhaustion_level: float = 0.9, 
                 duration_seconds: int = 300):
        super().__init__(name, ExperimentType.RESOURCE_EXHAUSTION, target_service, duration_seconds)
        self.target_services_dict = target_services_dict
        self.resource_type = resource_type  # "cpu" o "memory"
        self.exhaustion_level = exhaustion_level  # 0.0 - 1.0
        self.affected_instances = []
    
    def execute(self):
        """Simula agotamiento de recursos"""
        if self.target_service not in self.target_services_dict:
            raise ValueError(f"Servicio {self.target_service} no encontrado")
        
        service = self.target_services_dict[self.target_service]
        healthy_instances = service.get_healthy_instances()
        
        if not healthy_instances:
            raise ValueError(f"No hay instancias saludables en {self.target_service}")
        
        # Seleccionar instancia para agotar recursos
        target_instance = random.choice(healthy_instances)
        self.affected_instances.append(target_instance.instance_id)
        
        logger.warning(f"💥 RESOURCE EXHAUSTION: Agotando {self.resource_type} "
                      f"en instancia {target_instance.instance_id}")
        
        # Simular agotamiento de recursos con niveles más conservadores
        if self.resource_type == "cpu":
            # Simular alto uso de CPU (más conservador)
            target_instance.metrics.cpu_usage = min(85, self.exhaustion_level * 100)  # Máximo 85%
            target_instance.introduce_latency(200)  # Latencia moderada por CPU alto
            logger.info(f"💥 CPU usage aumentado a {target_instance.metrics.cpu_usage}% en {target_instance.instance_id}")
        elif self.resource_type == "memory":
            # Simular alto uso de memoria
            target_instance.metrics.memory_usage = min(90, self.exhaustion_level * 100)  # Máximo 90%
            target_instance.introduce_latency(150)  # Latencia por swapping
            logger.info(f"💥 Memory usage aumentado a {target_instance.metrics.memory_usage}% en {target_instance.instance_id}")
        
        # Introducir errores ocasionales pero no masivos
        original_error_rate = target_instance.error_probability
        target_instance.introduce_errors(min(0.05, original_error_rate * 5))  # Máximo 5%
        
        # Mantener el agotamiento durante la duración especificada
        start_time = time.time()
        while not self.should_stop.is_set() and time.time() - start_time < self.duration_seconds:
            time.sleep(10)  # Verificar cada 10 segundos
        
        self.results = {
            "target_service": self.target_service,
            "target_instance": target_instance.instance_id,
            "resource_type": self.resource_type,
            "exhaustion_level": self.exhaustion_level,
            "duration_seconds": time.time() - start_time,
            "final_cpu_usage": target_instance.metrics.cpu_usage,
            "final_memory_usage": target_instance.metrics.memory_usage,
            "errors_introduced": target_instance.error_probability
        }
    
    def cleanup(self):
        """Restaura los niveles de recursos"""
        if self.target_service in self.target_services_dict:
            service = self.target_services_dict[self.target_service]
            
            for instance_id in self.affected_instances:
                if instance_id in service.instances:
                    instance = service.instances[instance_id]
                    # Restaurar métricas normales
                    instance.metrics.cpu_usage = random.uniform(20, 40)
                    instance.metrics.memory_usage = random.uniform(30, 50)
                    # Restaurar tiempo de respuesta
                    instance.base_response_time = random.uniform(50, 200)
                    
                    if instance.status.value == "degraded":
                        instance.set_status(instance.status.__class__.HEALTHY)
            
            logger.info(f"🔧 Recursos restaurados en {self.target_service}")

class NetworkPartitionMonkey(ChaosExperiment):
    """
    Simula particiones de red aislando servicios.
    """
    
    def __init__(self, name: str, target_service: str, target_services_dict: Dict,
                 isolation_type: str = "partial", duration_seconds: int = 300):
        super().__init__(name, ExperimentType.NETWORK_PARTITION, target_service, duration_seconds)
        self.target_services_dict = target_services_dict
        self.isolation_type = isolation_type  # "partial" o "complete"
        self.isolated_instances = []
    
    def execute(self):
        """Simula partición de red"""
        if self.target_service not in self.target_services_dict:
            raise ValueError(f"Servicio {self.target_service} no encontrado")
        
        service = self.target_services_dict[self.target_service]
        healthy_instances = service.get_healthy_instances()
        
        if not healthy_instances:
            raise ValueError(f"No hay instancias saludables en {self.target_service}")
        
        # Seleccionar instancias a aislar
        if self.isolation_type == "partial":
            # Aislar ~30% de las instancias
            instances_to_isolate = random.sample(healthy_instances, 
                                               max(1, len(healthy_instances) // 3))
        else:
            # Aislamiento completo
            instances_to_isolate = healthy_instances
        
        logger.warning(f"💥 NETWORK PARTITION: Aislando {len(instances_to_isolate)} "
                      f"instancias de {self.target_service}")
        
        # Simular aislamiento con configuración más moderada
        for instance in instances_to_isolate:
            self.isolated_instances.append(instance.instance_id)
            # Simular pérdida de conectividad moderada (no extrema)
            original_error_rate = instance.error_probability
            instance.error_probability = min(0.3, original_error_rate * 10)  # Máximo 30% en lugar de 80%
            instance.introduce_latency(2000)  # 2 segundos en lugar de 10
        
        logger.info(f"🌐 Partición aplicada a {len(instances_to_isolate)} instancias")
        
        # Mantener aislamiento durante la duración
        start_time = time.time()
        while not self.should_stop.is_set() and time.time() - start_time < self.duration_seconds:
            time.sleep(15)  # Verificar cada 15 segundos
        
        self.results = {
            "target_service": self.target_service,
            "isolation_type": self.isolation_type,
            "isolated_instances": self.isolated_instances,
            "duration_seconds": time.time() - start_time,
            "affected_count": len(instances_to_isolate)
        }
    
    def cleanup(self):
        """Restaura la conectividad"""
        if self.target_service in self.target_services_dict:
            service = self.target_services_dict[self.target_service]
            
            for instance_id in self.isolated_instances:
                if instance_id in service.instances:
                    instance = service.instances[instance_id]
                    # Restaurar conectividad
                    instance.error_probability = 0.01
                    instance.base_response_time = random.uniform(50, 200)
            
            logger.info(f"🔧 Conectividad restaurada en {self.target_service}")

class ChaosGorilla(ChaosExperiment):
    """
    Simula la falla de un datacenter completo.
    Termina todas las instancias de una zona/región.
    """
    
    def __init__(self, name: str, target_zone: str, target_services_dict: Dict,
                 duration_seconds: int = 600):
        super().__init__(name, ExperimentType.CHAOS_GORILLA, None, duration_seconds)
        self.target_zone = target_zone
        self.target_services_dict = target_services_dict
        self.affected_services = []
        self.terminated_instances = {}
    
    def execute(self):
        """Simula falla de datacenter"""
        logger.critical(f"🦍 CHAOS GORILLA: Simulando falla de datacenter {self.target_zone}")
        
        # Terminar instancias en la zona target
        for service_name, service in self.target_services_dict.items():
            terminated_in_service = []
            
            for instance_id, instance in service.instances.items():
                if instance.region == self.target_zone:
                    instance.terminate()
                    terminated_in_service.append(instance_id)
            
            if terminated_in_service:
                self.affected_services.append(service_name)
                self.terminated_instances[service_name] = terminated_in_service
        
        # Monitorear recuperación
        start_time = time.time()
        recovery_times = {}
        
        while not self.should_stop.is_set() and time.time() - start_time < self.duration_seconds:
            # Verificar si servicios se están recuperando
            for service_name in self.affected_services:
                if service_name not in recovery_times:
                    service = self.target_services_dict[service_name]
                    healthy_instances = service.get_healthy_instances()
                    
                    if len(healthy_instances) >= service.min_instances:
                        recovery_times[service_name] = time.time() - start_time
                        logger.info(f"🔧 Servicio {service_name} recuperado en {recovery_times[service_name]:.1f}s")
            
            time.sleep(10)
        
        self.results = {
            "target_zone": self.target_zone,
            "affected_services": self.affected_services,
            "terminated_instances": self.terminated_instances,
            "recovery_times": recovery_times,
            "total_terminated": sum(len(instances) for instances in self.terminated_instances.values())
        }
    
    def cleanup(self):
        """Fuerza la recuperación de servicios"""
        logger.info(f"🔧 Forzando recuperación después de Chaos Gorilla")
        
        for service_name in self.affected_services:
            service = self.target_services_dict[service_name]
            
            # Añadir instancias para reemplazar las terminadas
            terminated_count = len(self.terminated_instances.get(service_name, []))
            for _ in range(terminated_count):
                service.add_instance()

class ChaosKong(ChaosExperiment):
    """
    Simula la falla de toda una región.
    El experimento más destructivo.
    """
    
    def __init__(self, name: str, target_region: str, target_services_dict: Dict,
                 duration_seconds: int = 900):
        super().__init__(name, ExperimentType.CHAOS_KONG, None, duration_seconds)
        self.target_region = target_region
        self.target_services_dict = target_services_dict
        self.affected_services = []
        self.terminated_instances = {}
    
    def execute(self):
        """Simula falla regional"""
        logger.critical(f"🦍 CHAOS KONG: Simulando falla REGIONAL {self.target_region}")
        
        # Terminar TODAS las instancias en la región
        for service_name, service in self.target_services_dict.items():
            terminated_in_service = []
            
            for instance_id, instance in service.instances.items():
                if instance.region == self.target_region:
                    instance.terminate()
                    terminated_in_service.append(instance_id)
            
            if terminated_in_service:
                self.affected_services.append(service_name)
                self.terminated_instances[service_name] = terminated_in_service
        
        # Este experimento no se auto-recupera
        # Simula un desastre real donde se requiere intervención manual
        
        start_time = time.time()
        while not self.should_stop.is_set() and time.time() - start_time < self.duration_seconds:
            time.sleep(30)  # Solo monitorear
        
        self.results = {
            "target_region": self.target_region,
            "affected_services": self.affected_services,
            "terminated_instances": self.terminated_instances,
            "total_terminated": sum(len(instances) for instances in self.terminated_instances.values()),
            "disaster_duration": time.time() - start_time
        }
    
    def cleanup(self):
        """Recuperación manual requerida"""
        logger.critical("🚨 CHAOS KONG completado - Se requiere recuperación manual")
        # No recuperación automática para simular desastre real

class DoctorMonkey(ChaosExperiment):
    """
    Detecta y reporta instancias no saludables.
    No es destructivo, solo diagnostica problemas.
    """
    
    def __init__(self, name: str, target_services_dict: Dict, duration_seconds: int = 300):
        super().__init__(name, ExperimentType.INSTANCE_TERMINATION, None, duration_seconds)
        self.target_services_dict = target_services_dict
        self.health_reports = []
        self.unhealthy_instances = []
    
    def execute(self):
        """Escanea la salud de todas las instancias"""
        logger.info(f"🩺 DOCTOR MONKEY: Iniciando diagnóstico de salud del sistema")
        start_time = time.time()
        scan_count = 0

        while not self.should_stop.is_set() and time.time() - start_time < self.duration_seconds:
            scan_count += 1
            self._run_single_health_scan(scan_count)
            time.sleep(30)  # Escanear cada 30 segundos

        self.results = {
            "total_scans": scan_count,
            "unique_unhealthy_instances": len(self.unhealthy_instances),
            "health_reports": self.health_reports[-5:],  # Últimos 5 reportes
            "summary": self._generate_health_summary()
        }

    def _run_single_health_scan(self, scan_count):
        current_scan = self._perform_health_scan(scan_count)
        self.health_reports.append(current_scan)
        self._report_critical_issues(current_scan)

    def _perform_health_scan(self, scan_count):
        current_scan = {
            "scan_number": scan_count,
            "timestamp": time.time(),
            "services": {}
        }
        for service_name, service in self.target_services_dict.items():
            service_health = self._check_service_health(service)
            current_scan["services"][service_name] = service_health
        return current_scan

    def _report_critical_issues(self, current_scan):
        total_unhealthy = sum(len(s["unhealthy_instances"]) for s in current_scan["services"].values())
        if total_unhealthy > 0:
            logger.warning(f"🩺 DOCTOR MONKEY: {total_unhealthy} instancias no saludables detectadas")

    def _check_service_health(self, service):
        service_health = {
            "total_instances": len(service.instances),
            "healthy_instances": 0,
            "unhealthy_instances": [],
            "degraded_instances": [],
            "performance_issues": []
        }
        for instance_id, instance in service.instances.items():
            self._evaluate_instance_health(instance_id, instance, service_health)
        return service_health

    def _evaluate_instance_health(self, instance_id, instance, service_health):
        health_check = instance.health_check()
        if not health_check or instance.status.value in ["unhealthy", "terminated"]:
            service_health["unhealthy_instances"].append(instance_id)
            if instance_id not in self.unhealthy_instances:
                self.unhealthy_instances.append(instance_id)
        elif instance.status.value == "degraded":
            service_health["degraded_instances"].append(instance_id)
        else:
            service_health["healthy_instances"] += 1

        # Detectar problemas de performance
        if instance.metrics.response_time_ms > 1000:
            service_health["performance_issues"].append({
                "instance_id": instance_id,
                "issue": "high_response_time",
                "value": instance.metrics.response_time_ms
            })
        if instance.metrics.cpu_usage > 90:
            service_health["performance_issues"].append({
                "instance_id": instance_id,
                "issue": "high_cpu",
                "value": instance.metrics.cpu_usage
            })
    
    def _generate_health_summary(self) -> Dict:
        """Genera un resumen de salud del sistema"""
        if not self.health_reports:
            return {}
        
        latest_report = self.health_reports[-1]
        total_instances = sum(s["total_instances"] for s in latest_report["services"].values())
        total_healthy = sum(s["healthy_instances"] for s in latest_report["services"].values())
        total_unhealthy = sum(len(s["unhealthy_instances"]) for s in latest_report["services"].values())
        total_degraded = sum(len(s["degraded_instances"]) for s in latest_report["services"].values())
        
        availability = (total_healthy / total_instances * 100) if total_instances > 0 else 0

        if availability > 90:
            health_status = "HEALTHY"
        elif availability > 50:
            health_status = "DEGRADED"
        else:
            health_status = "CRITICAL"
        
        return {
            "overall_availability": availability,
            "total_instances": total_instances,
            "healthy_instances": total_healthy,
            "unhealthy_instances": total_unhealthy,
            "degraded_instances": total_degraded,
            "health_status": health_status
        }
