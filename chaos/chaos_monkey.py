"""
Chaos Monkey - Motor principal de chaos engineering.
Termina instancias aleatoriamente respetando reglas de seguridad.
"""

import random
import time
import threading
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ChaosMonkey:
    """
    Implementa el famoso Chaos Monkey que termina instancias aleatoriamente.
    Respeta reglas de seguridad y horarios configurados.
    """
    
    def __init__(self, name: str = "chaos-monkey"):
        self.name = name
        self.is_enabled = False
        self.is_running = False
        self.target_services = {}
        
        # Configuración de seguridad
        self.min_healthy_instances = 1
        self.max_instances_to_kill = 1
        self.excluded_services = set()
        
        # Configuración de horarios
        self.allowed_days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        self.allowed_hours = {"start": 9, "end": 17}
        
        # Configuración de probabilidades
        self.termination_probability = 0.1  # 10% de probabilidad
        self.check_interval_seconds = 300    # 5 minutos
        
        # Métricas y registro
        self.total_terminations = 0
        self.successful_terminations = 0
        self.blocked_terminations = 0
        self.last_termination_time = None
        self.termination_history = []
        
        # Threading
        self.chaos_thread = None
        self.lock = threading.RLock()
        
        # Callbacks
        self.termination_callbacks = []
        
        logger.info(f"Chaos Monkey '{self.name}' inicializado")
    
    def configure(self, config: Dict):
        """
        Configura el Chaos Monkey con parámetros específicos.
        """
        with self.lock:
            self._configure_enabled(config)
            self._configure_schedule(config)
            self._configure_targets(config)
            self._configure_experiments(config)
        
        logger.info(f"Chaos Monkey configurado: enabled={self.is_enabled}, "
                   f"probability={self.termination_probability}")

    def _configure_enabled(self, config: Dict):
        if "enabled" in config:
            self.is_enabled = config["enabled"]

    def _configure_schedule(self, config: Dict):
        schedule = config.get("schedule", {})
        if "days" in schedule:
            self.allowed_days = schedule["days"]
        if "hours" in schedule:
            self.allowed_hours = schedule["hours"]

    def _configure_targets(self, config: Dict):
        targets = config.get("targets", {})
        if "min_healthy_instances" in targets:
            self.min_healthy_instances = targets["min_healthy_instances"]
        if "max_instances_to_kill" in targets:
            self.max_instances_to_kill = targets["max_instances_to_kill"]
        if "excluded_services" in targets:
            self.excluded_services = set(targets["excluded_services"])

    def _configure_experiments(self, config: Dict):
        experiments = config.get("experiments", {})
        termination_config = experiments.get("instance_termination", {})
        if "probability" in termination_config:
            self.termination_probability = termination_config["probability"]
        if "check_interval_seconds" in termination_config:
            self.check_interval_seconds = termination_config["check_interval_seconds"]
    
    def register_service(self, service_name: str, service):
        """Registra un servicio como target para chaos experiments"""
        with self.lock:
            if service_name not in self.excluded_services:
                self.target_services[service_name] = service
                logger.info(f"Servicio '{service_name}' registrado en Chaos Monkey")
            else:
                logger.info(f"Servicio '{service_name}' excluido de Chaos Monkey")
    
    def unregister_service(self, service_name: str):
        """Desregistra un servicio"""
        with self.lock:
            if service_name in self.target_services:
                del self.target_services[service_name]
                logger.info(f"Servicio '{service_name}' desregistrado de Chaos Monkey")
    
    def start(self):
        """Inicia el Chaos Monkey"""
        if self.is_running:
            logger.warning("Chaos Monkey ya está en ejecución")
            return
        
        if not self.is_enabled:
            logger.info("Chaos Monkey está deshabilitado")
            return
        
        self.is_running = True
        self.chaos_thread = threading.Thread(target=self._chaos_loop, daemon=True)
        self.chaos_thread.start()
        
        logger.info(f"🐒 Chaos Monkey '{self.name}' INICIADO")
    
    def stop(self):
        """Detiene el Chaos Monkey"""
        self.is_running = False
        if self.chaos_thread:
            self.chaos_thread.join(timeout=5)
        
        logger.info(f"🐒 Chaos Monkey '{self.name}' DETENIDO")
    
    def _chaos_loop(self):
        """Loop principal del Chaos Monkey"""
        while self.is_running:
            try:
                if self._is_chaos_time():
                    self._execute_chaos()
                
                time.sleep(self.check_interval_seconds)
                
            except Exception as e:
                logger.error(f"Error en loop de Chaos Monkey: {e}")
                time.sleep(30)  # Esperar antes de continuar
    
    def _is_chaos_time(self) -> bool:
        """
        Verifica si es un momento apropiado para ejecutar chaos.
        Respeta horarios y días configurados.
        """
        now = datetime.now()
        
        # Verificar día de la semana
        current_day = now.strftime("%A").lower()
        if current_day not in [day.lower() for day in self.allowed_days]:
            return False
        
        # Verificar hora
        current_hour = now.hour
        if not (self.allowed_hours["start"] <= current_hour < self.allowed_hours["end"]):
            return False
        
        return True
    
    def _execute_chaos(self):
        """
        Ejecuta un experimento de chaos si las condiciones se cumplen.
        """
        # Verificar probabilidad
        if random.random() > self.termination_probability:
            return
        
        # Seleccionar servicio target
        target_service_name = self._select_target_service()
        if not target_service_name:
            return
        
        target_service = self.target_services[target_service_name]
        
        # Intentar terminar una instancia
        result = self._terminate_instance(target_service_name, target_service)
        
        if result:
            self._record_termination(target_service_name, result)
            
            # Notificar callbacks
            for callback in self.termination_callbacks:
                try:
                    callback(target_service_name, result)
                except Exception as e:
                    logger.error(f"Error en callback de terminación: {e}")
    
    def _select_target_service(self) -> Optional[str]:
        """
        Selecciona un servicio target para chaos.
        Filtra servicios que no cumplen requisitos de seguridad.
        """
        eligible_services = []
        
        for service_name, service in self.target_services.items():
            try:
                healthy_instances = service.get_healthy_instances()
                
                # Verificar que hay suficientes instancias saludables
                if len(healthy_instances) > self.min_healthy_instances:
                    eligible_services.append(service_name)
                    
            except Exception as e:
                logger.error(f"Error evaluando servicio {service_name}: {e}")
        
        if not eligible_services:
            logger.debug("No hay servicios elegibles para chaos")
            return None
        
        return random.choice(eligible_services)
    
    def _terminate_instance(self, service_name: str, service) -> Optional[str]:
        """
        Termina una instancia del servicio especificado.
        Retorna el ID de la instancia terminada o None si no fue posible.
        """
        try:
            terminated_instance_id = service.chaos_terminate_random_instance()
            
            if terminated_instance_id:
                self.successful_terminations += 1
                logger.warning(f"🐒 CHAOS MONKEY: Terminada instancia {terminated_instance_id} "
                             f"del servicio {service_name}")
                return terminated_instance_id
            else:
                self.blocked_terminations += 1
                logger.info(f"Terminación bloqueada para {service_name} "
                           f"(protecciones de seguridad)")
                return None
                
        except Exception as e:
            logger.error(f"Error terminando instancia de {service_name}: {e}")
            return None
    
    def _record_termination(self, service_name: str, instance_id: str):
        """Registra una terminación en el historial"""
        with self.lock:
            self.total_terminations += 1
            self.last_termination_time = time.time()
            
            termination_record = {
                "timestamp": self.last_termination_time,
                "service_name": service_name,
                "instance_id": instance_id,
                "chaos_monkey": self.name
            }
            
            self.termination_history.append(termination_record)
            
            # Mantener solo últimas 100 terminaciones
            if len(self.termination_history) > 100:
                self.termination_history.pop(0)
    
    def force_chaos(self, service_name: str = None) -> Dict:
        """
        Fuerza la ejecución de chaos inmediatamente.
        Útil para testing y demostraciones.
        """
        if not self.is_enabled:
            return {"status": "error", "message": "Chaos Monkey está deshabilitado"}
        
        if service_name and service_name not in self.target_services:
            return {"status": "error", "message": f"Servicio {service_name} no registrado"}
        
        target_service_name = service_name or self._select_target_service()
        
        if not target_service_name:
            return {"status": "error", "message": "No hay servicios elegibles"}
        
        target_service = self.target_services[target_service_name]
        instance_id = self._terminate_instance(target_service_name, target_service)
        
        if instance_id:
            self._record_termination(target_service_name, instance_id)
            
            # Notificar callbacks
            for callback in self.termination_callbacks:
                try:
                    callback(target_service_name, instance_id)
                except Exception as e:
                    logger.error(f"Error en callback de terminación: {e}")
            
            return {
                "status": "success",
                "message": f"Instancia {instance_id} del servicio {target_service_name} terminada",
                "service_name": target_service_name,
                "instance_id": instance_id
            }
        else:
            return {
                "status": "blocked",
                "message": f"Terminación bloqueada para {target_service_name}",
                "service_name": target_service_name
            }
    
    def add_termination_callback(self, callback: Callable[[str, str], None]):
        """
        Añade un callback que se ejecuta cuando se termina una instancia.
        callback(service_name, instance_id)
        """
        self.termination_callbacks.append(callback)
    
    def get_statistics(self) -> Dict:
        """Retorna estadísticas del Chaos Monkey"""
        with self.lock:
            return {
                "name": self.name,
                "enabled": self.is_enabled,
                "running": self.is_running,
                "configuration": {
                    "termination_probability": self.termination_probability,
                    "check_interval_seconds": self.check_interval_seconds,
                    "min_healthy_instances": self.min_healthy_instances,
                    "max_instances_to_kill": self.max_instances_to_kill,
                    "allowed_days": self.allowed_days,
                    "allowed_hours": self.allowed_hours,
                    "excluded_services": list(self.excluded_services)
                },
                "statistics": {
                    "total_terminations": self.total_terminations,
                    "successful_terminations": self.successful_terminations,
                    "blocked_terminations": self.blocked_terminations,
                    "last_termination_time": self.last_termination_time,
                    "registered_services": len(self.target_services),
                    "is_chaos_time": self._is_chaos_time()
                },
                "recent_terminations": self.termination_history[-10:] if self.termination_history else []
            }
    
    def get_termination_history(self, hours: int = 24) -> List[Dict]:
        """Retorna el historial de terminaciones"""
        cutoff_time = time.time() - (hours * 3600)
        
        return [
            record for record in self.termination_history
            if record["timestamp"] >= cutoff_time
        ]
    
    def disable_temporarily(self, duration_minutes: int = 60):
        """
        Deshabilita temporalmente el Chaos Monkey.
        Útil durante mantenimientos o despliegues.
        """
        was_enabled = self.is_enabled
        self.is_enabled = False
        
        logger.info(f"Chaos Monkey deshabilitado temporalmente por {duration_minutes} minutos")
        
        def re_enable():
            time.sleep(duration_minutes * 60)
            self.is_enabled = was_enabled
            logger.info("Chaos Monkey re-habilitado automáticamente")
        
        re_enable_thread = threading.Thread(target=re_enable, daemon=True)
        re_enable_thread.start()
    
    def exclude_service(self, service_name: str, duration_minutes: int = None):
        """
        Excluye temporalmente un servicio del chaos.
        Si duration_minutes es None, la exclusión es permanente.
        """
        with self.lock:
            self.excluded_services.add(service_name)
            
            if service_name in self.target_services:
                del self.target_services[service_name]
        
        logger.info(f"Servicio {service_name} excluido del chaos" + 
                   (f" por {duration_minutes} minutos" if duration_minutes else " permanentemente"))
        
        if duration_minutes:
            def re_include():
                time.sleep(duration_minutes * 60)
                with self.lock:
                    self.excluded_services.discard(service_name)
                logger.info(f"Servicio {service_name} re-incluido en chaos automáticamente")
            
            re_include_thread = threading.Thread(target=re_include, daemon=True)
            re_include_thread.start()
    
    def simulate_outage(self, service_name: str = None, instance_count: int = 1) -> Dict:
        """
        Simula un outage más severo terminando múltiples instancias.
        Útil para simular fallas de datacenter o zona.
        """
        if not self.is_enabled:
            return {"status": "error", "message": "Chaos Monkey está deshabilitado"}
        
        results = []
        
        # Si no se especifica servicio, seleccionar uno aleatorio
        if not service_name:
            service_name = self._select_target_service()
            
        if not service_name or service_name not in self.target_services:
            return {"status": "error", "message": "Servicio no válido o no disponible"}
        
        service = self.target_services[service_name]
        
        for _ in range(min(instance_count, self.max_instances_to_kill)):
            instance_id = self._terminate_instance(service_name, service)
            
            if instance_id:
                self._record_termination(service_name, instance_id)
                results.append(instance_id)
                
                # Pequeña pausa entre terminaciones
                time.sleep(random.uniform(1, 5))
            else:
                break  # No más instancias disponibles para terminar
        
        return {
            "status": "success" if results else "blocked",
            "message": f"Outage simulado en {service_name}",
            "service_name": service_name,
            "terminated_instances": results,
            "requested_count": instance_count,
            "actual_count": len(results)
        }
