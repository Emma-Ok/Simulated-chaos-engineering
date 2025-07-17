"""
Módulo de servicios y instancias para el simulador de Chaos Engineering.
Implementa la arquitectura base de servicios distribuidos.
"""

import time
import threading
import random
import uuid
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    """Estados posibles de un servicio"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    TERMINATED = "terminated"
    RECOVERING = "recovering"

class ServiceType(Enum):
    """Tipos de servicios en la arquitectura"""
    API_GATEWAY = "api-gateway"
    AUTH_SERVICE = "auth-service"
    DATABASE = "database"
    CACHE = "cache"
    NOTIFICATION = "notification"
    PAYMENT = "payment"
    USER_PROFILE = "user-profile"

@dataclass
class ServiceMetrics:
    """Métricas de un servicio"""
    response_time_ms: float = 0.0
    requests_per_second: float = 0.0
    error_rate: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    uptime_seconds: float = 0.0
    last_health_check: float = field(default_factory=time.time)

class ServiceInstance:
    """
    Representa una instancia individual de un servicio.
    Cada instancia puede tener su propio estado y métricas.
    """
    
    def __init__(self, service_name: str, instance_id: str = None, 
                 port: int = None, region: str = "us-east-1"):
        self.service_name = service_name
        self.instance_id = instance_id or str(uuid.uuid4())[:8]
        self.port = port or random.randint(8000, 9000)
        self.region = region
        self.status = ServiceStatus.HEALTHY
        self.metrics = ServiceMetrics()
        self.start_time = time.time()
        self.last_request_time = time.time()
        self.failure_count = 0
        self.recovery_time = None
        
        # Configuración de simulación con valores más conservadores
        self.base_response_time = random.uniform(50, 200)  # ms
        self.error_probability = 0.005  # Reducido de 0.01 a 0.005 (0.5% en lugar de 1%)
        
        # Threading para simular carga
        self.lock = threading.RLock()
        self.is_processing = False
        
        logger.info(f"Instancia {self.instance_id} del servicio {self.service_name} iniciada en puerto {self.port}")
    
    def handle_request(self, request_data: Dict = None) -> Dict:
        """
        Simula el procesamiento de una request.
        Retorna la respuesta con métricas actualizadas.
        """
        with self.lock:
            start_time = time.time()
            self.last_request_time = start_time
            
            # Simular falla si el servicio está unhealthy
            if self.status == ServiceStatus.UNHEALTHY:
                raise ServiceException(f"Servicio {self.service_name} no disponible")
            
            if self.status == ServiceStatus.TERMINATED:
                raise ServiceException(f"Instancia {self.instance_id} terminada")
            
            # Simular processing time con variabilidad
            processing_time = self._calculate_response_time()
            time.sleep(processing_time / 1000)  # Convertir a segundos
            
            # Simular errores aleatorios con probabilidad reducida
            if random.random() < self.error_probability:
                self.failure_count += 1
                raise ServiceException(f"Error simulado en {self.service_name}")
            
            # Actualizar métricas
            response_time = (time.time() - start_time) * 1000  # ms
            self._update_metrics(response_time)
            
            return {
                "status": "success",
                "instance_id": self.instance_id,
                "service_name": self.service_name,
                "response_time_ms": response_time,
                "timestamp": time.time(),
                "data": request_data or {}
            }
    
    def _calculate_response_time(self) -> float:
        """Calcula el tiempo de respuesta basado en el estado del servicio"""
        base_time = self.base_response_time
        
        if self.status == ServiceStatus.DEGRADED:
            base_time *= random.uniform(2, 5)  # 2-5x más lento
        elif self.status == ServiceStatus.RECOVERING:
            base_time *= random.uniform(1.5, 3)  # 1.5-3x más lento
        
        # Añadir variabilidad natural
        return base_time * random.uniform(0.8, 1.2)
    
    def _update_metrics(self, response_time: float):
        """
        Actualiza las métricas de la instancia con cálculos mejorados.
        
        OPTIMIZACIONES:
        - Tiempo de respuesta con promedio móvil más sensible
        - Métricas de CPU/memoria más realistas y variables
        - Tracking de requests exitosos para calcular error rate
        """
        # Promedio móvil más sensible para response time (20% peso nuevo valor)
        if self.metrics.response_time_ms == 0:
            self.metrics.response_time_ms = response_time
        else:
            self.metrics.response_time_ms = (
                self.metrics.response_time_ms * 0.8 + response_time * 0.2
            )
        
        # Simular CPU y memoria con más variabilidad y realismo
        base_cpu = random.uniform(15, 40)  # Base más variable
        base_memory = random.uniform(25, 50)  # Base más variable
        
        # Variabilidad basada en estado del servicio
        if self.status == ServiceStatus.DEGRADED:
            base_cpu *= random.uniform(2.0, 4.0)
            base_memory *= random.uniform(1.5, 2.5)
        elif self.status == ServiceStatus.RECOVERING:
            base_cpu *= random.uniform(1.3, 2.0)
            base_memory *= random.uniform(1.2, 1.8)
        
        # Variabilidad adicional basada en latencia
        if response_time > 300:  # Si la respuesta es lenta
            base_cpu *= random.uniform(1.2, 1.8)
            base_memory *= random.uniform(1.1, 1.5)
        
        self.metrics.cpu_usage = min(95, max(5, base_cpu))
        self.metrics.memory_usage = min(90, max(10, base_memory))
        
        # Actualizar uptime
        self.metrics.uptime_seconds = time.time() - self.start_time
        self.metrics.last_health_check = time.time()
    
    def health_check(self) -> bool:
        """
        Realiza un health check de la instancia.
        Retorna True si está saludable.
        """
        try:
            if self.status in [ServiceStatus.TERMINATED, ServiceStatus.UNHEALTHY]:
                return False
            
            # Simular health check que puede fallar ocasionalmente
            if random.random() < 0.02:  # Reducido de 0.05 a 0.02 (2% vs 5%)
                self.set_status(ServiceStatus.DEGRADED)
                return False
            
            # Auto-recuperación más conservadora
            if self.status == ServiceStatus.DEGRADED and random.random() < 0.2:  # Reducido de 0.3 a 0.2
                self.set_status(ServiceStatus.HEALTHY)
                logger.info(f"Instancia {self.instance_id} se ha recuperado automáticamente")
            
            self.metrics.last_health_check = time.time()
            return self.status == ServiceStatus.HEALTHY
            
        except Exception as e:
            logger.error(f"Error en health check de {self.instance_id}: {e}")
            return False
    
    def set_status(self, status: ServiceStatus):
        """Cambia el estado de la instancia"""
        old_status = self.status
        self.status = status
        
        if status == ServiceStatus.TERMINATED:
            logger.warning(f"Instancia {self.instance_id} TERMINADA")
        elif status == ServiceStatus.RECOVERING and old_status == ServiceStatus.TERMINATED:
            self.start_time = time.time()  # Reiniciar tiempo de inicio
            self.recovery_time = time.time()
            logger.info(f"Instancia {self.instance_id} RECUPERÁNDOSE")
        elif status == ServiceStatus.HEALTHY and old_status in [ServiceStatus.DEGRADED, ServiceStatus.RECOVERING]:
            logger.info(f"Instancia {self.instance_id} RECUPERADA")
    
    def terminate(self):
        """Termina la instancia (simula crash o shutdown)"""
        self.set_status(ServiceStatus.TERMINATED)
        logger.warning(f"Instancia {self.instance_id} del servicio {self.service_name} terminada")
    
    def restart(self):
        """Reinicia la instancia después de una terminación"""
        if self.status == ServiceStatus.TERMINATED:
            self.set_status(ServiceStatus.RECOVERING)
            # Simular tiempo de arranque
            time.sleep(random.uniform(1, 3))
            self.set_status(ServiceStatus.HEALTHY)
            self.failure_count = 0
    
    def introduce_latency(self, additional_ms: float):
        """Introduce latencia adicional al servicio"""
        self.base_response_time += additional_ms
        logger.info(f"Latencia adicional de {additional_ms}ms introducida en {self.instance_id}")
    
    def introduce_errors(self, error_rate: float):
        """Aumenta la tasa de errores del servicio de forma controlada"""
        # Limitar la tasa máxima de errores para evitar chaos excesivo
        self.error_probability = min(0.1, error_rate)  # Máximo 10% en lugar de 100%
        logger.info("Tasa de errores aumentada a %.1f%% en %s", self.error_probability * 100, self.instance_id)
    
    def get_metrics(self) -> ServiceMetrics:
        """Retorna las métricas actuales de la instancia"""
        return self.metrics
    
    def __str__(self):
        return f"ServiceInstance({self.service_name}:{self.instance_id}:{self.port}, status={self.status.value})"

class Service:
    """
    Representa un servicio completo con múltiples instancias.
    Maneja la creación, destrucción y distribución de carga entre instancias.
    """
    
    def __init__(self, name: str, service_type: ServiceType, 
                 initial_instances: int = 4, min_instances: int = 2,  # Aumentado de 3,1 a 4,2
                 max_instances: int = 8, region: str = "us-east-1"):  # Agregado parámetro region
        """
        Inicializa un servicio distribuido con más instancias por defecto.
        
        OPTIMIZACIONES:
        - Más instancias por defecto para mejores estadísticas
        - Mejores contadores para métricas precisas
        - Threading mejorado para health checks
        """
        self.name = name
        self.service_type = service_type
        self.region = region  # Agregado atributo region
        self.instances: Dict[str, ServiceInstance] = {}
        self.initial_instances = initial_instances
        self.min_instances = min_instances
        self.max_instances = max_instances
        
        # Contadores mejorados para métricas más precisas
        self.request_count = 0
        self.successful_requests = 0  # NUEVO: contador de requests exitosos
        self.error_count = 0
        self.total_response_time = 0.0
        
        # Threading
        self.lock = threading.RLock()
        self.health_check_thread = None
        self.auto_scaling_enabled = True  # Agregado atributo faltante
        
        # Crear instancias iniciales
        for i in range(initial_instances):
            self.add_instance()
        
        # Iniciar health checks
        self._start_health_checks()
        
        logger.info(f"Servicio {name} ({service_type.value}) iniciado con {initial_instances} instancias")
    
    def add_instance(self, instance_id: str = None) -> ServiceInstance:
        """Añade una nueva instancia al servicio"""
        with self.lock:
            instance = ServiceInstance(
                service_name=self.name,
                instance_id=instance_id,
                port=random.randint(8000, 9000), # Generar puerto aleatorio
                region=self.region
            )
            self.instances[instance.instance_id] = instance
            logger.info(f"Instancia {instance.instance_id} añadida al servicio {self.name}")
            return instance
    
    def remove_instance(self, instance_id: str) -> bool:
        """Remueve una instancia específica"""
        with self.lock:
            if instance_id in self.instances:
                instance = self.instances[instance_id]
                instance.terminate()
                del self.instances[instance_id]
                logger.info(f"Instancia {instance_id} removida del servicio {self.name}")
                return True
            return False
    
    def get_healthy_instances(self) -> List[ServiceInstance]:
        """Retorna una lista de instancias saludables"""
        return [
            instance for instance in self.instances.values()
            if instance.status in [ServiceStatus.HEALTHY, ServiceStatus.DEGRADED]
        ]
    
    def get_instance_by_id(self, instance_id: str) -> Optional[ServiceInstance]:
        """Retorna una instancia específica por ID"""
        return self.instances.get(instance_id)
    
    def handle_request(self, request_data: Dict = None) -> Dict:
        """
        Maneja una request con métricas mejoradas y tracking preciso.
        Implementa balanceo de carga simple.
        """
        healthy_instances = self.get_healthy_instances()
        
        if not healthy_instances:
            self.error_count += 1
            self.request_count += 1  # Contar también requests fallidos
            raise ServiceException(f"No hay instancias saludables en el servicio {self.name}")
        
        # Balanceo de carga round-robin simple
        instance = random.choice(healthy_instances)
        
        try:
            start_time = time.time()
            response = instance.handle_request(request_data)
            
            # Actualizar métricas del servicio con tracking mejorado
            response_time = (time.time() - start_time) * 1000
            self.request_count += 1
            self.successful_requests += 1  # NUEVO: Contador de éxitos
            self.total_response_time += response_time
            
            return response
            
        except ServiceException as e:
            # Mejorar tracking de errores
            self.error_count += 1
            self.request_count += 1  # Contar también requests fallidos
            logger.error(f"Error en servicio {self.name}: {e}")
            raise
    
    def _start_health_checks(self):
        """Inicia el hilo de health checks automáticos"""
        def health_check_loop():
            while True:
                try:
                    self._perform_health_checks()
                    self._auto_scale_if_needed()
                    time.sleep(10)  # Health check cada 10 segundos
                except Exception as e:
                    logger.error(f"Error en health check de {self.name}: {e}")
                    time.sleep(5)
        
        self.health_check_thread = threading.Thread(target=health_check_loop, daemon=True)
        self.health_check_thread.start()
    
    def _perform_health_checks(self):
        """Realiza health checks en todas las instancias"""
        with self.lock:
            for instance_id, instance in self.instances.items():
                if not instance.health_check():
                    if instance.status == ServiceStatus.TERMINATED:
                        # Intentar restart automático
                        threading.Thread(target=self._auto_restart_instance, 
                                       args=(instance_id,), daemon=True).start()
    
    def _auto_restart_instance(self, instance_id: str):
        """
        Reinicia automáticamente una instancia terminada con tiempos más realistas.
        
        OPTIMIZACIONES:
        - Tiempo de espera más largo y variable
        - Verificación de estado antes de reiniciar
        - Límite de intentos de reinicio
        """
        # Tiempo de espera más realista para restart (30-90 segundos)
        wait_time = random.uniform(30, 90)  # Aumentado de 5-15 a 30-90 segundos
        time.sleep(wait_time)
        
        with self.lock:
            if instance_id in self.instances:
                instance = self.instances[instance_id]
                if instance.status == ServiceStatus.TERMINATED:
                    try:
                        instance.restart()
                        logger.info(f"Instancia {instance_id} reiniciada automáticamente después de {wait_time:.1f}s")
                    except Exception as e:
                        logger.error(f"Error al reiniciar instancia {instance_id}: {e}")
    
    def _auto_scale_if_needed(self):
        """
        Realiza auto-scaling del servicio si está habilitado.
        
        REGLAS DE SCALING:
        - Scale UP: Si uso de CPU promedio > 80% y instancias < max
        - Scale DOWN: Si uso de CPU promedio < 30% y instancias > min
        """
        if not self.auto_scaling_enabled:
            return
            
        with self.lock:
            healthy_instances = self.get_healthy_instances()
            
            if not healthy_instances:
                return
            
            # Calcular CPU promedio
            avg_cpu = sum(inst.metrics.cpu_usage for inst in healthy_instances) / len(healthy_instances)
            current_count = len(healthy_instances)
            
            # Scale UP si CPU alta y hay espacio
            if avg_cpu > 80 and current_count < self.max_instances:
                self.add_instance()
                logger.info(f"Auto-scaling UP: {self.name} ahora tiene {current_count + 1} instancias (CPU: {avg_cpu:.1f}%)")
            
            # Scale DOWN si CPU baja y hay margen
            elif avg_cpu < 30 and current_count > self.min_instances:
                # Remover instancia menos saludable
                worst_instance = min(healthy_instances, key=lambda x: x.metrics.cpu_usage)
                self.remove_instance(worst_instance.instance_id)
                logger.info(f"Auto-scaling DOWN: {self.name} ahora tiene {current_count - 1} instancias (CPU: {avg_cpu:.1f}%)")
    
    def get_service_metrics(self) -> Dict:
        """
        Retorna métricas agregadas del servicio con cálculos mejorados.
        
        OPTIMIZACIONES:
        - Cálculos más precisos de promedios
        - Mejor manejo de casos edge
        - Métricas más detalladas por instancia
        """
        with self.lock:
            healthy_instances = self.get_healthy_instances()
            
            if not self.instances:
                return {
                    "service_name": self.name,
                    "total_instances": 0,
                    "healthy_instances": 0,
                    "availability": 0.0,
                    "avg_response_time_ms": 0.0,
                    "requests_per_second": 0.0,
                    "error_rate": 0.0,
                    "total_requests": 0,
                    "successful_requests": 0
                }
            
            # Cálculos mejorados de métricas agregadas
            total_instances = len(self.instances)
            healthy_count = len(healthy_instances)
            availability = (healthy_count / total_instances) * 100 if total_instances > 0 else 0
            
            # Promedio de tiempo de respuesta más preciso
            if self.successful_requests > 0:
                avg_response_time = self.total_response_time / self.successful_requests
            else:
                # Si no hay requests exitosos, usar promedio de instancias
                instance_times = [inst.metrics.response_time_ms for inst in self.instances.values() 
                                if inst.metrics.response_time_ms > 0]
                avg_response_time = sum(instance_times) / len(instance_times) if instance_times else 0
            
            # Tasa de error más precisa
            error_rate = (self.error_count / max(1, self.request_count)) * 100
            
            return {
                "service_name": self.name,
                "service_type": self.service_type.value,
                "total_instances": total_instances,
                "healthy_instances": healthy_count,
                "availability": availability,
                "avg_response_time_ms": round(avg_response_time, 2),  # Redondear para mejor legibilidad
                "total_requests": self.request_count,
                "successful_requests": self.successful_requests,
                "error_count": self.error_count,
                "error_rate": round(error_rate, 3),  # Redondear con más precisión
                "instances": {
                    instance_id: {
                        "status": instance.status.value,
                        "failure_count": instance.failure_count,
                        "region": instance.region,
                        "port": instance.port,
                        "metrics": {
                            "response_time_ms": round(instance.metrics.response_time_ms, 2),
                            "cpu_usage": round(instance.metrics.cpu_usage, 1),
                            "memory_usage": round(instance.metrics.memory_usage, 1),
                            "uptime_seconds": round(instance.metrics.uptime_seconds, 1),
                            "error_probability": round(instance.error_probability * 100, 2)  # Como porcentaje
                        }
                    }
                    for instance_id, instance in self.instances.items()
                }
            }
    
    def chaos_terminate_random_instance(self) -> Optional[str]:
        """
        Termina una instancia aleatoria (usado por Chaos Monkey).
        Respeta el número mínimo de instancias saludables.
        """
        healthy_instances = self.get_healthy_instances()
        
        if len(healthy_instances) <= self.min_instances:
            logger.warning(f"No se puede terminar instancia en {self.name}: "
                         f"mínimo de instancias saludables alcanzado")
            return None
        
        target_instance = random.choice(healthy_instances)
        target_instance.terminate()
        
        logger.warning(f"CHAOS: Instancia {target_instance.instance_id} del servicio {self.name} terminada")
        return target_instance.instance_id
    
    def chaos_introduce_latency(self, latency_ms: float, instance_id: str = None):
        """Introduce latencia en una o todas las instancias"""
        targets = [self.instances[instance_id]] if instance_id else list(self.instances.values())
        
        for instance in targets:
            instance.introduce_latency(latency_ms)
    
    def chaos_introduce_errors(self, error_rate: float, instance_id: str = None):
        """Introduce errores en una o todas las instancias"""
        targets = [self.instances[instance_id]] if instance_id else list(self.instances.values())
        
        for instance in targets:
            instance.introduce_errors(error_rate)
    
    def shutdown(self):
        """Cierra el servicio y todas sus instancias"""
        with self.lock:
            for instance in self.instances.values():
                instance.terminate()
            logger.info(f"Servicio {self.name} cerrado")

class ServiceException(Exception):
    """Excepción personalizada para errores de servicio"""
    pass
