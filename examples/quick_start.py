#!/usr/bin/env python3
"""
Ejemplo de inicio rápido para el README.
Demuestra el uso básico del simulador de Chaos Engineering.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chaos_system import ChaosEngineeringSystem

def quick_start_example():
    """Ejemplo de inicio rápido"""
    print("=== Inicio Rápido - Simulador de Chaos Engineering ===\n")
    
    # 1. Inicializar el sistema
    system = ChaosEngineeringSystem()
    
    # 2. Agregar servicios
    print("Configurando servicios...")
    system.add_service("api-gateway", "api-gateway", instances=3)
    system.add_service("user-service", "user-profile", instances=2)
    system.add_service("database", "database", instances=2)
    
    # 3. Inicializar componentes
    system.initialize()
    
    # 4. Iniciar el sistema
    print("Iniciando sistema...")
    system.start()
    
    # 5. Ver estado inicial
    print("\nEstado inicial:")
    status = system.get_system_status()
    print(f"Servicios activos: {status.get('services_count', 0)}")
    print(f"Sistema ejecutándose: {status.get('is_running', False)}")
    
    # 6. Ejecutar experimento de chaos
    print("\nEjecutando experimento de chaos...")
    result = system.force_chaos_monkey()
    print(f"Resultado: {result.get('message', 'Experimento ejecutado')}")
    
    # 7. Ver estado después del chaos
    print("\nEstado después del experimento:")
    status = system.get_system_status()
    print(f"Servicios activos: {status.get('services_count', 0)}")
    
    # 8. Generar reporte
    print("\nGenerando reporte...")
    reports = system.generate_report()
    if reports:
        for format_type, path in reports.items():
            print(f"Reporte {format_type}: {path}")
    
    # 9. Detener sistema
    system.stop()
    
    print("\n✅ Ejemplo completado exitosamente!")

if __name__ == "__main__":
    quick_start_example()
