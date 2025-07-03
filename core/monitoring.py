"""
Sistema de monitoreo para el simulador de Chaos Engineering.
Recolecta métricas, genera alertas y proporciona dashboards en tiempo real.
"""

import time
import threading
import json
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from collections import deque, defaultdict
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class Alert:
    """Representa una alerta del sistema"""
    id: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    service_name: str
    instance_id: Optional[str]
    metric_name: str
    current_value: float
    threshold: float
    message: str
    timestamp: float
    resolved: bool = False
    resolved_timestamp: Optional[float] = None

@dataclass
class MetricPoint:
    """Punto de datos de una métrica"""
    timestamp: float
    value: float
    tags: Optional[Dict[str, str]] = None

class MetricCollector:
    """Recolector de métricas con almacenamiento temporal"""
    
    def __init__(self, max_points: int = 1000):
        self.max_points = max_points
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_points))
        self.lock = threading.RLock()
    
    def add_metric(self, metric_name: str, value: float, tags: Dict[str, str] = None):
        """Añade un punto de métrica"""
        with self.lock:
            point = MetricPoint(
                timestamp=time.time(),
                value=value,
                tags=tags or {}
            )
            self.metrics[metric_name].append(point)
    
    def get_metrics(self, metric_name: str, time_window_seconds: int = 300) -> List[MetricPoint]:
        """Obtiene métricas dentro de una ventana de tiempo"""
        with self.lock:
            if metric_name not in self.metrics:
                return []
            
            cutoff_time = time.time() - time_window_seconds
            return [
                point for point in self.metrics[metric_name]
                if point.timestamp >= cutoff_time
            ]
    
    def get_latest_value(self, metric_name: str) -> Optional[float]:
        """Obtiene el último valor de una métrica"""
        with self.lock:
            if metric_name not in self.metrics or not self.metrics[metric_name]:
                return None
            return self.metrics[metric_name][-1].value
    
    def calculate_average(self, metric_name: str, time_window_seconds: int = 300) -> Optional[float]:
        """Calcula el promedio de una métrica en una ventana de tiempo"""
        points = self.get_metrics(metric_name, time_window_seconds)
        if not points:
            return None
        
        return sum(point.value for point in points) / len(points)

class AlertManager:
    """Gestor de alertas del sistema"""
    
    def __init__(self):
        self.alerts: Dict[str, Alert] = {}
        self.alert_rules: List[Dict] = []
        self.alert_callbacks: List[Callable] = []
        self.lock = threading.RLock()
        
        # Configurar reglas de alerta por defecto
        self._setup_default_alert_rules()
    
    def _setup_default_alert_rules(self):
        """Configura las reglas de alerta por defecto"""
        default_rules = [
            {
                "name": "high_response_time",
                "metric": "response_time_ms",
                "threshold": 1000,
                "operator": ">",
                "severity": "HIGH",
                "message": "Tiempo de respuesta alto detectado"
            },
            {
                "name": "high_error_rate",
                "metric": "error_rate",
                "threshold": 5,
                "operator": ">",
                "severity": "CRITICAL",
                "message": "Tasa de errores alta detectada"
            },
            {
                "name": "low_availability",
                "metric": "availability",
                "threshold": 90,
                "operator": "<",
                "severity": "HIGH",
                "message": "Disponibilidad baja detectada"
            },
            {
                "name": "high_cpu_usage",
                "metric": "cpu_usage",
                "threshold": 85,
                "operator": ">",
                "severity": "MEDIUM",
                "message": "Uso alto de CPU detectado"
            },
            {
                "name": "high_memory_usage",
                "metric": "memory_usage",
                "threshold": 85,
                "operator": ">",
                "severity": "MEDIUM",
                "message": "Uso alto de memoria detectado"
            }
        ]
        
        self.alert_rules.extend(default_rules)
    
    def add_alert_rule(self, rule: Dict):
        """Añade una nueva regla de alerta"""
        required_fields = ["name", "metric", "threshold", "operator", "severity", "message"]
        if not all(field in rule for field in required_fields):
            raise ValueError(f"Regla de alerta debe contener: {required_fields}")
        
        self.alert_rules.append(rule)
        logger.info(f"Regla de alerta añadida: {rule['name']}")
    
    def check_metric(self, metric_name: str, value: float, service_name: str, instance_id: str = None):
        """Verifica si una métrica activa alguna alerta"""
        for rule in self.alert_rules:
            if rule["metric"] == metric_name:
                should_alert = self._evaluate_rule(rule, value)
                
                alert_id = f"{service_name}:{instance_id or 'service'}:{rule['name']}"
                
                if should_alert and alert_id not in self.alerts:
                    # Crear nueva alerta
                    alert = Alert(
                        id=alert_id,
                        severity=rule["severity"],
                        service_name=service_name,
                        instance_id=instance_id,
                        metric_name=metric_name,
                        current_value=value,
                        threshold=rule["threshold"],
                        message=f"{rule['message']}: {value} {rule['operator']} {rule['threshold']}",
                        timestamp=time.time()
                    )
                    
                    self.alerts[alert_id] = alert
                    self._trigger_alert(alert)
                
                elif not should_alert and alert_id in self.alerts:
                    # Resolver alerta existente
                    alert = self.alerts[alert_id]
                    if not alert.resolved:
                        alert.resolved = True
                        alert.resolved_timestamp = time.time()
                        self._resolve_alert(alert)
    
    def _evaluate_rule(self, rule: Dict, value: float) -> bool:
        """Evalúa si una regla se activa con el valor dado"""
        operator = rule["operator"]
        threshold = rule["threshold"]
        
        if operator == ">":
            return value > threshold
        elif operator == "<":
            return value < threshold
        elif operator == ">=":
            return value >= threshold
        elif operator == "<=":
            return value <= threshold
        elif operator == "==":
            return value == threshold
        elif operator == "!=":
            return value != threshold
        
        return False
    
    def _trigger_alert(self, alert: Alert):
        """Dispara una alerta nueva"""
        logger.warning(f"🚨 ALERTA {alert.severity}: {alert.message}")
        
        # Llamar callbacks registrados
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error en callback de alerta: {e}")
    
    def _resolve_alert(self, alert: Alert):
        """Resuelve una alerta"""
        duration = alert.resolved_timestamp - alert.timestamp
        logger.info(f"✅ ALERTA RESUELTA: {alert.message} (duración: {duration:.1f}s)")
    
    def get_active_alerts(self) -> List[Alert]:
        """Retorna todas las alertas activas"""
        return [alert for alert in self.alerts.values() if not alert.resolved]
    
    def get_alert_history(self, hours: int = 24) -> List[Alert]:
        """Retorna el historial de alertas"""
        cutoff_time = time.time() - (hours * 3600)
        return [
            alert for alert in self.alerts.values()
            if alert.timestamp >= cutoff_time
        ]
    
    def add_alert_callback(self, callback: Callable[[Alert], None]):
        """Añade un callback que se ejecuta cuando se dispara una alerta"""
        self.alert_callbacks.append(callback)

