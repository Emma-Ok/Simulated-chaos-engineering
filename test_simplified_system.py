#!/usr/bin/env python3
"""
Prueba rápida del sistema simplificado de Chaos Engineering.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_system():
    """Prueba básica del sistema."""
    print("🔥 Probando sistema simplificado...")
    
    try:
        # Importaciones
        from simple_chaos_system import SimpleChaosSystem, SystemConfig
        from chaos_experiments_core import ExperimentType, create_latency_experiment
        print("✓ Importaciones correctas")
        
        # Crear sistema
        config = SystemConfig()
        system = SimpleChaosSystem(config)
        print("✓ Sistema creado")
        
        # Inicializar
        system.initialize()
        print("✓ Sistema inicializado")
        
        # Verificar componentes
        assert len(system.services) > 0, "No se crearon servicios"
        assert system.load_balancer is not None, "Load balancer no creado"
        assert system.monitoring is not None, "Monitoring no creado"
        assert system.experiment_manager is not None, "Experiment manager no creado"
        print("✓ Componentes verificados")
        
        # Iniciar sistema
        system.start()
        print("✓ Sistema iniciado")
        
        # Obtener estado
        status = system.get_system_status()
        assert 'services' in status, "Estado incompleto"
        assert len(status['services']) > 0, "No hay servicios en estado"
        print("✓ Estado obtenido")
        
        # Detener sistema
        system.stop()
        print("✓ Sistema detenido")
        
        print("\n✅ TODAS LAS PRUEBAS PASARON - Sistema funciona correctamente")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBA: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)
