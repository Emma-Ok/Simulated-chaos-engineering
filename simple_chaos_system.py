#!/usr/bin/env python3
"""
Sistema Principal de Chaos Engineering - Versión Simplificada y Centralizada.
Este módulo unifica toda la funcionalidad del sistema en una interfaz simple.
"""

import time
import threading
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Importaciones de componentes core
from core.service import Service, ServiceType
from core.load_balancer import LoadBalancer, LoadBalancingStrategy
from core.monitoring import MonitoringSystem

# Importaciones del nuevo sistema de experimentos centralizado
from chaos_experiments_core import (
    ChaosExperimentManager, ExperimentConfig, ExperimentType,
    create_latency_experiment, create_termination_experiment,
    create_resource_experiment, create_health_check_experiment
)

# Utilidades
from utils.helpers import setup_logging, format_timestamp, format_duration
from utils.reports import ReportGenerator

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# CONFIGURACIÓN SIMPLIFICADA DEL SISTEMA
# ═══════════════════════════════════════════════════════════════════

@dataclass
class SystemConfig:
    """Configuración simplificada del sistema."""
    # Configuración de servicios
    services: Dict[str, Dict[str, Any]] = None
    
    # Configuración de monitoreo
    monitoring_interval_seconds: int = 5
    
    # Configuración de experimentos
    max_concurrent_experiments: int = 3
    safety_checks_enabled: bool = True
    
    # Configuración de reportes
    reports_enabled: bool = True
    reports_directory: str = "./reports"
    
    def __post_init__(self):
        if self.services is None:
            self.services = {
                "api-service": {"type": "api-gateway", "instances": 3, "min_instances": 1},
                "auth-service": {"type": "auth-service", "instances": 2, "min_instances": 1},
                "db-service": {"type": "database", "instances": 2, "min_instances": 1},
                "cache-service": {"type": "cache", "instances": 2, "min_instances": 1}
            }

# ═══════════════════════════════════════════════════════════════════
# SISTEMA PRINCIPAL SIMPLIFICADO
# ═══════════════════════════════════════════════════════════════════

