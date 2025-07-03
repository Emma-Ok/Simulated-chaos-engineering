#!/usr/bin/env python3
"""
Ejemplo avanzado de experimentos de Chaos Engineering.
Demuestra experimentos más complejos como Latency Monkey, 
Resource Exhaustion, y Chaos Gorilla.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chaos_system import ChaosEngineeringSystem
from chaos.experiments import LatencyMonkey, ResourceExhaustionMonkey, ChaosGorilla
from chaos.runner import ExperimentRunner
import time

def advanced_experiments_example():
    """Ejecuta experimentos avanzados de chaos engineering"""
    print("=== Ejemplo de Experimentos Avanzados de Chaos Engineering ===\n")
    
    # Inicializar el sistema
    system = ChaosEngineeringSystem()
    
    print("1. Configurando arquitectura de microservicios...")
    # Configurar una arquitectura más compleja
    try:
        system.add_service("api-gateway", "api-gateway", instances=3)
        system.add_service("user-service", "user-profile", instances=4)
        system.add_service("order-service", "payment", instances=3)
        system.add_service("payment-service", "payment", instances=2)
        system.add_service("notification-service", "notification", instances=2)
        system.add_service("database", "database", instances=2)
    except Exception as e:
        print(f"Error configurando servicios: {e}")
        return
    
    # Usar context manager para el ciclo de vida del sistema
    with system:
        print("2. Sistema iniciado...")
        
        # Simular tráfico normal
        print("3. Generando tráfico base...")
        if system.load_balancer:
            system.load_balancer.simulate_traffic(requests_per_second=100, duration_seconds=20)
        
        print("4. Estado inicial del sistema:")
        status = system.get_system_status()
        print(f"   Servicios activos: {len(status.get('services', {}))}")
        print(f"   Sistema ejecutándose: {status.get('is_running', False)}")
        
        print("\n=== FASE 1: Experimento de Latencia ===")
        # Experimento de latencia usando el runner del sistema
        try:
            exp_id = system.run_chaos_experiment(
                "latency",
                name="test-latency",
                target_service="user-service",
                latency_ms=1000,
                duration_seconds=60
            )
            print(f"Experimento de latencia iniciado: {exp_id}")
            time.sleep(30)  # Observar por 30 segundos
            
            # Verificar estado durante el experimento
            exp_status = system.experiment_runner.get_experiment_status(exp_id)
            if exp_status:
                print(f"Estado del experimento: {exp_status['status']}")
            
        except Exception as e:
            print(f"Error en experimento de latencia: {e}")
        
        time.sleep(35)  # Esperar a que termine el experimento
        
        print("\n=== FASE 2: Experimento de Agotamiento de Recursos ===")
        try:
            exp_id = system.run_chaos_experiment(
                "resource_exhaustion",
                name="test-cpu-exhaustion",
                target_service="payment-service",
                resource_type="cpu",
                exhaustion_level=0.9,
                duration_seconds=60
            )
            print(f"Experimento de CPU iniciado: {exp_id}")
            time.sleep(30)
            
            # Verificar estado
            exp_status = system.experiment_runner.get_experiment_status(exp_id)
            if exp_status:
                print(f"Estado del experimento: {exp_status['status']}")
                
        except Exception as e:
            print(f"Error en experimento de recursos: {e}")
        
        time.sleep(35)
        
        print("\n=== FASE 3: Chaos Monkey Avanzado ===")
        try:
            # Múltiples terminaciones
            for i in range(3):
                result = system.force_chaos_monkey()
                print(f"Terminación {i+1}: {result.get('message', 'No disponible')}")
                time.sleep(10)
                
        except Exception as e:
            print(f"Error en chaos monkey: {e}")
        
        print("\n=== FASE 4: Diagnóstico Final ===")
        try:
            exp_id = system.run_chaos_experiment(
                "doctor_monkey",
                name="final-diagnosis",
                duration_seconds=30
            )
            print(f"Diagnóstico iniciado: {exp_id}")
            time.sleep(35)
            
            # Obtener resultados del diagnóstico
            exp_status = system.experiment_runner.get_experiment_status(exp_id)
            if exp_status and exp_status.get('results'):
                results = exp_status['results']
                summary = results.get('summary', {})
                print(f"Salud del sistema: {summary.get('health_status', 'UNKNOWN')}")
                print(f"Disponibilidad general: {summary.get('overall_availability', 0):.1f}%")
                
        except Exception as e:
            print(f"Error en diagnóstico: {e}")
        
        print("\n6. Generando reporte final...")
        try:
            report_files = system.generate_report(formats=["html", "json"], include_charts=True)
            print("Reportes generados:")
            for format_type, path in report_files.items():
                print(f"   {format_type.upper()}: {path}")
        except Exception as e:
            print(f"Error generando reporte: {e}")
    
    print("\n=== Experimentos Avanzados Completados ===")
    print("Resumen de lo observado:")
    print("- Impacto de latencia en cascada entre servicios")
    print("- Comportamiento bajo agotamiento de recursos")
    print("- Capacidad de auto-recuperación del sistema")
    print("- Eficacia de los patrones de resiliencia implementados")
if __name__ == "__main__":
    advanced_experiments_example()
