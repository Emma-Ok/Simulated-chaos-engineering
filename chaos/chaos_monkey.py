"""
Chaos Monkey - Motor principal de chaos engineering.
Termina instancias aleatoriamente respetando reglas de seguridad.

TIEMPOS OPTIMIZADOS PARA DEMO:
- Intervalo de verificación: 30 segundos (vs 5 minutos original)
- Probabilidades más altas para mayor actividad
- Respuesta más rápida para demostraciones
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
    
    CARACTERÍSTICAS:
    - Respeta reglas de seguridad estrictas
    - Configurable por horarios y días
    - Probabilidades ajustables
    - Historial completo de acciones
    - Callbacks para integración
    
    OPTIMIZADO PARA DEMOS:
    - Intervalos cortos (30s vs 5min)
    - Probabilidades altas para actividad visible
    - Respuesta inmediata en modo forzado
    """
    
    def __init__(self, name: str = "chaos-monkey"):
        # ═══════════════════════════════════════════════════════════════════
        # CONFIGURACIÓN BÁSICA
        # ═══════════════════════════════════════════════════════════════════
        self.name = name
        self.is_enabled = False      # Estado de habilitación
        self.is_running = False      # Estado de ejecución
        self.target_services = {}    # Servicios registrados para chaos
        
        # ═══════════════════════════════════════════════════════════════════
        # CONFIGURACIÓN DE SEGURIDAD
        # ═══════════════════════════════════════════════════════════════════
        self.min_healthy_instances = 1     # Mínimo de instancias que deben sobrevivir
        self.max_instances_to_kill = 1     # Máximo de instancias a terminar simultáneamente
        self.excluded_services = set()     # Servicios protegidos
        
        # ═══════════════════════════════════════════════════════════════════
        # CONFIGURACIÓN DE HORARIOS
        # ═══════════════════════════════════════════════════════════════════
        self.allowed_days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        self.allowed_hours = {"start": 9, "end": 17}  # Horario de oficina por defecto
        
        # ═══════════════════════════════════════════════════════════════════
        # CONFIGURACIÓN DE PROBABILIDADES (OPTIMIZADA PARA DEMOS)
        # ═══════════════════════════════════════════════════════════════════
        self.termination_probability = 0.3  # 30% de probabilidad (vs 10% original)
        self.check_interval_seconds = 30    # 30 segundos (vs 5 minutos original)
        
        # ═══════════════════════════════════════════════════════════════════
        # MÉTRICAS Y REGISTRO
        # ═══════════════════════════════════════════════════════════════════
        self.total_terminations = 0        # Total de intentos de terminación
        self.successful_terminations = 0   # Terminaciones exitosas
        self.blocked_terminations = 0      # Terminaciones bloqueadas por seguridad
        self.last_termination_time = None  # Timestamp de última terminación
        self.termination_history = []      # Historial detallado (últimas 100)
        
        # ═══════════════════════════════════════════════════════════════════
        # THREADING PARA OPERACIÓN ASÍNCRONA
        # ═══════════════════════════════════════════════════════════════════
        self.chaos_thread = None           # Hilo principal de chaos
        self.lock = threading.RLock()      # Lock para thread safety
        
        # ═══════════════════════════════════════════════════════════════════
        # SISTEMA DE CALLBACKS
        # ═══════════════════════════════════════════════════════════════════
        self.termination_callbacks = []    # Callbacks para integración externa
        
        logger.info(f"🐒 Chaos Monkey '{self.name}' inicializado con intervalos optimizados")
    
    def configure(self, config: Dict):
        """
        Configura el Chaos Monkey con parámetros específicos.
        
        CONFIGURACIONES SOPORTADAS:
        - enabled: Habilitar/deshabilitar
        - schedule: Días y horarios permitidos
        - targets: Servicios objetivo y exclusiones
        - experiments: Probabilidades y intervalos
        
        Args:
            config: Diccionario con configuraciones
        """
        with self.lock:
            self._configure_enabled(config)
            self._configure_schedule(config)
            self._configure_targets(config)
            self._configure_experiments(config)
        
        logger.info(f"🔧 Chaos Monkey configurado: enabled={self.is_enabled}, "
                   f"probability={self.termination_probability}, interval={self.check_interval_seconds}s")

    def _configure_enabled(self, config: Dict):
        """Configura el estado de habilitación"""
        if "enabled" in config:
            self.is_enabled = config["enabled"]

    def _configure_schedule(self, config: Dict):
        """Configura los horarios permitidos para chaos"""
        schedule = config.get("schedule", {})
        if "days" in schedule:
            self.allowed_days = schedule["days"]
        if "hours" in schedule:
            self.allowed_hours = schedule["hours"]

    def _configure_targets(self, config: Dict):
        """Configura los objetivos y reglas de seguridad"""
        targets = config.get("targets", {})
        if "min_healthy_instances" in targets:
            self.min_healthy_instances = targets["min_healthy_instances"]
        if "max_instances_to_kill" in targets:
            self.max_instances_to_kill = targets["max_instances_to_kill"]
        if "excluded_services" in targets:
            self.excluded_services = set(targets["excluded_services"])

    def _configure_experiments(self, config: Dict):
        """Configura los parámetros de experimentos"""
        experiments = config.get("experiments", {})
        termination_config = experiments.get("instance_termination", {})
        
        if "probability" in termination_config:
            self.termination_probability = termination_config["probability"]
        if "check_interval_seconds" in termination_config:
            self.check_interval_seconds = termination_config["check_interval_seconds"]
            # ⚠️ Asegurar que el intervalo no sea muy largo para demos
            if self.check_interval_seconds > 60:
                logger.warning(f"⏱️ Intervalo {self.check_interval_seconds}s muy largo para demos, "
                             f"recomendado: <= 60s")
    
    def register_service(self, service_name: str, service):
        """
        Registra un servicio como target para chaos experiments.
        
        VERIFICACIONES:
        - Servicio no esté en lista de exclusiones
        - Servicio tenga suficientes instancias
        
        Args:
            service_name: Nombre del servicio
            service: Objeto del servicio
        """
        with self.lock:
            if service_name not in self.excluded_services:
                self.target_services[service_name] = service
                logger.info(f"🎯 Servicio '{service_name}' registrado en Chaos Monkey")
            else:
                logger.info(f"🛡️ Servicio '{service_name}' excluido de Chaos Monkey")
    
    def unregister_service(self, service_name: str):
        """Desregistra un servicio del Chaos Monkey"""
        with self.lock:
            if service_name in self.target_services:
                del self.target_services[service_name]
                logger.info(f"🚫 Servicio '{service_name}' desregistrado de Chaos Monkey")
    
    def start(self):
        """
        Inicia el Chaos Monkey en modo automático.
        
        COMPORTAMIENTO:
        - Verificación cada 30 segundos (configurable)
        - Respeta horarios y días configurados
        - Aplica probabilidades de ejecución
        - Registra todas las acciones
        """
        if self.is_running:
            logger.warning("🐒 Chaos Monkey ya está en ejecución")
            return
        
        if not self.is_enabled:
            logger.info("🐒 Chaos Monkey está deshabilitado")
            return
        
        self.is_running = True
        self.chaos_thread = threading.Thread(target=self._chaos_loop, daemon=True)
        self.chaos_thread.start()
        
        logger.info(f"🐒 Chaos Monkey '{self.name}' INICIADO (intervalo: {self.check_interval_seconds}s)")
    
    def stop(self):
        """
        Detiene el Chaos Monkey de forma segura.
        
        COMPORTAMIENTO:
        - Para el hilo principal
        - Mantiene el historial y estadísticas
        - No afecta experimentos en curso
        """
        self.is_running = False
        if self.chaos_thread:
            self.chaos_thread.join(timeout=5)
        
        logger.info(f"🐒 Chaos Monkey '{self.name}' DETENIDO")
    
    def _chaos_loop(self):
        """
        Loop principal del Chaos Monkey con manejo robusto de errores.
        
        COMPORTAMIENTO:
        - Verificar si es momento apropiado para chaos
        - Aplicar probabilidades de ejecución
        - Ejecutar terminaciones de forma segura
        - Registrar resultados y errores
        """
        logger.info(f"🔄 Iniciando loop de Chaos Monkey (cada {self.check_interval_seconds}s)")
        
        while self.is_running:
            try:
                if self._is_chaos_time():
                    self._execute_chaos()
                else:
                    logger.debug("⏰ Fuera del horario permitido para chaos")
                
                time.sleep(self.check_interval_seconds)
                
            except Exception as e:
                logger.error(f"💥 Error en loop de Chaos Monkey: {e}")
                time.sleep(30)  # Esperar antes de continuar tras error
    
    def _is_chaos_time(self) -> bool:
        """
        Verifica si es un momento apropiado para ejecutar chaos.
        
        VERIFICACIONES:
        - Día de la semana permitido
        - Hora del día dentro de rango
        - Sistema habilitado
        
        Returns:
            bool: True si es momento apropiado para chaos
        """
        if not self.is_enabled:
            return False
            
        now = datetime.now()
        
        # ▓▓▓ VERIFICAR DÍA DE LA SEMANA ▓▓▓
        current_day = now.strftime("%A").lower()
        if current_day not in [day.lower() for day in self.allowed_days]:
            logger.debug(f"📅 {current_day} no está en días permitidos: {self.allowed_days}")
            return False
        
        # ▓▓▓ VERIFICAR HORA DEL DÍA ▓▓▓
        current_hour = now.hour
        if not (self.allowed_hours["start"] <= current_hour < self.allowed_hours["end"]):
            logger.debug(f"🕐 Hora {current_hour} fuera de rango permitido: "
                        f"{self.allowed_hours['start']}-{self.allowed_hours['end']}")
            return False
        
        return True
    
    def _execute_chaos(self):
        """
        Ejecuta un experimento de chaos si las condiciones se cumplen.
        
        PROCESO:
        1. Verificar probabilidad de ejecución
        2. Seleccionar servicio objetivo elegible
        3. Intentar terminar una instancia
        4. Registrar resultado y notificar callbacks
        """
        # ▓▓▓ VERIFICAR PROBABILIDAD ▓▓▓
        if random.random() > self.termination_probability:
            logger.debug(f"🎲 Probabilidad no alcanzada ({self.termination_probability*100:.1f}%)")
            return
        
        # ▓▓▓ SELECCIONAR SERVICIO TARGET ▓▓▓
        target_service_name = self._select_target_service()
        if not target_service_name:
            logger.debug("🎯 No hay servicios elegibles para chaos")
            return
        
        target_service = self.target_services[target_service_name]
        
        # ▓▓▓ INTENTAR TERMINAR INSTANCIA ▓▓▓
        result = self._terminate_instance(target_service_name, target_service)
        
        if result:
            self._record_termination(target_service_name, result)
            
            # ▓▓▓ NOTIFICAR CALLBACKS ▓▓▓
            for callback in self.termination_callbacks:
                try:
                    callback(target_service_name, result)
                except Exception as e:
                    logger.error(f"💥 Error en callback de terminación: {e}")
    
    def _select_target_service(self) -> Optional[str]:
        """
        Selecciona un servicio target para chaos aplicando reglas de seguridad.
        
        CRITERIOS DE SELECCIÓN:
        - Servicio no excluido
        - Suficientes instancias saludables
        - Respeta mínimo de instancias
        
        Returns:
            str: Nombre del servicio seleccionado, None si ninguno es elegible
        """
        eligible_services = []
        
        for service_name, service in self.target_services.items():
            try:
                healthy_instances = service.get_healthy_instances()
                
                # ▓▓▓ VERIFICAR REGLAS DE SEGURIDAD ▓▓▓
                if len(healthy_instances) > self.min_healthy_instances:
                    eligible_services.append(service_name)
                    logger.debug(f"✅ {service_name}: {len(healthy_instances)} instancias saludables")
                else:
                    logger.debug(f"🛡️ {service_name}: solo {len(healthy_instances)} instancias, "
                               f"mínimo requerido: {self.min_healthy_instances}")
                    
            except Exception as e:
                logger.error(f"💥 Error evaluando servicio {service_name}: {e}")
        
        if not eligible_services:
            logger.debug("🚫 No hay servicios elegibles para chaos")
            return None
        
        selected = random.choice(eligible_services)
        logger.debug(f"🎯 Servicio seleccionado: {selected}")
        return selected
    
    def _terminate_instance(self, service_name: str, service) -> Optional[str]:
        """
        Termina una instancia del servicio especificado aplicando reglas de seguridad.
        
        PROCESO:
        1. Verificar elegibilidad del servicio
        2. Llamar al método de terminación del servicio
        3. Actualizar estadísticas
        4. Registrar resultado
        
        Args:
            service_name: Nombre del servicio
            service: Objeto del servicio
            
        Returns:
            str: ID de la instancia terminada, None si no fue posible
        """
        try:
            terminated_instance_id = service.chaos_terminate_random_instance()
            
            if terminated_instance_id:
                self.successful_terminations += 1
                logger.warning(f"🐒💥 CHAOS MONKEY: Terminada instancia {terminated_instance_id} "
                             f"del servicio {service_name}")
                return terminated_instance_id
            else:
                self.blocked_terminations += 1
                logger.info(f"🛡️ Terminación bloqueada para {service_name} "
                           f"(protecciones de seguridad activas)")
                return None
                
        except Exception as e:
            logger.error(f"💥 Error terminando instancia de {service_name}: {e}")
            return None
    
    def _record_termination(self, service_name: str, instance_id: str):
        """
        Registra una terminación en el historial con timestamp y detalles.
        
        DATOS REGISTRADOS:
        - Timestamp exacto
        - Servicio afectado
        - ID de instancia terminada
        - Chaos Monkey responsable
        
        Args:
            service_name: Nombre del servicio afectado
            instance_id: ID de la instancia terminada
        """
        with self.lock:
            self.total_terminations += 1
            self.last_termination_time = time.time()
            
            termination_record = {
                "timestamp": self.last_termination_time,
                "service_name": service_name,
                "instance_id": instance_id,
                "chaos_monkey": self.name,
                "formatted_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.termination_history.append(termination_record)
            
            # ▓▓▓ MANTENER SOLO ÚLTIMAS 100 TERMINACIONES ▓▓▓
            if len(self.termination_history) > 100:
                self.termination_history.pop(0)
            
            logger.info(f"📝 Terminación registrada: {service_name}/{instance_id}")
    
    def force_chaos(self, service_name: str = None) -> Dict:
        """
        Fuerza la ejecución de chaos inmediatamente, ignorando horarios y probabilidades.
        
        USO TÍPICO:
        - Demostraciones en vivo
        - Testing manual
        - Validación de respuesta del sistema
        
        Args:
            service_name: Servicio específico a afectar, None para selección automática
            
        Returns:
            Dict: Resultado de la operación con detalles
        """
        if not self.is_enabled:
            return {
                "status": "error", 
                "message": "🚫 Chaos Monkey está deshabilitado",
                "chaos_monkey": self.name
            }
        
        # ▓▓▓ VALIDAR SERVICIO ESPECÍFICO ▓▓▓
        if service_name and service_name not in self.target_services:
            return {
                "status": "error", 
                "message": f"🚫 Servicio {service_name} no registrado",
                "chaos_monkey": self.name
            }
        
        # ▓▓▓ SELECCIONAR TARGET ▓▓▓
        target_service_name = service_name or self._select_target_service()
        
        if not target_service_name:
            return {
                "status": "error", 
                "message": "🚫 No hay servicios elegibles para terminación",
                "available_services": list(self.target_services.keys()),
                "chaos_monkey": self.name
            }
        
        target_service = self.target_services[target_service_name]
        
        # ▓▓▓ EJECUTAR TERMINACIÓN ▓▓▓
        instance_id = self._terminate_instance(target_service_name, target_service)
        
        if instance_id:
            self._record_termination(target_service_name, instance_id)
            
            # ▓▓▓ NOTIFICAR CALLBACKS ▓▓▓
            for callback in self.termination_callbacks:
                try:
                    callback(target_service_name, instance_id)
                except Exception as e:
                    logger.error(f"💥 Error en callback de terminación: {e}")
            
            return {
                "status": "success",
                "message": f"✅ Instancia {instance_id} del servicio {target_service_name} terminada",
                "service_name": target_service_name,
                "instance_id": instance_id,
                "chaos_monkey": self.name,
                "timestamp": time.time()
            }
        else:
            return {
                "status": "blocked",
                "message": f"🛡️ Terminación bloqueada para {target_service_name} por reglas de seguridad",
                "service_name": target_service_name,
                "chaos_monkey": self.name,
                "min_instances_required": self.min_healthy_instances
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
