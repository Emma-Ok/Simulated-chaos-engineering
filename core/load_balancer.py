"""
Load Balancer para el simulador de Chaos Engineering.
Implementa distribución de tráfico entre servicios e instancias.
"""

import random
import time
import threading
from typing import Dict, List, Optional
from enum import Enum
import logging

from .service import Service, ServiceInstance, ServiceException

logger = logging.getLogger(__name__)

class LoadBalancingStrategy(Enum):
    """Estrategias de balanceo de carga disponibles"""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    RANDOM = "random"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    HEALTH_BASED = "health_based"

class LoadBalancer:
    """
    Load Balancer que distribuye el tráfico entre múltiples servicios e instancias.
    Implementa diferentes estrategias de balanceo y health checking.
    """
    
    def __init__(self, name: str = "main-lb", strategy: LoadBalancingStrategy = LoadBalancingStrategy.HEALTH_BASED):
        self.name = name
        self.strategy = strategy
        self.services: Dict[str, Service] = {}
        self.request_count = 0
        self.total_response_time = 0.0
        self.error_count = 0
        
        # Estado para round robin
        self._round_robin_counters: Dict[str, int] = {}
        
        # Threading
        self.lock = threading.RLock()
        
        # Métricas de tráfico
        self.traffic_metrics = {
            "requests_per_second": 0.0,
            "avg_response_time_ms": 0.0,
            "error_rate": 0.0,
            "total_requests": 0
        }
        
        # Iniciar recolección de métricas
        self._start_metrics_collection()
        
        logger.info(f"Load Balancer {self.name} iniciado con estrategia {strategy.value}")
    
    def register_service(self, service: Service):
        """Registra un servicio en el load balancer"""
        with self.lock:
            self.services[service.name] = service
            self._round_robin_counters[service.name] = 0
            logger.info(f"Servicio {service.name} registrado en Load Balancer {self.name}")
    
    def unregister_service(self, service_name: str):
        """Desregistra un servicio del load balancer"""
        with self.lock:
            if service_name in self.services:
                del self.services[service_name]
                del self._round_robin_counters[service_name]
                logger.info(f"Servicio {service_name} desregistrado del Load Balancer {self.name}")
    
    def route_request(self, service_name: str, request_data: Dict = None) -> Dict:
        """
        Enruta una request al servicio especificado usando la estrategia configurada.
        """
        start_time = time.time()
        
        try:
            if service_name not in self.services:
                raise ServiceException(f"Servicio {service_name} no encontrado en Load Balancer")
            
            service = self.services[service_name]
            instance = self._select_instance(service)
            
            if not instance:
                raise ServiceException(f"No hay instancias disponibles para {service_name}")
            
            # Procesar la request
            response = instance.handle_request(request_data)
            
            # Actualizar métricas
            response_time = (time.time() - start_time) * 1000
            self._update_metrics(response_time, success=True)
            
            # Añadir información de routing
            response["routed_by"] = self.name
            response["routing_strategy"] = self.strategy.value
            response["load_balancer_response_time_ms"] = response_time
            
            return response
            
        except ServiceException as e:
            self._update_metrics(0, success=False)
            logger.error(f"Error en routing hacia {service_name}: {e}")
            raise
    
    def _select_instance(self, service: Service) -> Optional[ServiceInstance]:
        """Selecciona una instancia usando la estrategia configurada"""
        healthy_instances = service.get_healthy_instances()
        
        if not healthy_instances:
            return None
        
        if self.strategy == LoadBalancingStrategy.RANDOM:
            return random.choice(healthy_instances)
        
        elif self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin_selection(service, healthy_instances)
        
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._least_connections_selection(healthy_instances)
        
        elif self.strategy == LoadBalancingStrategy.HEALTH_BASED:
            return self._health_based_selection(healthy_instances)
        
        elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return self._weighted_round_robin_selection(healthy_instances)
        
        else:
            return random.choice(healthy_instances)
    
    def _round_robin_selection(self, service: Service, instances: List[ServiceInstance]) -> ServiceInstance:
        """Implementa selección Round Robin"""
        with self.lock:
            counter = self._round_robin_counters[service.name]
            selected = instances[counter % len(instances)]
            self._round_robin_counters[service.name] = (counter + 1) % len(instances)
            return selected
    
    def _least_connections_selection(self, instances: List[ServiceInstance]) -> ServiceInstance:
        """Selecciona la instancia con menos conexiones activas (simulado)"""
        # Simulamos "conexiones activas" basándose en el tiempo desde última request
        least_busy = min(instances, 
                        key=lambda x: time.time() - x.last_request_time)
        return least_busy
    
    def _health_based_selection(self, instances: List[ServiceInstance]) -> ServiceInstance:
        """Selecciona basándose en la salud y performance de las instancias"""
        # Calcular score de salud para cada instancia
        scores = []
        for instance in instances:
            score = self._calculate_health_score(instance)
            scores.append((instance, score))
        
        # Seleccionar la instancia con mejor score
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[0][0]
    
    def _weighted_round_robin_selection(self, instances: List[ServiceInstance]) -> ServiceInstance:
        """Implementa weighted round robin basado en la performance"""
        weights = []
        for instance in instances:
            # Peso inversamente proporcional al tiempo de respuesta
            weight = max(1, 1000 / max(instance.metrics.response_time_ms, 1))
            weights.append(weight)
        
        # Selección aleatoria ponderada
        total_weight = sum(weights)
        r = random.uniform(0, total_weight)
        
        cumulative_weight = 0
        for i, weight in enumerate(weights):
            cumulative_weight += weight
            if r <= cumulative_weight:
                return instances[i]
        
        return instances[-1]  # Fallback
    
    def _calculate_health_score(self, instance: ServiceInstance) -> float:
        """Calcula un score de salud para una instancia"""
        score = 100.0  # Score base
        
        # Penalizar por tiempo de respuesta alto
        if instance.metrics.response_time_ms > 500:
            score -= (instance.metrics.response_time_ms - 500) / 10
        
        # Penalizar por alto uso de CPU
        if instance.metrics.cpu_usage > 80:
            score -= (instance.metrics.cpu_usage - 80) * 2
        
        # Penalizar por alto uso de memoria
        if instance.metrics.memory_usage > 80:
            score -= (instance.metrics.memory_usage - 80) * 1.5
        
        # Penalizar por fallas recientes
        score -= instance.failure_count * 10
        
        # Bonus por uptime alto
        if instance.metrics.uptime_seconds > 3600:  # 1 hora
            score += 10
        
        return max(0, score)
    
    def _update_metrics(self, response_time: float, success: bool):
        """Actualiza las métricas del load balancer"""
        with self.lock:
            self.request_count += 1
            
            if success:
                self.total_response_time += response_time
            else:
                self.error_count += 1
    
    def _start_metrics_collection(self):
        """Inicia la recolección periódica de métricas"""
        def metrics_loop():
            last_request_count = 0
            while True:
                try:
                    with self.lock:
                        # Calcular requests per second
                        current_requests = self.request_count
                        rps = current_requests - last_request_count
                        last_request_count = current_requests
                        
                        # Actualizar métricas
                        self.traffic_metrics["requests_per_second"] = rps
                        self.traffic_metrics["total_requests"] = current_requests
                        
                        if current_requests > 0:
                            self.traffic_metrics["avg_response_time_ms"] = (
                                self.total_response_time / current_requests
                            )
                            self.traffic_metrics["error_rate"] = (
                                self.error_count / current_requests
                            ) * 100
                    
                    time.sleep(1)  # Actualizar cada segundo
                    
                except Exception as e:
                    logger.error(f"Error en recolección de métricas del LB: {e}")
                    time.sleep(5)
        
        metrics_thread = threading.Thread(target=metrics_loop, daemon=True)
        metrics_thread.start()
    
    def get_load_balancer_metrics(self) -> Dict:
        """Retorna las métricas del load balancer"""
        with self.lock:
            return {
                "load_balancer_name": self.name,
                "strategy": self.strategy.value,
                "traffic_metrics": self.traffic_metrics.copy(),
                "registered_services": list(self.services.keys()),
                "service_health": {
                    service_name: {
                        "total_instances": len(service.instances),
                        "healthy_instances": len(service.get_healthy_instances()),
                        "availability": (len(service.get_healthy_instances()) / 
                                       max(1, len(service.instances))) * 100
                    }
                    for service_name, service in self.services.items()
                }
            }
    
    def health_check_all_services(self) -> Dict[str, bool]:
        """Realiza health check en todos los servicios registrados"""
        results = {}
        
        for service_name, service in self.services.items():
            healthy_instances = service.get_healthy_instances()
            results[service_name] = len(healthy_instances) > 0
        
        return results
    
    def get_service_availability(self) -> Dict[str, float]:
        """Retorna la disponibilidad de cada servicio"""
        availability = {}
        
        for service_name, service in self.services.items():
            total_instances = len(service.instances)
            healthy_instances = len(service.get_healthy_instances())
            availability[service_name] = (
                (healthy_instances / total_instances * 100) if total_instances > 0 else 0
            )
        
        return availability
    
    def chaos_remove_service(self, service_name: str) -> bool:
        """
        Remueve temporalmente un servicio del load balancer (simula falla de servicio completo).
        Usado por experimentos de Chaos Engineering.
        """
        if service_name in self.services:
            service = self.services[service_name]
            # Terminar todas las instancias
            for instance in service.instances.values():
                instance.terminate()
            
            logger.warning(f"CHAOS: Servicio {service_name} removido del Load Balancer")
            return True
        return False
    
    def chaos_degrade_service(self, service_name: str, degradation_factor: float = 2.0):
        """
        Degrada el performance de un servicio.
        Usado por experimentos de Chaos Engineering.
        """
        if service_name in self.services:
            service = self.services[service_name]
            for instance in service.instances.values():
                instance.introduce_latency(instance.base_response_time * (degradation_factor - 1))
            
            logger.warning(f"CHAOS: Servicio {service_name} degradado con factor {degradation_factor}")
            return True
        return False
    
    def simulate_traffic(self, requests_per_second: int = 10, duration_seconds: int = 60):
        """
        Simula tráfico hacia los servicios registrados.
        Útil para testing y demostración.
        """
        def traffic_generator():
            end_time = time.time() + duration_seconds
            service_names = list(self.services.keys())
            
            if not service_names:
                logger.warning("No hay servicios registrados para simular tráfico")
                return
            
            while time.time() < end_time:
                try:
                    # Seleccionar servicio aleatorio
                    service_name = random.choice(service_names)
                    
                    # Simular request
                    request_data = {
                        "user_id": random.randint(1000, 9999),
                        "action": random.choice(["get", "post", "put", "delete"]),
                        "timestamp": time.time()
                    }
                    
                    self.route_request(service_name, request_data)
                    
                    # Esperar antes de la siguiente request
                    time.sleep(1.0 / requests_per_second)
                    
                except Exception as e:
                    logger.error(f"Error en simulación de tráfico: {e}")
                    time.sleep(0.1)
        
        traffic_thread = threading.Thread(target=traffic_generator, daemon=True)
        traffic_thread.start()
        logger.info(f"Simulación de tráfico iniciada: {requests_per_second} RPS por {duration_seconds} segundos")
    
    def get_detailed_status(self) -> Dict:
        """Retorna un estado detallado del load balancer y todos los servicios"""
        status = {
            "load_balancer": self.get_load_balancer_metrics(),
            "services": {}
        }
        
        for service_name, service in self.services.items():
            status["services"][service_name] = service.get_service_metrics()
        
        return status
    
    def shutdown(self):
        """Cierra el load balancer y todos los servicios"""
        logger.info(f"Cerrando Load Balancer {self.name}")
        
        for service in self.services.values():
            service.shutdown()
        
        self.services.clear()
        logger.info(f"Load Balancer {self.name} cerrado")
