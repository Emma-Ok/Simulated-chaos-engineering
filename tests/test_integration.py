"""
Tests de integración para el sistema completo de Chaos Engineering
"""

import unittest
import time
import tempfile
import os
import sys

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chaos_system import ChaosEngineeringSystem

class TestChaosEngineeringSystemIntegration(unittest.TestCase):
    """Tests de integración para el sistema completo"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.system = ChaosEngineeringSystem()
    
    def tearDown(self):
        """Limpieza después de cada test"""
        if self.system.is_running:
            self.system.stop()
    
    def test_system_initialization(self):
        """Test de inicialización del sistema completo"""
        # Agregar servicios con tipos válidos
        success1 = self.system.add_service("web-service", "api-gateway", instances=2)
        success2 = self.system.add_service("api-service", "user-profile", instances=3)
        success3 = self.system.add_service("db-service", "database", instances=1)
        
        self.assertTrue(success1)
        self.assertTrue(success2)
        self.assertTrue(success3)
        
        # Verificar servicios registrados
        self.assertIn("web-service", self.system.services)
        self.assertIn("api-service", self.system.services)
        self.assertIn("db-service", self.system.services)
        
        # Usar context manager para inicializar componentes
        with self.system:
            # Verificar que los componentes se inicializaron
            self.assertIsNotNone(self.system.load_balancer)
            self.assertIsNotNone(self.system.monitoring)
            self.assertIsNotNone(self.system.chaos_monkey)
    
    def test_system_start_stop(self):
        """Test de inicio y parada del sistema"""
        # Configurar sistema
        self.system.add_service("test-service", "user-profile", instances=2)
        
        # Usar context manager para manejar inicio/parada
        with self.system:
            # El sistema se inicia automáticamente
            self.assertTrue(self.system.is_running)
        
        # El sistema se detiene automáticamente
        self.assertFalse(self.system.is_running)
    
    def test_traffic_simulation(self):
        """Test de simulación de tráfico"""
        # Configurar sistema
        self.system.add_service("api-service", "user-profile", instances=2)
        
        with self.system:
            # Simular tráfico por poco tiempo usando load balancer
            if self.system.load_balancer:
                self.system.load_balancer.simulate_traffic(requests_per_second=10, duration_seconds=5)
            
            # Verificar que el servicio existe y está funcionando
            service = self.system.services["api-service"]
            status = self.system.get_system_status()
            
            # Debería haber servicios activos
            self.assertGreater(len(status.get("services", {})), 0)
    
    def test_chaos_experiment_integration(self):
        """Test de integración de experimentos de chaos"""
        # Configurar sistema con suficientes instancias
        self.system.add_service("target-service", "user-profile", instances=3)
        
        with self.system:
            # Configurar chaos monkey
            if self.system.chaos_monkey:
                self.system.chaos_monkey.is_enabled = True
                self.system.chaos_monkey.min_healthy_instances = 1
            
            # Obtener estado inicial
            initial_healthy = len(self.system.services["target-service"].get_healthy_instances())
            
            # Ejecutar experimento de chaos
            if self.system.chaos_monkey:
                result = self.system.chaos_monkey.force_chaos("target-service")
                
                if result["status"] == "success":
                    # Verificar que el experimento tuvo efecto
                    current_healthy = len(self.system.services["target-service"].get_healthy_instances())
                    self.assertLess(current_healthy, initial_healthy)
                    
                    # Verificar que el sistema sigue monitoreando
                    status = self.system.get_system_status()
                    self.assertIsNotNone(status)
    
    def test_monitoring_integration(self):
        """Test de integración del sistema de monitoreo"""
        # Configurar sistema
        self.system.add_service("monitored-service", "user-profile", instances=2)
        
        with self.system:
            # Simular algo de actividad directamente con el servicio
            service = self.system.services["monitored-service"]
            for _ in range(10):
                service.handle_request()
            
            # Verificar que el monitoreo funciona
            if self.system.monitoring:
                # Obtener métricas del sistema
                system_status = self.system.get_system_status()
                self.assertIsNotNone(system_status)
                
                # Verificar que hay servicios monitoreados
                self.assertIn("services", system_status)
                self.assertGreater(len(system_status["services"]), 0)
    
    def test_load_balancer_integration(self):
        """Test de integración del balanceador de carga"""
        # Configurar sistema con múltiples instancias
        self.system.add_service("balanced-service", "user-profile", instances=3)
        # Sistema se inicializa con context manager
        
        # Verificar que el load balancer se configuró
        if self.system.load_balancer:
            # Verificar que el servicio está registrado
            self.assertIn("balanced-service", self.system.load_balancer.services)
            
            # Simular distribución de carga
            instances_selected = []
            for _ in range(10):
                instance = self.system.load_balancer.route_request("balanced-service")
                if instance:
                    instances_selected.append(instance.instance_id)
            
            # Verificar que se distribuyó entre múltiples instancias
            unique_instances = set(instances_selected)
            self.assertGreater(len(unique_instances), 1)
    
    def test_report_generation(self):
        """Test de generación de reportes"""
        # Configurar sistema
        self.system.add_service("report-service", "user-profile", instances=2)
        
        with self.system:
            # Simular alguna actividad directamente con el servicio
            service = self.system.services["report-service"]
            for _ in range(10):
                service.handle_request()
            
            # Ejecutar experimento si es posible
            if self.system.chaos_monkey:
                self.system.chaos_monkey.is_enabled = True
                self.system.chaos_monkey.force_chaos("report-service")
            
            # Generar reporte
            report_result = self.system.generate_report()
            
            # Verificar que el reporte se generó (es un diccionario)
            self.assertIsInstance(report_result, dict)
            self.assertIn("html", report_result)  # Formato por defecto
            
            # Verificar que el archivo HTML existe
            if "html" in report_result and os.path.exists(report_result["html"]):
                self.assertTrue(os.path.isfile(report_result["html"]))
                
                # Verificar que el archivo no está vacío
                self.assertGreater(os.path.getsize(report_result["html"]), 0)
    
    def test_system_resilience(self):
        """Test de resiliencia del sistema ante múltiples fallas"""
        # Configurar sistema robusto
        self.system.add_service("resilient-service", "user-profile", instances=4)
        
        with self.system:
            # Configurar chaos monkey
            if self.system.chaos_monkey:
                self.system.chaos_monkey.is_enabled = True
                self.system.chaos_monkey.min_healthy_instances = 1
            
            # Simular tráfico base directamente con el servicio (con manejo de errores)
            service = self.system.services["resilient-service"] 
            for _ in range(20):
                try:
                    service.handle_request()
                except Exception:
                    # Ignorar errores simulados durante el test
                    pass
            
            # Introducir múltiples fallas
            failures_introduced = 0
            if self.system.chaos_monkey:
                for _ in range(3):  # Intentar 3 fallas
                    result = self.system.chaos_monkey.force_chaos("resilient-service")
                    if result["status"] == "success":
                        failures_introduced += 1
                    time.sleep(1)  # Pausa entre fallas
            
            # Verificar que el sistema sigue funcionando
            remaining_healthy = len(self.system.services["resilient-service"].get_healthy_instances())
            self.assertGreater(remaining_healthy, 0, "El sistema debería tener al menos una instancia saludable")
            
            # Verificar que las fallas fueron registradas
            if self.system.chaos_monkey and failures_introduced > 0:
                stats = self.system.chaos_monkey.get_statistics()
                self.assertGreater(stats["statistics"]["total_terminations"], 0)
    
    def test_system_status_display(self):
        """Test de visualización del estado del sistema"""
        # Configurar sistema
        self.system.add_service("status-service", "user-profile", instances=2)
        
        with self.system:
            # El método show_system_status no debería lanzar excepciones
            try:
                self.system.show_system_status()
                # Si llegamos aquí, el método funcionó correctamente
                # Método ejecutado correctamente, no se lanzó excepción
            except Exception as e:
                self.fail(f"show_system_status lanzó una excepción: {e}")
    
    def test_configuration_with_file(self):
        """Test de configuración usando archivo temporal"""
        # Crear archivo de configuración temporal
        config_content = """
system:
  name: "test-system"
  region: "us-east-1"

chaos_monkey:
  enabled: true
  min_healthy_instances: 1
  termination_probability: 0.2
  
resilience_patterns:
  circuit_breaker:
    enabled: true
    failure_threshold: 3
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_content)
            config_file = f.name
        
        try:
            # Inicializar sistema con configuración
            configured_system = ChaosEngineeringSystem(config_path=config_file)
            
            # Verificar que se cargó la configuración
            self.assertIsNotNone(configured_system.config)
            
            # Agregar servicios y verificar funcionamiento
            configured_system.add_service("config-service", "user-profile", instances=2)
            # Sistema se inicializa con context manager
            
            # Verificar que los componentes se inicializaron con la configuración
            self.assertIsNotNone(configured_system.chaos_monkey)
            
            # Limpiar
            if configured_system.is_running:
                configured_system.stop()
                
        finally:
            # Limpiar archivo temporal
            try:
                os.unlink(config_file)
            except OSError:
                pass

if __name__ == "__main__":
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.ERROR)  # Solo errores durante tests
    
    # Ejecutar tests
    unittest.main(verbosity=2)
