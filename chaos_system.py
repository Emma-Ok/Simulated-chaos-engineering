"""
Sistema principal de Chaos Engineering.
Integra todos los componentes y proporciona una interfaz unificada.
"""

import time
import threading
import logging
from typing import Dict, List, Optional, Any

# Importar componentes principales
from core.service import Service, ServiceType
from core.load_balancer import LoadBalancer, LoadBalancingStrategy
from core.monitoring import MonitoringSystem
from core.patterns import ResiliencePatterns, CircuitBreakerConfig

# Importar componentes de chaos
from chaos.chaos_monkey import ChaosMonkey
from chaos.runner import ExperimentRunner

# Importar utilidades
from utils.helpers import load_config, setup_colored_logging, format_timestamp
from utils.reports import ReportGenerator

logger = logging.getLogger(__name__)

class ChaosEngineeringSystem:
    """
    Sistema principal que orquesta todos los componentes de Chaos Engineering.
    Proporciona una interfaz unificada para configurar, ejecutar y monitorear experimentos.
    """
    
    def __init__(self, config_path: str = None):
        # Configuración
        self.config = {}
        if config_path:
            self.config = load_config(config_path)
        
        # Componentes principales
        self.services: Dict[str, Service] = {}
        self.load_balancer: Optional[LoadBalancer] = None
        self.monitoring: Optional[MonitoringSystem] = None
        self.chaos_monkey: Optional[ChaosMonkey] = None
        self.experiment_runner: Optional[ExperimentRunner] = None
        self.report_generator: Optional[ReportGenerator] = None
        
        # Estado del sistema
        self.is_running = False
        self.start_time = None
        
        # Patrones de resiliencia
        self.resilience_patterns: Dict[str, ResiliencePatterns] = {}
        
        # Threading
        self.system_thread = None
        self.lock = threading.RLock()
        
        logger.info("🔥 ChaosEngineeringSystem inicializado")
    
    def initialize(self):
        """
        Inicializa todos los componentes del sistema basándose en la configuración.
        """
        logger.info("🚀 Inicializando sistema de Chaos Engineering...")
        
        try:
            # Inicializar componentes base
            self._initialize_load_balancer()
            self._initialize_services()
            self._initialize_monitoring()
            self._initialize_chaos_components()
            self._initialize_reports()
            
            # Configurar patrones de resiliencia
            self._setup_resilience_patterns()
            
            # Aplicar configuración
            self._apply_configuration()
            
            logger.info("✅ Sistema inicializado correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error inicializando sistema: {e}")
            raise
    
    def _initialize_load_balancer(self):
        """Inicializa el load balancer"""
        lb_config = self.config.get("load_balancer", {})
        strategy_name = lb_config.get("strategy", "health_based")
        
        try:
            strategy = LoadBalancingStrategy(strategy_name)
        except ValueError:
            logger.warning(f"Estrategia de LB inválida: {strategy_name}, usando health_based")
            strategy = LoadBalancingStrategy.HEALTH_BASED
        
        self.load_balancer = LoadBalancer("main-lb", strategy)
        
        # Registrar servicios existentes en el load balancer
        self._register_existing_services_in_component(self.load_balancer, "register_service")
        
        logger.info(f"Load Balancer inicializado con estrategia: {strategy.value}")
    
    def _initialize_services(self):
        """Inicializa los servicios configurados"""
        services_config = self.config.get("services", {})
        
        for service_name, service_config in services_config.items():
            try:
                # Determinar tipo de servicio
                service_type_str = service_config.get("type", "api-gateway")
                service_type = ServiceType(service_type_str)
                
                # Crear servicio
                service = Service(
                    name=service_name,
                    service_type=service_type,
                    initial_instances=service_config.get("initial_instances", 2),
                    region=service_config.get("region", "us-east-1")
                )
                
                # Configurar límites
                service.min_instances = service_config.get("min_instances", 1)
                service.max_instances = service_config.get("max_instances", 10)
                
                self.services[service_name] = service
                
                # Registrar en load balancer
                if self.load_balancer:
                    self.load_balancer.register_service(service)
                
                logger.info(f"Servicio {service_name} inicializado con {service_config.get('initial_instances', 2)} instancias")
                
            except Exception as e:
                logger.error(f"Error inicializando servicio {service_name}: {e}")
    
    def _initialize_monitoring(self):
        """Inicializa el sistema de monitoreo"""
        monitoring_config = self.config.get("monitoring", {})
        collection_interval = monitoring_config.get("collection_interval_seconds", 5)
        
        self.monitoring = MonitoringSystem(collection_interval)
        
        # Registrar componentes para monitoreo
        if self.load_balancer:
            self.monitoring.register_component("load_balancer", self.load_balancer)
        
        for service_name, service in self.services.items():
            self.monitoring.register_component(service_name, service)
        
        # Configurar alertas personalizadas
        alert_thresholds = monitoring_config.get("alert_thresholds", {})
        for metric, threshold in alert_thresholds.items():
            if metric == "response_time_ms":
                self.monitoring.alert_manager.add_alert_rule({
                    "name": f"high_{metric}",
                    "metric": metric,
                    "threshold": threshold,
                    "operator": ">",
                    "severity": "HIGH",
                    "message": f"Tiempo de respuesta alto: {threshold}ms"
                })
        
        logger.info("Sistema de monitoreo inicializado")
    
    def _initialize_chaos_components(self):
        """Inicializa los componentes de chaos engineering"""
        # Chaos Monkey
        self.chaos_monkey = ChaosMonkey()
        
        # Configurar Chaos Monkey
        if "experiments" in self.config or "targets" in self.config or "schedule" in self.config:
            chaos_config = {
                "enabled": self.config.get("enabled", True),
                "schedule": self.config.get("schedule", {}),
                "targets": self.config.get("targets", {}),
                "experiments": self.config.get("experiments", {})
            }
            self.chaos_monkey.configure(chaos_config)
        
        # Registrar servicios en Chaos Monkey
        for service_name, service in self.services.items():
            self.chaos_monkey.register_service(service_name, service)
        
        # Experiment Runner
        self.experiment_runner = ExperimentRunner()
        
        # Configurar seguridad
        safety_config = self.config.get("safety", {})
        self.experiment_runner.set_safety_mode(
            enabled=safety_config.get("enabled", True),
            dry_run=safety_config.get("dry_run_mode", False),
            require_confirmation=safety_config.get("require_confirmation_for_destructive", True)
        )
        
        # Registrar servicios en Experiment Runner
        for service_name, service in self.services.items():
            self.experiment_runner.register_service(service_name, service)
        
        logger.info("Componentes de chaos engineering inicializados")
    
    def _initialize_reports(self):
        """Inicializa el generador de reportes"""
        reporting_config = self.config.get("reporting", {})
        output_dir = reporting_config.get("output_directory", "./reports")
        
        self.report_generator = ReportGenerator(output_dir)
        logger.info(f"Generador de reportes inicializado: {output_dir}")
    
    def _setup_resilience_patterns(self):
        """Configura patrones de resiliencia para servicios críticos"""
        for service_name, service in self.services.items():
            # Crear patrones de resiliencia para cada servicio
            patterns = ResiliencePatterns(f"{service_name}-resilience")
            
            # Circuit breaker para servicios críticos
            if service.service_type in [ServiceType.DATABASE, ServiceType.AUTH_SERVICE]:
                cb_config = CircuitBreakerConfig(
                    failure_threshold=5,
                    success_threshold=3,
                    timeout_seconds=60
                )
                patterns.with_circuit_breaker(cb_config)
            
            # Bulkhead para servicios con alta carga
            if service.service_type == ServiceType.API_GATEWAY:
                patterns.with_bulkhead(max_concurrent=20)
            
            # Retry para servicios de red
            patterns.with_retry(max_attempts=3, base_delay=1.0)
            
            # Rate limiting
            patterns.with_rate_limiter(rate=100, burst_size=200)
            
            # Timeout
            patterns.with_timeout(default_timeout=30.0)
            
            self.resilience_patterns[service_name] = patterns
        
        logger.info(f"Patrones de resiliencia configurados para {len(self.resilience_patterns)} servicios")
    
    def _apply_configuration(self):
        """Aplica configuraciones específicas del archivo de config"""
        # Configurar exclusiones de servicios
        targets_config = self.config.get("targets", {})
        excluded_services = targets_config.get("excluded_services", [])
        
        for service_name in excluded_services:
            self.chaos_monkey.exclude_service(service_name)
        
        logger.info("Configuración aplicada")
    
    def start(self):
        """Inicia el sistema completo"""
        if self.is_running:
            logger.warning("El sistema ya está en ejecución")
            return
        
        logger.info("🚀 Iniciando sistema de Chaos Engineering...")
        
        try:
            self.is_running = True
            self.start_time = time.time()
            
            # Inicializar si no se ha hecho
            if not self.services:
                self.initialize()
            
            # Iniciar monitoreo
            if self.monitoring:
                self.monitoring.start_monitoring()
            
            # Iniciar Chaos Monkey
            if self.chaos_monkey and self.chaos_monkey.is_enabled:
                self.chaos_monkey.start()
            
            # Iniciar simulación de tráfico
            if self.load_balancer:
                self.load_balancer.simulate_traffic(
                    requests_per_second=10,
                    duration_seconds=3600  # 1 hora
                )
            
            # Iniciar hilo de mantenimiento del sistema
            self.system_thread = threading.Thread(target=self._system_maintenance_loop, daemon=True)
            self.system_thread.start()
            
            logger.info("✅ Sistema iniciado correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error iniciando sistema: {e}")
            self.is_running = False
            raise
    
    def stop(self):
        """Detiene el sistema completo"""
        logger.info("🛑 Deteniendo sistema de Chaos Engineering...")
        
        self.is_running = False
        
        # Detener Chaos Monkey
        if self.chaos_monkey:
            self.chaos_monkey.stop()
        
        # Detener experimentos activos
        if self.experiment_runner:
            self.experiment_runner.stop_all_experiments()
        
        # Detener monitoreo
        if self.monitoring:
            self.monitoring.stop_monitoring()
        
        # Cerrar servicios
        for service in self.services.values():
            service.shutdown()
        
        # Cerrar load balancer
        if self.load_balancer:
            self.load_balancer.shutdown()
        
        logger.info("✅ Sistema detenido")
    
    def _system_maintenance_loop(self):
        """Loop de mantenimiento del sistema"""
        while self.is_running:
            try:
                self._maybe_generate_automatic_report()
                self._perform_system_health_check()
                time.sleep(60)
            except Exception as e:
                logger.error(f"Error en loop de mantenimiento: {e}")
                time.sleep(10)

    def _maybe_generate_automatic_report(self):
        """Verifica si es momento de generar un reporte automático y lo genera si corresponde."""
        if not self.report_generator:
            return
        reporting_config = self.config.get("reporting", {})
        if not reporting_config.get("enabled", True):
            return
        interval_hours = reporting_config.get("auto_generate_interval_hours", 1)
        if hasattr(self, '_last_report_time'):
            if time.time() - self._last_report_time > interval_hours * 3600:
                self._generate_automatic_report()
        else:
            self._last_report_time = time.time()
    
    def _generate_automatic_report(self):
        """Genera un reporte automático"""
        try:
            formats = self.config.get("reporting", {}).get("formats", ["html"])
            include_charts = self.config.get("reporting", {}).get("include_charts", True)
            
            self.report_generator.generate_comprehensive_report(
                chaos_system=self,
                include_charts=include_charts,
                formats=formats
            )
            
            self._last_report_time = time.time()
            logger.info("Reporte automático generado")
            
        except Exception as e:
            logger.error(f"Error generando reporte automático: {e}")
    
    def _perform_system_health_check(self):
        """Realiza un health check general del sistema"""
        try:
            # Verificar servicios
            unhealthy_services = []
            for service_name, service in self.services.items():
                healthy_instances = service.get_healthy_instances()
                if len(healthy_instances) < service.min_instances:
                    unhealthy_services.append(service_name)
            
            if unhealthy_services:
                logger.warning(f"Servicios con instancias insuficientes: {unhealthy_services}")
            
            # Verificar load balancer
            if self.load_balancer:
                lb_metrics = self.load_balancer.get_load_balancer_metrics()
                error_rate = lb_metrics["traffic_metrics"]["error_rate"]
                
                if error_rate > 10:  # 10% de errores
                    logger.warning(f"Tasa de errores alta en Load Balancer: {error_rate:.2f}%")
            
        except Exception as e:
            logger.error(f"Error en health check del sistema: {e}")
    
    # Métodos de interfaz pública
    
    def add_service(self, service_name: str, service_type: str, instances: int = 2, 
                   region: str = "us-east-1") -> bool:
        """Añade un nuevo servicio al sistema"""
        try:
            service_type_enum = ServiceType(service_type)
            service = Service(service_name, service_type_enum, initial_instances=instances, region=region)
            
            with self.lock:
                self.services[service_name] = service
                
                # Registrar en componentes
                if self.load_balancer:
                    self.load_balancer.register_service(service)
                
                if self.monitoring:
                    self.monitoring.register_component(service_name, service)
                
                if self.chaos_monkey:
                    self.chaos_monkey.register_service(service_name, service)
                
                if self.experiment_runner:
                    self.experiment_runner.register_service(service_name, service)
            
            logger.info(f"Servicio {service_name} añadido con {instances} instancias")
            return True
            
        except Exception as e:
            logger.error(f"Error añadiendo servicio {service_name}: {e}")
            return False
    
    def remove_service(self, service_name: str) -> bool:
        """Remueve un servicio del sistema"""
        try:
            with self.lock:
                if service_name not in self.services:
                    logger.warning(f"Servicio {service_name} no encontrado")
                    return False
                
                service = self.services[service_name]
                service.shutdown()
                
                # Desregistrar de componentes
                if self.load_balancer:
                    self.load_balancer.unregister_service(service_name)
                
                if self.chaos_monkey:
                    self.chaos_monkey.unregister_service(service_name)
                
                del self.services[service_name]
            
            logger.info(f"Servicio {service_name} removido")
            return True
            
        except Exception as e:
            logger.error(f"Error removiendo servicio {service_name}: {e}")
            return False
    
    def run_chaos_experiment(self, experiment_type: str, **kwargs) -> str:
        """Ejecuta un experimento de chaos"""
        if not self.experiment_runner:
            raise RuntimeError("ExperimentRunner no inicializado")
        
        try:
            if experiment_type == "latency":
                exp_id = self.experiment_runner.create_latency_experiment(**kwargs)
            elif experiment_type == "resource_exhaustion":
                exp_id = self.experiment_runner.create_resource_exhaustion_experiment(**kwargs)
            elif experiment_type == "network_partition":
                exp_id = self.experiment_runner.create_network_partition_experiment(**kwargs)
            elif experiment_type == "chaos_gorilla":
                exp_id = self.experiment_runner.create_chaos_gorilla_experiment(**kwargs)
            elif experiment_type == "chaos_kong":
                exp_id = self.experiment_runner.create_chaos_kong_experiment(**kwargs)
            elif experiment_type == "doctor_monkey":
                exp_id = self.experiment_runner.create_doctor_monkey_experiment(**kwargs)
            else:
                raise ValueError(f"Tipo de experimento desconocido: {experiment_type}")
            
            # Iniciar experimento
            success = self.experiment_runner.start_experiment(exp_id)
            
            if success:
                logger.info(f"Experimento {experiment_type} iniciado con ID: {exp_id}")
                return exp_id
            else:
                raise RuntimeError("Error iniciando experimento")
                
        except Exception as e:
            logger.error(f"Error ejecutando experimento {experiment_type}: {e}")
            raise
    
    def force_chaos_monkey(self, service_name: str = None) -> Dict:
        """Fuerza la ejecución del Chaos Monkey"""
        if not self.chaos_monkey:
            raise RuntimeError("Chaos Monkey no inicializado")
        
        return self.chaos_monkey.force_chaos(service_name)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el estado completo del sistema"""
        with self.lock:
            status = {
                "timestamp": time.time(),
                "uptime_seconds": time.time() - self.start_time if self.start_time else 0,
                "is_running": self.is_running,
                "services": {},
                "load_balancer": {},
                "monitoring": {},
                "chaos_monkey": {},
                "experiments": {}
            }
            
            # Estado de servicios
            for service_name, service in self.services.items():
                status["services"][service_name] = service.get_service_metrics()
            
            # Estado del load balancer
            if self.load_balancer:
                status["load_balancer"] = self.load_balancer.get_load_balancer_metrics()
            
            # Estado del monitoreo
            if self.monitoring:
                status["monitoring"] = self.monitoring.get_dashboard_data()
            
            # Estado del Chaos Monkey
            if self.chaos_monkey:
                status["chaos_monkey"] = self.chaos_monkey.get_statistics()
            
            # Estado de experimentos
            if self.experiment_runner:
                status["experiments"] = self.experiment_runner.get_all_experiments_status()
            
            return status
    
    def generate_report(self, formats: List[str] = None, include_charts: bool = True) -> Dict[str, str]:
        """Genera un reporte del sistema"""
        if not self.report_generator:
            raise RuntimeError("ReportGenerator no inicializado")
        
        return self.report_generator.generate_comprehensive_report(
            chaos_system=self,
            include_charts=include_charts,
            formats=formats or ["html", "json"]
        )
    
    def emergency_stop(self):
        """Parada de emergencia del sistema"""
        logger.critical("🚨 PARADA DE EMERGENCIA ACTIVADA")
        
        # Detener todos los experimentos
        if self.experiment_runner:
            self.experiment_runner.emergency_stop()
        
        # Detener Chaos Monkey
        if self.chaos_monkey:
            self.chaos_monkey.stop()
        
        # Detener sistema
        self.stop()
        
        logger.critical("🚨 Parada de emergencia completada")
    
    def run_simulation(self, duration_minutes: int = 30):
        """
        Ejecuta una simulación completa con tráfico y experimentos.
        Método principal para demostraciones.
        """
        logger.info(f"🎮 Iniciando simulación de {duration_minutes} minutos")
        try:
            if not self.is_running:
                self.initialize()
                self.start()
            simulation_start = time.time()
            end_time = simulation_start + (duration_minutes * 60)
            self._monitor_simulation(simulation_start, end_time)
            logger.info("📊 Generando reporte final de simulación...")
            report_files = self.generate_report(formats=["html", "json"])
            logger.info(f"✅ Simulación completada. Reporte: {report_files}")
        except Exception as e:
            logger.error(f"❌ Error en simulación: {e}")
            raise
        finally:
            logger.info("🧹 Limpiando simulación...")

    def _get_default_experiment_schedule(self):
        """Devuelve la programación por defecto de experimentos automáticos."""
        first_service = list(self.services.keys())[0] if self.services else None
        return [
            {"delay": 60, "type": "doctor_monkey", "name": "health-check-1"},
            {"delay": 300, "type": "latency", "name": "latency-test-1", "target_service": first_service},
            {"delay": 600, "type": "resource_exhaustion", "name": "cpu-test-1", "target_service": first_service},
        ]

    def _schedule_experiments(self, experiment_schedule, duration_minutes):
        """Programa los experimentos automáticos en hilos separados."""
        scheduled_experiments = []
        for schedule in experiment_schedule:
            if schedule["delay"] < duration_minutes * 60:
                exp_thread = threading.Thread(
                    target=self._run_scheduled_experiment, args=(schedule,), daemon=True
                )
                exp_thread.start()
                scheduled_experiments.append(exp_thread)
        return scheduled_experiments

    def _run_scheduled_experiment(self, exp_schedule):
        """Ejecuta un experimento programado después de un retardo."""
        time.sleep(exp_schedule["delay"])
        try:
            kwargs = {k: v for k, v in exp_schedule.items() if k not in ["delay", "type"]}
            if exp_schedule.get("target_service"):
                self.run_chaos_experiment(exp_schedule["type"], **kwargs)
        except Exception as e:
            logger.error(f"Error en experimento programado: {e}")

    def _monitor_simulation(self, simulation_start, end_time):
        """Monitorea la simulación y muestra el estado periódicamente."""
        last_status_time = 0
        while time.time() < end_time and self.is_running:
            current_time = time.time()
            if current_time - last_status_time > 120:
                elapsed = (current_time - simulation_start) / 60
                remaining = (end_time - current_time) / 60
                logger.info(f"📊 Simulación - Transcurrido: {elapsed:.1f}m, Restante: {remaining:.1f}m")
                self._log_basic_metrics()
                last_status_time = current_time
            time.sleep(10)

    def _log_basic_metrics(self):
        """Muestra métricas básicas y alertas activas."""
        if self.monitoring:
            dashboard = self.monitoring.get_dashboard_data()
            active_alerts = len(dashboard.get("alerts", []))
            if active_alerts > 0:
                logger.warning(f"⚠️ Alertas activas: {active_alerts}")
    
    def configure_experiments(self, config: Dict[str, Any]):
        """Configura experimentos basándose en un diccionario de configuración"""
        if self.chaos_monkey:
            self.chaos_monkey.configure(config)
        
        if self.experiment_runner:
            safety_config = config.get("safety", {})
            self.experiment_runner.set_safety_mode(
                enabled=safety_config.get("enabled", True),
                dry_run=safety_config.get("dry_run_mode", False),
                require_confirmation=safety_config.get("require_confirmation_for_destructive", True)
            )
        
        logger.info("Configuración de experimentos aplicada")
    
    def __enter__(self):
        """Soporte para context manager"""
        self.initialize()
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Soporte para context manager"""
        self.stop()

    def _register_existing_services_in_component(self, component, method_name):
        """Registra todos los servicios existentes en un componente específico"""
        if not component:
            return
            
        for service_name, service in self.services.items():
            try:
                if hasattr(component, method_name):
                    if method_name == "register_service":
                        getattr(component, method_name)(service)
                    else:
                        getattr(component, method_name)(service_name, service)
                    logger.debug(f"Servicio {service_name} registrado en {component.__class__.__name__}")
            except Exception as e:
                logger.warning(f"Error registrando servicio {service_name} en {component.__class__.__name__}: {e}")
