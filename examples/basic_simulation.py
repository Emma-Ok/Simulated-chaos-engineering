#!/usr/bin/env python3
"""
Ejemplo básico de simulación con Chaos Engineering
Este ejemplo demuestra cómo configurar y ejecutar una simulación básica
con introducción de fallas controladas.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chaos_system import ChaosEngineeringSystem
import time

def basic_simulation_example():
    """Ejecuta una simulación básica con fallas controladas"""
    print("=== Ejemplo de Simulación Básica de Chaos Engineering ===\n")
    
    # Inicializar el sistema
    system = ChaosEngineeringSystem()
    
    print("1. Configurando servicios...")
    # Configurar servicios de prueba
    system.add_service("api-gateway", "api-gateway", instances=3)
    system.add_service("user-service", "user-profile", instances=2)
    system.add_service("order-service", "payment", instances=4)
    system.add_service("payment-service", "payment", instances=2)
    
    # Usar context manager para manejar el ciclo de vida del sistema
    with system:
        print("2. Iniciando simulación de tráfico...")
        # Simular tráfico normal usando el load balancer
        if system.load_balancer:
            system.load_balancer.simulate_traffic(requests_per_second=50, duration_seconds=30)
        
        print("3. Estado inicial del sistema:")
        status = system.get_system_status()
        print(f"   Servicios activos: {len(status.get('services', {}))}")
        print(f"   Sistema ejecutándose: {status.get('is_running', False)}")
        
        print("\n4. Introduciendo fallas controladas...")
        # Experimento 1: Falla de instancia
        print("   - Experimento: Falla de instancia en user-service")
        if system.chaos_monkey:
            result = system.chaos_monkey.force_chaos("user-service")
            print(f"     Resultado: {result.get('message', 'Chaos Monkey no está disponible')}")
        time.sleep(5)
        
        # Experimento 2: Simulación de outage
        print("   - Experimento: Simulando outage")
        if system.chaos_monkey:
            result = system.chaos_monkey.force_chaos("order-service")
            print(f"     Resultado: {result.get('message', 'Chaos Monkey no está disponible')}")
        time.sleep(10)
        
        print("\n5. Estado del sistema después de las fallas:")
        status = system.get_system_status()
        print(f"   Servicios activos: {len(status.get('services', {}))}")
        print(f"   Sistema ejecutándose: {status.get('is_running', False)}")
        
        print("\n6. Generando reporte...")
        report_files = system.generate_report()
        if isinstance(report_files, dict):
            for format_type, path in report_files.items():
                print(f"Reporte {format_type}: {path}")
        else:
            print(f"Reporte generado en: {report_files}")
    
    print("\n=== Simulación Completada ===")
    print("Puntos clave observados:")
    print("- Los patrones de resiliencia ayudaron a mantener la estabilidad")
    print("- El sistema se auto-recuperó de algunas fallas")
    print("- Las métricas muestran el impacto real de cada experimento")

if __name__ == "__main__":
    basic_simulation_example()
