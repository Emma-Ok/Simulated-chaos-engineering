"""
Sistema principal de Chaos Engineering.
Integra todos los componentes y proporciona una interfaz unificada.

TIEMPOS OPTIMIZADOS PARA DEMO:
- Simulación máxima: 4 minutos
- Tráfico por defecto: 4 minutos
- Experimentos programados: intervalos cortos
- Mantenimiento del sistema: cada minuto
"""

import time
import threading
import logging
from typing import Dict, List, Optional, Any
import random # Added for _configure_service_variability

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
    
    CARACTERÍSTICAS PRINCIPALES:
    - Gestión de servicios distribuidos
    - Ejecución de experimentos de chaos
    - Monitoreo en tiempo real
    - Generación de reportes
    - Patrones de resiliencia
    
    OPTIMIZADO PARA DEMOS RÁPIDAS:
    - Tiempos de simulación cortos (4 minutos máximo)
    - Intervalos de monitoreo frecuentes
    - Recuperación automática rápida
    """
    
    def __init__(self, config_path: str = None):
        # ═══════════════════════════════════════════════════════════════════
        # CONFIGURACIÓN INICIAL
        # ═══════════════════════════════════════════════════════════════════
        self.config = {}
        if config_path:
            self.config = load_config(config_path)
        
        # ═══════════════════════════════════════════════════════════════════
        # COMPONENTES PRINCIPALES
        # ═══════════════════════════════════════════════════════════════════
        self.services: Dict[str, Service] = {}              # Servicios registrados
        self.load_balancer: Optional[LoadBalancer] = None   # Balanceador de carga
        self.monitoring: Optional[MonitoringSystem] = None  # Sistema de monitoreo
        self.chaos_monkey: Optional[ChaosMonkey] = None     # Motor de chaos
        self.experiment_runner: Optional[ExperimentRunner] = None  # Ejecutor de experimentos
        self.report_generator: Optional[ReportGenerator] = None    # Generador de reportes
        
        # ═══════════════════════════════════════════════════════════════════
        # ESTADO DEL SISTEMA
        # ═══════════════════════════════════════════════════════════════════
        self.is_running = False          # Estado de ejecución
        self.start_time = None          # Momento de inicio
        
        # ═══════════════════════════════════════════════════════════════════
        # PATRONES DE RESILIENCIA
        # ═══════════════════════════════════════════════════════════════════
        self.resilience_patterns: Dict[str, ResiliencePatterns] = {}
        
        # ═══════════════════════════════════════════════════════════════════
        # THREADING PARA OPERACIONES ASÍNCRONAS
        # ═══════════════════════════════════════════════════════════════════
        self.system_thread = None       # Hilo de mantenimiento
        self.lock = threading.RLock()   # Lock para thread safety
        
        logger.info("🔥 ChaosEngineeringSystem inicializado")
    
    def initialize(self):
        """
        Inicializa todos los componentes del sistema basándose en la configuración.
        
        ORDEN DE INICIALIZACIÓN:
        1. Load Balancer (distribución de tráfico)
        2. Servicios (arquitectura distribuida)
        3. Monitoreo (observabilidad)
        4. Chaos Components (experimentos)
        5. Reportes (análisis)
        6. Patrones de Resiliencia (protección)
        """
        logger.info("🚀 Inicializando sistema de Chaos Engineering...")
        
        try:
            # ▓▓▓ FASE 1: Inicializar componentes base ▓▓▓
            self._initialize_load_balancer()
            self._initialize_services()
            self._initialize_monitoring()
            self._initialize_chaos_components()
            self._initialize_reports()
            
            # ▓▓▓ FASE 2: Configurar patrones avanzados ▓▓▓
            self._setup_resilience_patterns()
            
            # ▓▓▓ FASE 3: Aplicar configuración final ▓▓▓
            self._apply_configuration()
            
            logger.info("✅ Sistema inicializado correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error inicializando sistema: {e}")
            raise
    
    def _initialize_load_balancer(self):
        """Inicializa el balanceador de carga con estrategia configurada para mejor distribución"""
        lb_config = self.config.get("load_balancer", {})
        strategy_name = lb_config.get("strategy", "round_robin")  # Cambiado de health_based a round_robin
        
        try:
            strategy = LoadBalancingStrategy(strategy_name)
        except ValueError:
            logger.warning(f"Estrategia de LB inválida: {strategy_name}, usando round_robin")
            strategy = LoadBalancingStrategy.ROUND_ROBIN  # Cambiado de HEALTH_BASED a ROUND_ROBIN
        
        self.load_balancer = LoadBalancer("main-lb", strategy)
        
        # Registrar servicios existentes en el load balancer
        self._register_existing_services_in_component(self.load_balancer, "register_service")
        
        logger.info(f"⚖️ Load Balancer inicializado con estrategia: {strategy.value}")
    
    def _initialize_services(self):
        """
        Inicializa servicios con configuración optimizada para demos.
        
        SERVICIOS CONFIGURADOS:
        - API Service: 5 instancias (puerto web)
        - Auth Service: 4 instancias (autenticación)  
        - Database Service: 3 instancias (persistencia)
        - Cache Service: 4 instancias (memoria)
        
        OPTIMIZACIONES:
        - Más instancias para mejores métricas
        - Configuración variada para diferentes comportamientos
        - Regiones distribuidas para simular geo-distribución
        """
        service_configs = [
            {
                "name": "api-service",
                "type": ServiceType.API_GATEWAY,
                "instances": 5,  # Aumentado de 3 a 5
                "min_instances": 2,
                "max_instances": 10
            },
            {
                "name": "auth-service", 
                "type": ServiceType.AUTH_SERVICE,  # Corregido de AUTHENTICATION a AUTH_SERVICE
                "instances": 4,  # Aumentado de 2 a 4
                "min_instances": 2,
                "max_instances": 8
            },
            {
                "name": "db-service",
                "type": ServiceType.DATABASE,
                "instances": 3,  # Instancias conservadoras para DB
                "min_instances": 2,
                "max_instances": 6
            },
            {
                "name": "cache-service",
                "type": ServiceType.CACHE,
                "instances": 4,  # Aumentado de 2 a 4
                "min_instances": 2,
                "max_instances": 8
            }
        ]
        
        logger.info("🏗️ Inicializando servicios con configuración optimizada...")
        
        for config in service_configs:
            try:
                service = Service(
                    name=config["name"],
                    service_type=config["type"],
                    initial_instances=config["instances"],
                    min_instances=config["min_instances"],
                    max_instances=config["max_instances"]
                )
                
                self.services[config["name"]] = service
                logger.info(f"✅ Servicio {config['name']} creado con {config['instances']} instancias")
                
            except Exception as e:
                logger.error(f"❌ Error creando servicio {config['name']}: {e}")
                raise
        
        # Configurar variabilidad en las instancias para métricas más interesantes
        self._configure_service_variability()
        
        # Registrar servicios en el load balancer
        self._register_existing_services_in_component(self.load_balancer, "register_service")
        
        logger.info(f"✅ {len(self.services)} servicios inicializados con "
                   f"{sum(len(s.instances) for s in self.services.values())} instancias totales")

    def _configure_service_variability(self):
        """
        Configura variabilidad en servicios para generar métricas más interesantes.
        
        OPTIMIZACIONES:
        - Diferentes regiones para geo-distribución
        - Latencias base variadas
        - Probabilidades de error ligeramente diferentes
        """
        regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]
        
        for service_name, service in self.services.items():
            # Distribuir instancias en diferentes regiones
            instances_list = list(service.instances.values())
            for i, instance in enumerate(instances_list):
                instance.region = regions[i % len(regions)]
                
                # Configurar latencias base diferentes por servicio
                if service.service_type == ServiceType.DATABASE:
                    instance.base_response_time = random.uniform(100, 300)  # DB más lenta
                elif service.service_type == ServiceType.CACHE:
                    instance.base_response_time = random.uniform(20, 80)    # Cache más rápida
                elif service.service_type == ServiceType.API_GATEWAY:
                    instance.base_response_time = random.uniform(50, 150)   # API intermedia
                elif service.service_type == ServiceType.AUTH_SERVICE:  # Corregido
                    instance.base_response_time = random.uniform(70, 200)   # Auth intermedia-lenta
                else:
                    instance.base_response_time = random.uniform(70, 200)   # Default intermedia-lenta
                
                # Pequeñas variaciones en error probability para realismo
                base_error = 0.005  # 0.5% base
                variation = random.uniform(0.8, 1.5)  # ±50% variación
                instance.error_probability = base_error * variation
        
        logger.info("🔧 Variabilidad configurada en servicios para métricas realistas")
    
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
        """
        Inicia el sistema completo con configuración optimizada para demos.
        
        PROCESOS QUE SE INICIAN:
        - Sistema de monitoreo (intervalos cortos)
        - Chaos Monkey (si está habilitado)
        - Simulación de tráfico (duración limitada)
        - Mantenimiento automático (cada minuto)
        """
        if self.is_running:
            logger.warning("El sistema ya está en ejecución")
            return
        
        logger.info("🚀 Iniciando sistema de Chaos Engineering...")
        
        try:
            self.is_running = True
            self.start_time = time.time()
            
            # ▓▓▓ INICIALIZACIÓN AUTOMÁTICA ▓▓▓
            if not self.services:
                self.initialize()
            
            # ▓▓▓ INICIAR MONITOREO ▓▓▓
            if self.monitoring:
                self.monitoring.start_monitoring()
                logger.info("📊 Sistema de monitoreo iniciado")
            
            # ▓▓▓ INICIAR CHAOS MONKEY ▓▓▓
            if self.chaos_monkey and self.chaos_monkey.is_enabled:
                self.chaos_monkey.start()
                logger.info("🐒 Chaos Monkey activado")
            
            # ▓▓▓ INICIAR SIMULACIÓN DE TRÁFICO (OPTIMIZADO) ▓▓▓
            if self.load_balancer:
                # OPTIMIZADO: Tráfico moderado para evitar saturación durante chaos
                self.load_balancer.simulate_traffic(
                    requests_per_second=8,      # Reducido de 15 a 8 para menos errores
                    duration_seconds=240        # 4 minutos
                )
                logger.info("🌐 Simulación de tráfico iniciada (8 RPS, 4 minutos)")
            
            # ▓▓▓ INICIAR MANTENIMIENTO DEL SISTEMA ▓▓▓
            self.system_thread = threading.Thread(target=self._system_maintenance_loop, daemon=True)
            self.system_thread.start()
            logger.info("🔧 Mantenimiento del sistema iniciado")
            
            logger.info("✅ Sistema iniciado correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error iniciando sistema: {e}")
            self.is_running = False
            raise
    
    def stop(self):
        """
        Detiene el sistema completo de forma ordenada y sin duplicaciones.
        
        ORDEN DE PARADA:
        1. Marcar sistema como detenido
        2. Detener experimentos activos
        3. Detener Chaos Monkey
        4. Detener monitoreo
        5. Cerrar load balancer (que cierra servicios)
        """
        logger.info("🛑 Deteniendo sistema de Chaos Engineering...")
        
        self.is_running = False
        
        # ▓▓▓ DETENER EXPERIMENTOS ▓▓▓
        if self.experiment_runner:
            self.experiment_runner.stop_all_experiments()
        
        # ▓▓▓ DETENER CHAOS MONKEY ▓▓▓
        if self.chaos_monkey:
            self.chaos_monkey.stop()
        
        # ▓▓▓ DETENER MONITOREO ▓▓▓
        if self.monitoring:
            self.monitoring.stop_monitoring()
        
        # ▓▓▓ CERRAR LOAD BALANCER (incluye servicios) ▓▓▓
        if self.load_balancer:
            self.load_balancer.shutdown()
        else:
            # Si no hay load balancer, cerrar servicios directamente
            for service in self.services.values():
                service.shutdown()
        
        logger.info("✅ Sistema detenido")
    
    def _system_maintenance_loop(self):
        """
        Loop de mantenimiento del sistema con intervalos optimizados para demos.
        
        TAREAS DE MANTENIMIENTO:
        - Generación automática de reportes
        - Health checks del sistema
        - Limpieza de recursos
        
        FRECUENCIA: Cada 30 segundos (vs 60 segundos original)
        """
        while self.is_running:
            try:
                self._maybe_generate_automatic_report()
                self._perform_system_health_check()
                time.sleep(30)  # ⏱️ OPTIMIZADO: 30s vs 60s original
            except Exception as e:
                logger.error(f"Error en loop de mantenimiento: {e}")
                time.sleep(10)

    def _maybe_generate_automatic_report(self):
        """
        Verifica si es momento de generar un reporte automático.
        
        OPTIMIZADO: Genera reportes cada 30 minutos (vs 1 hora original)
        """
        if not self.report_generator:
            return
        reporting_config = self.config.get("reporting", {})
        if not reporting_config.get("enabled", True):
            return
        
        # ⏱️ OPTIMIZADO: 0.5 horas (30 minutos) vs 1 hora original
        interval_hours = reporting_config.get("auto_generate_interval_hours", 0.5)
        
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
    
    def run_simulation(self, duration_minutes: int = 4):
        """
        Ejecuta una simulación completa con tráfico y experimentos.
        
        CARACTERÍSTICAS DE LA SIMULACIÓN:
        - Duración por defecto: 4 minutos (vs 30 minutos original)
        - Experimentos programados automáticamente
        - Monitoreo continuo
        - Reporte final automático
        
        Args:
            duration_minutes: Duración de la simulación (máximo recomendado: 4)
        """
        # ⚠️ VALIDACIÓN DE TIEMPO MÁXIMO
        if duration_minutes > 4:
            logger.warning(f"⚠️ Duración {duration_minutes}min excede el máximo recomendado de 4min")
        
        logger.info(f"🎮 Iniciando simulación de {duration_minutes} minutos")
        try:
            if not self.is_running:
                self.initialize()
                self.start()
            
            simulation_start = time.time()
            end_time = simulation_start + (duration_minutes * 60)
            
            # ▓▓▓ PROGRAMAR EXPERIMENTOS AUTOMÁTICOS ▓▓▓
            self._schedule_demo_experiments(duration_minutes)
            
            # ▓▓▓ MONITOREAR SIMULACIÓN ▓▓▓
            self._monitor_simulation(simulation_start, end_time)
            
            # ▓▓▓ GENERAR REPORTE FINAL ▓▓▓
            logger.info("📊 Generando reporte final de simulación...")
            report_files = self.generate_report(formats=["html", "json"])
            logger.info(f"✅ Simulación completada. Reporte: {report_files}")
            
        except Exception as e:
            logger.error(f"❌ Error en simulación: {e}")
            raise
        finally:
            logger.info("🧹 Limpiando simulación...")

    def _schedule_demo_experiments(self, duration_minutes: int):
        """
        Programa experimentos automáticos optimizados para la duración de la demo.
        
        EXPERIMENTOS PROGRAMADOS:
        - Doctor Monkey: Diagnóstico inicial (30s)
        - Latency Test: Prueba de latencia (60s después)
        - Resource Test: Agotamiento de recursos (120s después, si hay tiempo)
        """
        if duration_minutes < 2:
            logger.info("⏱️ Simulación muy corta, sin experimentos automáticos")
            return
        
        first_service = list(self.services.keys())[0] if self.services else None
        if not first_service:
            logger.warning("No hay servicios disponibles para experimentos")
            return
        
        # ▓▓▓ EXPERIMENTOS OPTIMIZADOS PARA TIEMPO CORTO ▓▓▓
        experiments = [
            {"delay": 30, "type": "doctor_monkey", "name": "health-check-demo"},  # 30s después del inicio
        ]
        
        # Solo añadir más experimentos si hay tiempo suficiente
        if duration_minutes >= 3:
            experiments.append({
                "delay": 90, "type": "latency", "name": "latency-demo", 
                "target_service": first_service, "latency_ms": 400, "duration_seconds": 60
            })
        
        if duration_minutes >= 4:
            experiments.append({
                "delay": 180, "type": "resource_exhaustion", "name": "resource-demo",
                "target_service": first_service, "resource_type": "cpu", "duration_seconds": 60
            })
        
        # ▓▓▓ PROGRAMAR EXPERIMENTOS EN HILOS SEPARADOS ▓▓▓
        for experiment in experiments:
            exp_thread = threading.Thread(
                target=self._run_scheduled_experiment, 
                args=(experiment,), 
                daemon=True
            )
            exp_thread.start()
        
        logger.info(f"🧪 {len(experiments)} experimentos programados para {duration_minutes} minutos")

    def _run_scheduled_experiment(self, exp_schedule):
        """
        Ejecuta un experimento programado después de un retardo.
        
        MANEJO DE ERRORES: Captura y registra errores sin interrumpir la simulación
        """
        time.sleep(exp_schedule["delay"])
        
        if not self.is_running:
            logger.debug("Sistema detenido, cancelando experimento programado")
            return
        
        try:
            kwargs = {k: v for k, v in exp_schedule.items() if k not in ["delay", "type"]}
            exp_id = self.run_chaos_experiment(exp_schedule["type"], **kwargs)
            logger.info(f"🔬 Experimento programado iniciado: {exp_schedule['type']} ({exp_id})")
        except Exception as e:
            logger.error(f"Error en experimento programado {exp_schedule.get('name', 'unknown')}: {e}")

    def _monitor_simulation(self, simulation_start, end_time):
        """
        Monitorea la simulación y muestra el estado periódicamente.
        
        OPTIMIZADO: Reportes cada minuto (vs 2 minutos original)
        """
        last_status_time = 0
        
        while time.time() < end_time and self.is_running:
            current_time = time.time()
            
            # ⏱️ OPTIMIZADO: Reportar cada 60s vs 120s original
            if current_time - last_status_time > 60:
                elapsed = (current_time - simulation_start) / 60
                remaining = (end_time - current_time) / 60
                logger.info(f"📊 Simulación - ⏱️ Transcurrido: {elapsed:.1f}m, Restante: {remaining:.1f}m")
                self._log_basic_metrics()
                last_status_time = current_time
            
            time.sleep(5)  # Verificar cada 5 segundos

    def _log_basic_metrics(self):
        """
        Muestra métricas básicas y alertas activas.
        
        MÉTRICAS MOSTRADAS:
        - Número de alertas activas
        - Estado general del sistema
        - Servicios saludables vs total
        """
        if self.monitoring:
            dashboard = self.monitoring.get_dashboard_data()
            active_alerts = len(dashboard.get("alerts", []))
            
            if active_alerts > 0:
                logger.warning(f"⚠️ Alertas activas: {active_alerts}")
            
            # Mostrar estado de servicios
            services_data = dashboard.get("service_metrics", {})
            healthy_services = sum(1 for s in services_data.values() if s.get("availability", 0) > 90)
            total_services = len(services_data)
            
            if total_services > 0:
                logger.info(f"🏥 Servicios saludables: {healthy_services}/{total_services}")
    
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