class SimpleChaosSystem:
    """
    Sistema principal simplificado de Chaos Engineering.
    
    Características:
    - Interfaz unificada y simple
    - Gestión automática de servicios
    - Experimentos centralizados
    - Monitoreo integrado
    - Reportes automáticos
    """
    
    def __init__(self, config: SystemConfig = None):
        self.config = config or SystemConfig()
        
        # Componentes principales
        self.services: Dict[str, Service] = {}
        self.load_balancer: Optional[LoadBalancer] = None
        self.monitoring: Optional[MonitoringSystem] = None
        self.experiment_manager: Optional[ChaosExperimentManager] = None
        self.report_generator: Optional[ReportGenerator] = None
        
        # Estado del sistema
        self.is_running = False
        self.start_time = None
        self.lock = threading.RLock()
        
        logger.info("🔥 SimpleChaosSystem inicializado")
    
    def initialize(self):
        """Inicializa todos los componentes del sistema."""
        logger.info("🚀 Inicializando sistema de Chaos Engineering...")
        
        try:
            self._create_services()
            self._create_load_balancer()
            self._create_monitoring()
            self._create_experiment_manager()
            self._create_report_generator()
            
            logger.info("✅ Sistema inicializado correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error inicializando sistema: {e}")
            raise
    
    def _create_services(self):
        """Crea los servicios configurados."""
        logger.info("🏗️ Creando servicios...")
        
        for service_name, service_config in self.config.services.items():
            service_type = self._get_service_type(service_config["type"])
            instances = service_config.get("instances", 2)
            min_instances = service_config.get("min_instances", 1)
            
            service = Service(
                name=service_name,
                service_type=service_type,
                initial_instances=instances
            )
            service.min_instances = min_instances
            
            self.services[service_name] = service
            logger.info(f"   ✓ {service_name}: {instances} instancias")
    
    def _get_service_type(self, type_string: str) -> ServiceType:
        """Convierte string a ServiceType."""
        type_mapping = {
            "api-gateway": ServiceType.API_GATEWAY,
            "auth-service": ServiceType.AUTH_SERVICE,
            "database": ServiceType.DATABASE,
            "cache": ServiceType.CACHE,
            "user-profile": ServiceType.USER_PROFILE,
            "payment": ServiceType.PAYMENT,
            "notification": ServiceType.NOTIFICATION
        }
        return type_mapping.get(type_string, ServiceType.API_GATEWAY)
    
    def _create_load_balancer(self):
        """Crea el balanceador de carga."""
        self.load_balancer = LoadBalancer("main-lb", LoadBalancingStrategy.ROUND_ROBIN)
        
        # Registrar servicios
        for service in self.services.values():
            self.load_balancer.register_service(service)
        
        logger.info("⚖️ Load Balancer creado")
    
    def _create_monitoring(self):
        """Crea el sistema de monitoreo."""
        self.monitoring = MonitoringSystem(self.config.monitoring_interval_seconds)
        
        # Registrar componentes para monitoreo
        if self.load_balancer:
            self.monitoring.register_component("load_balancer", self.load_balancer)
        
        for service_name, service in self.services.items():
            self.monitoring.register_component(service_name, service)
        
        logger.info("📊 Sistema de monitoreo creado")
    
    def _create_experiment_manager(self):
        """Crea el gestor de experimentos."""
        self.experiment_manager = ChaosExperimentManager(self.services)
        self.experiment_manager.max_concurrent_experiments = self.config.max_concurrent_experiments
        self.experiment_manager.safety_checks_enabled = self.config.safety_checks_enabled
        
        logger.info("🧪 Gestor de experimentos creado")
    
    def _create_report_generator(self):
        """Crea el generador de reportes."""
        if self.config.reports_enabled:
            self.report_generator = ReportGenerator(self.config.reports_directory)
            logger.info("📋 Generador de reportes creado")
    
    def start(self):
        """Inicia el sistema completo."""
        if self.is_running:
            logger.warning("Sistema ya está ejecutándose")
            return
        
        logger.info("🚀 Iniciando sistema...")
        
        with self.lock:
            self.is_running = True
            self.start_time = time.time()
        
        # Iniciar monitoreo
        if self.monitoring:
            self.monitoring.start_monitoring()
        
        # Iniciar simulación de tráfico ligero
        if self.load_balancer:
            self.load_balancer.simulate_traffic(requests_per_second=20, duration_seconds=None)
        
        logger.info("✅ Sistema iniciado correctamente")
    
    def stop(self):
        """Detiene el sistema completo."""
        logger.info("🛑 Deteniendo sistema...")
        
        with self.lock:
            self.is_running = False
        
        # Detener experimentos
        if self.experiment_manager:
            self.experiment_manager.stop_all_experiments()
        
        # Detener monitoreo
        if self.monitoring:
            self.monitoring.stop_monitoring()
        
        # Detener load balancer (cerrar servicios)
        if self.load_balancer:
            # El load balancer no tiene método stop, simplemente limpiar
            pass
        
        # Cerrar servicios directamente
        for service in self.services.values():
            if hasattr(service, 'stop'):
                service.stop()
        
        logger.info("✅ Sistema detenido")
    
    # ═══════════════════════════════════════════════════════════════════
    # MÉTODOS PARA EXPERIMENTOS
    # ═══════════════════════════════════════════════════════════════════
    
    def run_latency_experiment(self, target_service: str, latency_ms: int = 500, 
                              duration_seconds: int = 120) -> str:
        """Ejecuta un experimento de latencia."""
        if not self.experiment_manager:
            raise RuntimeError("Sistema no inicializado")
        
        config = create_latency_experiment(
            name=f"latency-{target_service}",
            target_service=target_service,
            latency_ms=latency_ms,
            duration_seconds=duration_seconds
        )
        
        return self.experiment_manager.create_and_run_experiment(config)
    
    def run_termination_experiment(self, target_service: str = None) -> str:
        """Ejecuta un experimento de terminación de instancias."""
        if not self.experiment_manager:
            raise RuntimeError("Sistema no inicializado")
        
        config = create_termination_experiment(
            name=f"termination-{target_service or 'random'}",
            target_service=target_service
        )
        
        return self.experiment_manager.create_and_run_experiment(config)
    
    def run_resource_experiment(self, target_service: str, resource_type: str = 'cpu',
                               exhaustion_level: float = 0.8, duration_seconds: int = 120) -> str:
        """Ejecuta un experimento de agotamiento de recursos."""
        if not self.experiment_manager:
            raise RuntimeError("Sistema no inicializado")
        
        config = create_resource_experiment(
            name=f"resource-{target_service}-{resource_type}",
            target_service=target_service,
            resource_type=resource_type,
            exhaustion_level=exhaustion_level,
            duration_seconds=duration_seconds
        )
        
        return self.experiment_manager.create_and_run_experiment(config)
    
    def run_health_check(self, duration_seconds: int = 60) -> str:
        """Ejecuta un diagnóstico completo del sistema."""
        if not self.experiment_manager:
            raise RuntimeError("Sistema no inicializado")
        
        config = create_health_check_experiment(
            name="system-health-check",
            duration_seconds=duration_seconds
        )
        
        return self.experiment_manager.create_and_run_experiment(config)
    
    def stop_experiment(self, experiment_id: str) -> bool:
        """Detiene un experimento específico."""
        if not self.experiment_manager:
            return False
        return self.experiment_manager.stop_experiment(experiment_id)
    
    def get_experiment_status(self, experiment_id: str) -> Optional[Dict]:
        """Obtiene el estado de un experimento."""
        if not self.experiment_manager:
            return None
        return self.experiment_manager.get_experiment_status(experiment_id)
    
    # ═══════════════════════════════════════════════════════════════════
    # MÉTODOS DE ESTADO Y REPORTES
    # ═══════════════════════════════════════════════════════════════════
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el estado completo del sistema."""
        with self.lock:
            uptime = time.time() - self.start_time if self.start_time else 0
            
            # Estado de servicios
            services_status = {}
            for service_name, service in self.services.items():
                healthy_instances = service.get_healthy_instances()
                total_instances = list(service.instances.values())
                
                services_status[service_name] = {
                    'total_instances': len(total_instances),
                    'healthy_instances': len(healthy_instances),
                    'availability': (len(healthy_instances) / len(total_instances)) * 100 if total_instances else 0,
                    'avg_response_time_ms': sum(i.base_response_time for i in healthy_instances) / len(healthy_instances) if healthy_instances else 0,
                    'error_rate': sum(i.error_probability for i in total_instances) / len(total_instances) if total_instances else 0
                }
            
            # Estado de experimentos
            experiments_status = {}
            if self.experiment_manager:
                experiments_status = self.experiment_manager.get_system_summary()
            
            # Estado de monitoreo
            monitoring_status = {}
            if self.monitoring:
                alerts = self.monitoring.alert_manager.get_active_alerts()
                monitoring_status = {
                    'active_alerts': len(alerts),
                    'alerts': [{'metric': a.metric_name, 'severity': a.severity} for a in alerts[:5]]
                }
            
            return {
                'system_running': self.is_running,
                'uptime_seconds': uptime,
                'uptime_formatted': format_duration(uptime),
                'services': services_status,
                'experiments': experiments_status,
                'monitoring': monitoring_status,
                'timestamp': format_timestamp()
            }
    
    def generate_report(self, include_charts: bool = True) -> Optional[str]:
        """Genera un reporte del sistema."""
        if not self.report_generator:
            logger.warning("Generador de reportes no disponible")
            return None
        
        try:
            # Obtener datos para el reporte
            system_status = self.get_system_status()
            
            # Generar reporte
            report_path = self.report_generator.generate_comprehensive_report(
                chaos_system=self,
                include_charts=include_charts,
                formats=["html"]
            )
            
            logger.info(f"📋 Reporte generado: {report_path}")
            return report_path.get("html") if isinstance(report_path, dict) else report_path
            
        except Exception as e:
            logger.error(f"Error generando reporte: {e}")
            return None
    
    # ═══════════════════════════════════════════════════════════════════
    # DEMOSTRACIONES PREDEFINIDAS
    # ═══════════════════════════════════════════════════════════════════
    
    def run_basic_demo(self, duration_minutes: int = 3):
        """
        Ejecuta una demostración básica de chaos engineering.
        
        Args:
            duration_minutes: Duración total de la demo (máximo 4 minutos)
        """
        if duration_minutes > 4:
            logger.warning("Duración máxima recomendada: 4 minutos")
            duration_minutes = 4
        
        logger.info(f"🎮 Iniciando demostración básica de {duration_minutes} minutos")
        
        try:
            # Mostrar estado inicial
            print("\n" + "="*60)
            print("🔥 DEMOSTRACIÓN DE CHAOS ENGINEERING")
            print("="*60)
            self._show_system_status()
            
            # Programa de experimentos basado en duración
            experiments_schedule = []
            
            # Experimento 1: Health check inicial (siempre se ejecuta)
            experiments_schedule.append({
                'delay': 10,
                'action': lambda: self.run_health_check(30),
                'description': "Diagnóstico inicial del sistema"
            })
            
            # Experimento 2: Latencia (si hay tiempo)
            if duration_minutes >= 2:
                experiments_schedule.append({
                    'delay': 60,
                    'action': lambda: self.run_latency_experiment("api-service", 400, 60),
                    'description': "Experimento de latencia en API"
                })
            
            # Experimento 3: Terminación (si hay tiempo)
            if duration_minutes >= 3:
                experiments_schedule.append({
                    'delay': 120,
                    'action': lambda: self.run_termination_experiment("auth-service"),
                    'description': "Terminación de instancia"
                })
            
            # Ejecutar experimentos programados
            demo_end_time = time.time() + (duration_minutes * 60)
            
            for experiment in experiments_schedule:
                # Programar experimento
                def run_scheduled_experiment(exp_info):
                    time.sleep(exp_info['delay'])
                    if time.time() < demo_end_time:
                        try:
                            print(f"\n🧪 {exp_info['description']}...")
                            exp_id = exp_info['action']()
                            print(f"   Experimento iniciado: {exp_id}")
                        except Exception as e:
                            print(f"   Error: {e}")
                
                exp_thread = threading.Thread(
                    target=run_scheduled_experiment, 
                    args=(experiment,), 
                    daemon=True
                )
                exp_thread.start()
            
            # Monitorear progreso
            start_time = time.time()
            last_status_time = 0
            
            while time.time() < demo_end_time:
                current_time = time.time() - start_time
                
                # Mostrar estado cada minuto
                if current_time - last_status_time >= 60:
                    remaining = (demo_end_time - time.time()) / 60
                    print(f"\n⏱️ Tiempo transcurrido: {current_time/60:.1f}m, Restante: {remaining:.1f}m")
                    self._show_experiment_summary()
                    last_status_time = current_time
                
                time.sleep(10)
            
            # Resumen final
            print("\n" + "="*60)
            print("📊 RESUMEN FINAL DE LA DEMOSTRACIÓN")
            print("="*60)
            self._show_system_status()
            self._show_experiment_summary()
            
            # Generar reporte
            report_path = self.generate_report()
            if report_path:
                print(f"📋 Reporte generado: {report_path}")
            
            print("\n✅ Demostración completada exitosamente")
            
        except Exception as e:
            logger.error(f"Error en demostración: {e}")
            raise
    
    def _show_system_status(self):
        """Muestra el estado actual del sistema."""
        status = self.get_system_status()
        
        print(f"\n📊 Estado del Sistema:")
        print(f"   🔄 Sistema activo: {'Sí' if status['system_running'] else 'No'}")
        print(f"   ⏱️ Tiempo activo: {status['uptime_formatted']}")
        print(f"   🔧 Servicios: {len(status['services'])}")
        
        for service_name, service_data in status['services'].items():
            instances = f"{service_data['healthy_instances']}/{service_data['total_instances']}"
            availability = service_data['availability']
            print(f"      • {service_name}: {instances} instancias, {availability:.1f}% disponible")
    
    def _show_experiment_summary(self):
        """Muestra un resumen de los experimentos."""
        if not self.experiment_manager:
            return
        
        summary = self.experiment_manager.get_system_summary()
        print(f"\n🧪 Experimentos:")
        print(f"   🔬 Activos: {summary['active_experiments']}")
        print(f"   ✅ Completados: {summary['completed_experiments']}")
        print(f"   📈 Tasa de éxito: {summary['success_rate']:.1f}%")
    
    # ═══════════════════════════════════════════════════════════════════
    # CONTEXT MANAGER SUPPORT
    # ═══════════════════════════════════════════════════════════════════
    
    def __enter__(self):
        """Soporte para context manager."""
        self.initialize()
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Soporte para context manager."""
        self.stop()

# ═══════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL PARA DEMOSTRACIONES RÁPIDAS
# ═══════════════════════════════════════════════════════════════════

def run_quick_demo(duration_minutes: int = 3):
    """
    Función de conveniencia para ejecutar una demostración rápida.
    
    Args:
        duration_minutes: Duración de la demo (1-4 minutos)
    """
    # Configurar logging
    setup_logging("INFO", colors=True)
    
    print("🔥 Iniciando sistema simplificado de Chaos Engineering...")
    
    # Crear y ejecutar demo
    with SimpleChaosSystem() as system:
        system.run_basic_demo(duration_minutes)

if __name__ == "__main__":
    # Demo por defecto de 3 minutos
    run_quick_demo(3)
