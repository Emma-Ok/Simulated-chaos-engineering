#!/usr/bin/env python3
"""
Ejemplo de configuración mediante archivos YAML.
Demuestra cómo usar configuración externa para experimentos
y personalizar el comportamiento del sistema.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chaos_system import ChaosEngineeringSystem
try:
    import yaml
except ImportError:
    print("PyYAML no instalado. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
    import yaml

def configuration_example():
    """Demuestra el uso de configuración externa"""
    print("=== Ejemplo de Configuración con YAML ===\n")
    
    # Crear configuración personalizada
    custom_config = {
        "system": {
            "name": "demo-ecommerce",
            "region": "us-west-2",
            "monitoring_interval": 10
        },
        "services": [
            {
                "name": "web-frontend",
                "type": "web",
                "instances": 3,
                "auto_scaling": {
                    "enabled": True,
                    "min_instances": 2,
                    "max_instances": 6,
                    "cpu_threshold": 75
                }
            },
            {
                "name": "api-backend",
                "type": "api", 
                "instances": 4,
                "auto_scaling": {
                    "enabled": True,
                    "min_instances": 2,
                    "max_instances": 8,
                    "cpu_threshold": 80
                }
            },
            {
                "name": "user-db",
                "type": "database",
                "instances": 2,
                "auto_scaling": {
                    "enabled": False
                }
            }
        ],
        "chaos_monkey": {
            "enabled": True,
            "schedule": {
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                "hours": {"start": 10, "end": 16}
            },
            "safety": {
                "min_healthy_instances": 1,
                "max_instances_to_kill": 1,
                "excluded_services": ["user-db"]
            },
            "probabilities": {
                "termination": 0.15,
                "latency": 0.08,
                "resource_exhaustion": 0.05
            }
        },
        "experiments": {
            "enabled_experiments": [
                "instance_termination",
                "network_latency", 
                "resource_exhaustion"
            ],
            "default_duration": 300,
            "monitoring_interval": 30
        },
        "resilience_patterns": {
            "circuit_breaker": {
                "enabled": True,
                "failure_threshold": 5,
                "recovery_timeout": 60,
                "half_open_max_calls": 3
            },
            "retry": {
                "enabled": True,
                "max_retries": 3,
                "base_delay": 1,
                "max_delay": 10,
                "exponential_base": 2
            },
            "bulkhead": {
                "enabled": True,
                "max_concurrent_calls": 100
            }
        }
    }
    
    # Guardar configuración en archivo temporal
    config_file = "temp_chaos_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(custom_config, f, default_flow_style=False, indent=2)
    
    print("1. Configuración creada y guardada en temp_chaos_config.yaml")
    
    # Inicializar sistema con configuración
    print("2. Inicializando sistema con configuración personalizada...")
    system = ChaosEngineeringSystem(config_path=config_file)
    
    # La configuración se aplicará automáticamente
    print("3. Servicios configurados desde YAML:")
    for service_config in custom_config["services"]:
        service_name = service_config["name"]
        service_type = service_config["type"]
        instances = service_config["instances"]
        
        system.add_service(service_name, service_type, instances)
        print(f"   ✓ {service_name} ({service_type}) - {instances} instancias")
    
    # Inicializar componentes
    system.initialize_components()
    
    print("\n4. Configuración del Chaos Monkey:")
    chaos_config = custom_config["chaos_monkey"]
    print(f"   - Habilitado: {chaos_config['enabled']}")
    print(f"   - Horario: {chaos_config['schedule']['days']} "
          f"{chaos_config['schedule']['hours']['start']}-{chaos_config['schedule']['hours']['end']}")
    print(f"   - Servicios excluidos: {chaos_config['safety']['excluded_services']}")
    print(f"   - Probabilidad de terminación: {chaos_config['probabilities']['termination']*100}%")
    
    print("\n5. Configuración de patrones de resiliencia:")
    patterns_config = custom_config["resilience_patterns"]
    for pattern_name, pattern_config in patterns_config.items():
        print(f"   - {pattern_name.replace('_', ' ').title()}: "
              f"{'Habilitado' if pattern_config['enabled'] else 'Deshabilitado'}")
    
    # Iniciar el sistema
    print("\n6. Iniciando sistema...")
    system.start()
    
    # Simular actividad
    print("7. Simulando tráfico de usuario...")
    system.simulate_traffic(duration=30, requests_per_second=75)
    
    print("\n8. Estado del sistema configurado:")
    system.show_system_status()
    
    # Ejecutar chaos monkey según configuración
    print("\n9. Ejecutando Chaos Monkey con configuración personalizada...")
    
    # Forzar algunos experimentos para demostración
    if system.chaos_monkey.is_enabled:
        for i in range(3):
            print(f"   Experimento {i+1}/3:")
            result = system.chaos_monkey.force_chaos()
            print(f"   Resultado: {result.get('message', 'N/A')}")
            
            # Mostrar estado después de cada experimento
            system.show_system_status()
            print()
    
    print("10. Estadísticas del Chaos Monkey:")
    stats = system.chaos_monkey.get_statistics()
    print(f"    - Total terminaciones: {stats['total_terminations']}")
    print(f"    - Terminaciones exitosas: {stats['successful_terminations']}")
    print(f"    - Terminaciones bloqueadas: {stats['blocked_terminations']}")
    print(f"    - Tasa de éxito: {stats['success_rate']:.1%}")
    
    # Generar reporte
    print("\n11. Generando reporte...")
    report_path = system.generate_report()
    print(f"Reporte generado en: {report_path}")
    
    # Limpiar
    system.stop()
    
    # Eliminar archivo temporal
    try:
        os.remove(config_file)
        print(f"\n12. Archivo temporal {config_file} eliminado")
    except OSError:
        pass
    
    print("\n=== Configuración Completada ===")
    print("\nBeneficios de la configuración externa:")
    print("✓ Flexibilidad para diferentes entornos")
    print("✓ Configuración versionada y reproducible")
    print("✓ Fácil personalización sin cambios de código")
    print("✓ Separación de configuración y lógica")

if __name__ == "__main__":
    configuration_example()
