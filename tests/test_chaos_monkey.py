"""
Tests unitarios pa        # Crear servicios mock para pruebas
        self.test_service = Service("test-service", ServiceType.API_GATEWAY, initial_instances=3)
        self.db_service = Service("database", ServiceType.DATABASE, initial_instances=2)el módulo chaos.chaos_monkey
"""

import unittest
import time
from unittest.mock import Mock, MagicMock
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chaos.chaos_monkey import ChaosMonkey
from core.service import Service, ServiceType

class TestChaosMonkey(unittest.TestCase):
    """Tests para la clase ChaosMonkey"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.chaos_monkey = ChaosMonkey("test-monkey")
        
        # Crear servicios mock para pruebas
        self.test_service = Service("test-service", ServiceType.API_GATEWAY, initial_instances=3)
        self.db_service = Service("database", ServiceType.DATABASE, initial_instances=2)
        
        # Registrar servicios
        self.chaos_monkey.register_service("test-service", self.test_service)
        self.chaos_monkey.register_service("database", self.db_service)
    
    def test_chaos_monkey_creation(self):
        """Test de creación del Chaos Monkey"""
        self.assertEqual(self.chaos_monkey.name, "test-monkey")
        self.assertFalse(self.chaos_monkey.is_enabled)
        self.assertFalse(self.chaos_monkey.is_running)
        self.assertEqual(self.chaos_monkey.min_healthy_instances, 1)
        self.assertEqual(self.chaos_monkey.termination_probability, 0.1)
    
    def test_configuration(self):
        """Test de configuración del Chaos Monkey"""
        config = {
            "enabled": True,
            "targets": {
                "min_healthy_instances": 2,
                "max_instances_to_kill": 2,
                "excluded_services": ["database"]
            },
            "schedule": {
                "days": ["monday", "tuesday"],
                "hours": {"start": 10, "end": 16}
            },
            "experiments": {
                "instance_termination": {
                    "probability": 0.2
                }
            }
        }
        
        self.chaos_monkey.configure(config)
        
        self.assertTrue(self.chaos_monkey.is_enabled)
        self.assertEqual(self.chaos_monkey.min_healthy_instances, 2)
        self.assertEqual(self.chaos_monkey.max_instances_to_kill, 2)
        self.assertIn("database", self.chaos_monkey.excluded_services)
        self.assertEqual(self.chaos_monkey.allowed_days, ["monday", "tuesday"])
    
    def test_service_registration(self):
        """Test de registro de servicios"""
        # Verificar servicios registrados
        self.assertIn("test-service", self.chaos_monkey.target_services)
        self.assertIn("database", self.chaos_monkey.target_services)
        
        # Registrar nuevo servicio
        new_service = Service("new-service", ServiceType.CACHE, initial_instances=2)
        self.chaos_monkey.register_service("new-service", new_service)
        self.assertIn("new-service", self.chaos_monkey.target_services)
        
        # Desregistrar servicio
        self.chaos_monkey.unregister_service("new-service")
        self.assertNotIn("new-service", self.chaos_monkey.target_services)
    
    def test_target_service_selection(self):
        """Test de selección de servicio objetivo"""
        # Habilitar chaos monkey
        self.chaos_monkey.is_enabled = True
        
        # Seleccionar servicio
        target = self.chaos_monkey._select_target_service()
        
        # Debería seleccionar un servicio registrado y no excluido
        self.assertIn(target, ["test-service", "database"])
        
        # Excluir todos los servicios excepto uno
        self.chaos_monkey.excluded_services = {"database"}
        target = self.chaos_monkey._select_target_service()
        self.assertEqual(target, "test-service")
    
    def test_force_chaos(self):
        """Test de ejecución forzada de chaos"""
        # Habilitar chaos monkey
        self.chaos_monkey.is_enabled = True
        
        # Obtener conteo inicial de instancias saludables
        initial_healthy = len(self.test_service.get_healthy_instances())
        
        # Forzar chaos en servicio específico
        result = self.chaos_monkey.force_chaos("test-service")
        
        # Verificar resultado
        self.assertEqual(result["status"], "success")
        self.assertIn("test-service", result["message"])
        self.assertIn("service_name", result)
        self.assertIn("instance_id", result)
        
        # Verificar que se terminó una instancia
        current_healthy = len(self.test_service.get_healthy_instances())
        self.assertEqual(current_healthy, initial_healthy - 1)
    
    def test_chaos_blocked_by_safety_rules(self):
        """Test de bloqueo por reglas de seguridad"""
        # Terminar instancias hasta llegar al mínimo
        self.chaos_monkey.is_enabled = True
        self.chaos_monkey.min_healthy_instances = 1
        
        # Terminar instancias hasta que solo quede el mínimo
        self.chaos_monkey.force_chaos("test-service")  # 2 restantes
        self.chaos_monkey.force_chaos("test-service")  # 1 restante
        
        # Ahora intentar terminar una más debería estar bloqueado
        result = self.chaos_monkey.force_chaos("test-service")
        
        # Debería estar bloqueado por reglas de seguridad o no tener servicios elegibles
        # ya que solo queda 1 instancia y el mínimo es 1
        self.assertIn(result["status"], ["blocked", "error"])
    
    def test_simulate_outage(self):
        """Test de simulación de outage"""
        # Habilitar chaos monkey
        self.chaos_monkey.is_enabled = True
        self.chaos_monkey.min_healthy_instances = 1  # Permitir más terminaciones
        
        initial_healthy = len(self.test_service.get_healthy_instances())
        
        # Simular outage con múltiples instancias
        result = self.chaos_monkey.simulate_outage("test-service", instance_count=2)
        
        # Verificar resultado
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["service_name"], "test-service")
        self.assertIn("terminated_instances", result)
        self.assertGreater(len(result["terminated_instances"]), 0)
        
        # Verificar que se terminaron instancias
        current_healthy = len(self.test_service.get_healthy_instances())
        self.assertLess(current_healthy, initial_healthy)
    
    def test_statistics_collection(self):
        """Test de recolección de estadísticas"""
        # Habilitar chaos monkey
        self.chaos_monkey.is_enabled = True
        
        # Ejecutar algunos experimentos
        self.chaos_monkey.force_chaos("test-service")
        self.chaos_monkey.force_chaos("test-service")
        
        # Obtener estadísticas
        stats = self.chaos_monkey.get_statistics()
        
        # Verificar estructura de estadísticas
        self.assertIn("statistics", stats)
        statistics = stats["statistics"]
        self.assertIn("total_terminations", statistics)
        self.assertIn("successful_terminations", statistics)
        self.assertIn("blocked_terminations", statistics)
        
        # Verificar valores
        self.assertGreaterEqual(statistics["total_terminations"], 0)
        self.assertGreaterEqual(statistics["successful_terminations"], 0)
    
    def test_termination_history(self):
        """Test de historial de terminaciones"""
        # Habilitar chaos monkey
        self.chaos_monkey.is_enabled = True
        
        # Ejecutar experimento
        result = self.chaos_monkey.force_chaos("test-service")
        
        if result["status"] == "success":
            # Obtener historial
            history = self.chaos_monkey.get_termination_history(hours=1)
            
            # Verificar que hay entradas en el historial
            self.assertGreater(len(history), 0)
            
            # Verificar estructura de entrada
            entry = history[0]
            self.assertIn("timestamp", entry)
            self.assertIn("service_name", entry)
            self.assertIn("instance_id", entry)
            self.assertIn("chaos_monkey", entry)
    
    def test_exclude_service_temporarily(self):
        """Test de exclusión temporal de servicios"""
        # Excluir servicio por tiempo limitado
        self.chaos_monkey.exclude_service("test-service", duration_minutes=1)
        
        # Verificar que está excluido
        self.assertIn("test-service", self.chaos_monkey.excluded_services)
        
        # Intentar ejecutar chaos en servicio excluido
        self.chaos_monkey.is_enabled = True
        target = self.chaos_monkey._select_target_service()
        
        # No debería seleccionar el servicio excluido
        self.assertNotEqual(target, "test-service")
    
    def test_disable_temporarily(self):
        """Test de deshabilitación temporal"""
        # Habilitar inicialmente
        self.chaos_monkey.is_enabled = True
        
        # Deshabilitar temporalmente
        self.chaos_monkey.disable_temporarily(duration_minutes=1)
        
        # Verificar que está deshabilitado
        self.assertFalse(self.chaos_monkey.is_enabled)
        
        # Intentar ejecutar chaos
        result = self.chaos_monkey.force_chaos()
        self.assertEqual(result["status"], "error")
        self.assertIn("deshabilitado", result["message"])
    
    def test_chaos_monkey_disabled(self):
        """Test de comportamiento cuando está deshabilitado"""
        # Asegurar que está deshabilitado
        self.chaos_monkey.is_enabled = False
        
        # Intentar ejecutar chaos
        result = self.chaos_monkey.force_chaos()
        
        # Debería fallar
        self.assertEqual(result["status"], "error")
        self.assertIn("deshabilitado", result["message"])
    
    def test_callback_registration(self):
        """Test de registro de callbacks"""
        # Crear callback mock
        callback = Mock()
        
        # Registrar callback
        self.chaos_monkey.add_termination_callback(callback)
        
        # Ejecutar chaos
        self.chaos_monkey.is_enabled = True
        result = self.chaos_monkey.force_chaos("test-service")
        
        # Verificar que el callback fue llamado si hubo terminación exitosa
        if result["status"] == "success":
            callback.assert_called_once()

if __name__ == "__main__":
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    # Ejecutar tests
    unittest.main(verbosity=2)