class MonitoringSystem:
    """Sistema principal de monitoreo"""
    
    def __init__(self, collection_interval: int = 5):
        self.collection_interval = collection_interval
        self.metric_collector = MetricCollector()
        self.alert_manager = AlertManager()
        self.monitored_components = {}
        self.is_running = False
        
        # Threading
        self.collection_thread = None
        self.lock = threading.RLock()
        
        # Dashboard data
        self.dashboard_data = {
            "last_update": time.time(),
            "system_overview": {},
            "service_metrics": {},
            "alerts": []
        }
        
        logger.info("Sistema de monitoreo inicializado")
    
    def register_component(self, name: str, component):
        """Registra un componente para monitoreo"""
        with self.lock:
            self.monitored_components[name] = component
            logger.info(f"Componente {name} registrado para monitoreo")
    
    def start_monitoring(self):
        """Inicia el monitoreo automático"""
        if self.is_running:
            logger.warning("El monitoreo ya está en ejecución")
            return
        
        self.is_running = True
        self.collection_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.collection_thread.start()
        logger.info("Monitoreo iniciado")
    
    def stop_monitoring(self):
        """Detiene el monitoreo"""
        self.is_running = False
        if self.collection_thread:
            self.collection_thread.join(timeout=5)
        logger.info("Monitoreo detenido")
    
    def _monitoring_loop(self):
        """Loop principal de recolección de métricas"""
        while self.is_running:
            try:
                self._collect_all_metrics()
                self._update_dashboard_data()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error en loop de monitoreo: {e}")
                time.sleep(1)
    
    def _collect_all_metrics(self):
        """Recolecta métricas de todos los componentes registrados"""
        with self.lock:
            for component_name, component in self.monitored_components.items():
                try:
                    if hasattr(component, 'get_service_metrics'):
                        # Es un servicio
                        metrics = component.get_service_metrics()
                        self._process_service_metrics(component_name, metrics)
                    
                    elif hasattr(component, 'get_load_balancer_metrics'):
                        # Es un load balancer
                        metrics = component.get_load_balancer_metrics()
                        self._process_load_balancer_metrics(component_name, metrics)
                    
                    elif hasattr(component, 'get_metrics'):
                        # Componente genérico con métricas
                        metrics = component.get_metrics()
                        self._process_generic_metrics(component_name, metrics)
                
                except Exception as e:
                    logger.error(f"Error recolectando métricas de {component_name}: {e}")
    
    def _process_service_metrics(self, service_name: str, metrics: Dict):
        """Procesa métricas de un servicio"""
        # Métricas del servicio
        self.metric_collector.add_metric(
            f"{service_name}.availability",
            metrics["availability"],
            {"service": service_name}
        )
        
        self.metric_collector.add_metric(
            f"{service_name}.response_time_ms",
            metrics["avg_response_time_ms"],
            {"service": service_name}
        )
        
        self.metric_collector.add_metric(
            f"{service_name}.error_rate",
            metrics["error_rate"],
            {"service": service_name}
        )
        
        # Verificar alertas
        self.alert_manager.check_metric("availability", metrics["availability"], service_name)
        self.alert_manager.check_metric("response_time_ms", metrics["avg_response_time_ms"], service_name)
        self.alert_manager.check_metric("error_rate", metrics["error_rate"], service_name)
        
        # Métricas de instancias
        for instance_id, instance_data in metrics.get("instances", {}).items():
            instance_metrics = instance_data["metrics"]
            
            self.metric_collector.add_metric(
                f"{service_name}.instance.cpu_usage",
                instance_metrics["cpu_usage"],
                {"service": service_name, "instance": instance_id}
            )
            
            self.metric_collector.add_metric(
                f"{service_name}.instance.memory_usage",
                instance_metrics["memory_usage"],
                {"service": service_name, "instance": instance_id}
            )
            
            # Verificar alertas de instancia
            self.alert_manager.check_metric("cpu_usage", instance_metrics["cpu_usage"], 
                                           service_name, instance_id)
            self.alert_manager.check_metric("memory_usage", instance_metrics["memory_usage"], 
                                           service_name, instance_id)
    
    def _process_load_balancer_metrics(self, lb_name: str, metrics: Dict):
        """Procesa métricas de un load balancer"""
        traffic_metrics = metrics["traffic_metrics"]
        
        self.metric_collector.add_metric(
            f"{lb_name}.requests_per_second",
            traffic_metrics["requests_per_second"],
            {"load_balancer": lb_name}
        )
        
        self.metric_collector.add_metric(
            f"{lb_name}.avg_response_time_ms",
            traffic_metrics["avg_response_time_ms"],
            {"load_balancer": lb_name}
        )
        
        self.metric_collector.add_metric(
            f"{lb_name}.error_rate",
            traffic_metrics["error_rate"],
            {"load_balancer": lb_name}
        )
    
    def _process_generic_metrics(self, component_name: str, metrics: Dict):
        """Procesa métricas genéricas"""
        for metric_name, value in metrics.items():
            if isinstance(value, (int, float)):
                self.metric_collector.add_metric(
                    f"{component_name}.{metric_name}",
                    value,
                    {"component": component_name}
                )
    
    def _update_dashboard_data(self):
        """Actualiza los datos del dashboard"""
        with self.lock:
            self.dashboard_data = {
                "last_update": time.time(),
                "system_overview": self._generate_system_overview(),
                "service_metrics": self._generate_service_metrics(),
                "alerts": [asdict(alert) for alert in self.alert_manager.get_active_alerts()]
            }
    
    def _generate_system_overview(self) -> Dict:
        """Genera un overview del sistema"""
        overview = {
            "total_services": len([name for name in self.monitored_components.keys() 
                                 if hasattr(self.monitored_components[name], 'get_service_metrics')]),
            "total_alerts": len(self.alert_manager.get_active_alerts()),
            "critical_alerts": len([a for a in self.alert_manager.get_active_alerts() 
                                  if a.severity == "CRITICAL"]),
            "system_health": "HEALTHY"
        }
        
        # Determinar salud del sistema
        critical_alerts = overview["critical_alerts"]
        total_alerts = overview["total_alerts"]
        
        if critical_alerts > 0:
            overview["system_health"] = "CRITICAL"
        elif total_alerts > 5:
            overview["system_health"] = "DEGRADED"
        elif total_alerts > 0:
            overview["system_health"] = "WARNING"
        
        return overview
    
    def _generate_service_metrics(self) -> Dict:
        """Genera métricas agregadas por servicio"""
        service_metrics = {}
        
        for component_name, component in self.monitored_components.items():
            if hasattr(component, 'get_service_metrics'):
                try:
                    metrics = component.get_service_metrics()
                    service_metrics[component_name] = {
                        "availability": metrics["availability"],
                        "response_time": metrics["avg_response_time_ms"],
                        "error_rate": metrics["error_rate"],
                        "total_instances": metrics["total_instances"],
                        "healthy_instances": metrics["healthy_instances"]
                    }
                except Exception as e:
                    logger.error(f"Error generando métricas para {component_name}: {e}")
        
        return service_metrics
    
    def get_dashboard_data(self) -> Dict:
        """Retorna los datos actuales del dashboard"""
        with self.lock:
            return self.dashboard_data.copy()
    
    def get_metric_history(self, metric_name: str, time_window_seconds: int = 300) -> List[Dict]:
        """Retorna el historial de una métrica"""
        points = self.metric_collector.get_metrics(metric_name, time_window_seconds)
        return [
            {
                "timestamp": point.timestamp,
                "value": point.value,
                "tags": point.tags
            }
            for point in points
        ]
    
    def get_alerts(self, active_only: bool = True) -> List[Dict]:
        """Retorna las alertas"""
        if active_only:
            alerts = self.alert_manager.get_active_alerts()
        else:
            alerts = self.alert_manager.get_alert_history()
        
        return [asdict(alert) for alert in alerts]
    
    def generate_health_report(self) -> Dict:
        """Genera un reporte de salud del sistema"""
        report = {
            "timestamp": time.time(),
            "system_overview": self._generate_system_overview(),
            "service_health": self._get_service_health(),
            "alert_summary": self._get_alert_summary(),
            "performance_summary": self._get_performance_summary()
        }
        return report

    def _get_alert_summary(self) -> Dict:
        """Obtiene el resumen de alertas"""
        active_alerts = self.alert_manager.get_active_alerts()
        alerts_by_severity = {}
        for alert in active_alerts:
            severity = alert.severity
            alerts_by_severity[severity] = alerts_by_severity.get(severity, 0) + 1
        return {
            "active_alerts": len(active_alerts),
            "alerts_by_severity": alerts_by_severity,
            "recent_alerts": len(self.alert_manager.get_alert_history(hours=1))
        }

    def _get_service_health(self) -> Dict:
        """Obtiene la salud de cada servicio"""
        service_health = {}
        for component_name, component in self.monitored_components.items():
            if hasattr(component, 'get_service_metrics'):
                try:
                    metrics = component.get_service_metrics()
                    if metrics["availability"] > 90:
                        status = "HEALTHY"
                    elif metrics["availability"] > 50:
                        status = "DEGRADED"
                    else:
                        status = "CRITICAL"
                    service_health[component_name] = {
                        "status": status,
                        "availability": metrics["availability"],
                        "instances": f"{metrics['healthy_instances']}/{metrics['total_instances']}"
                    }
                except Exception as e:
                    service_health[component_name] = {
                        "status": "UNKNOWN",
                        "error": str(e)
                    }
        return service_health

    def _get_performance_summary(self) -> Dict:
        """Obtiene el resumen de performance"""
        avg_response_times = []
        error_rates = []
        service_health = self._get_service_health()
        for service_name in service_health.keys():
            rt_metric = f"{service_name}.response_time_ms"
            er_metric = f"{service_name}.error_rate"
            rt = self.metric_collector.get_latest_value(rt_metric)
            er = self.metric_collector.get_latest_value(er_metric)
            if rt is not None:
                avg_response_times.append(rt)
            if er is not None:
                error_rates.append(er)
        summary = {}
        if avg_response_times:
            summary["avg_response_time_ms"] = sum(avg_response_times) / len(avg_response_times)
        if error_rates:
            summary["avg_error_rate"] = sum(error_rates) / len(error_rates)
        return summary
    
    def export_metrics(self, output_file: str, time_window_seconds: int = 3600):
        """Exporta métricas a un archivo JSON"""
        export_data = {
            "export_timestamp": time.time(),
            "time_window_seconds": time_window_seconds,
            "metrics": {}
        }
        
        # Exportar todas las métricas
        for metric_name in self.metric_collector.metrics.keys():
            points = self.metric_collector.get_metrics(metric_name, time_window_seconds)
            export_data["metrics"][metric_name] = [
                {
                    "timestamp": point.timestamp,
                    "value": point.value,
                    "tags": point.tags
                }
                for point in points
            ]
        
        # Exportar alertas
        export_data["alerts"] = [
            asdict(alert) for alert in self.alert_manager.get_alert_history(hours=24)
        ]
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Métricas exportadas a {output_file}")
        except Exception as e:
            logger.error(f"Error exportando métricas: {e}")
    
    def add_custom_alert_callback(self, callback: Callable[[Alert], None]):
        """Añade un callback personalizado para alertas"""
        self.alert_manager.add_alert_callback(callback)
    
    def get_system_status(self) -> str:
        """Retorna el estado general del sistema"""
        active_alerts = self.alert_manager.get_active_alerts()
        critical_alerts = [a for a in active_alerts if a.severity == "CRITICAL"]
        
        if critical_alerts:
            return "CRITICAL"
        elif len(active_alerts) > 5:
            return "DEGRADED"
        elif active_alerts:
            return "WARNING"
        else:
            return "HEALTHY"
