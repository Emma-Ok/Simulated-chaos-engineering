#!/usr/bin/env python3
"""
Simulador de Chaos Engineering - Archivo principal
Demonstración completa de principios y prácticas de Chaos Engineering

Uso:
    python main.py                              # Simulación básica con configuración por defecto
    python main.py --config config/custom.yaml # Simulación con configuración personalizada
    python main.py --duration 60               # Simulación de 60 minutos
    python main.py --interactive               # Modo interactivo
    python main.py --demo                      # Demostración rápida
"""

import argparse
import sys
import time
import os
from typing import Dict, Any

# Añadir el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chaos_system import ChaosEngineeringSystem
from utils.helpers import setup_colored_logging, format_timestamp, format_duration
from core.service import ServiceType

import logging

def setup_demo_system() -> ChaosEngineeringSystem:
    """
    Configura un sistema de demostración con servicios predefinidos.
    """
    logger = logging.getLogger(__name__)
    logger.info("🎮 Configurando sistema de demostración...")
    
    # Configuración de demostración
    demo_config = {
        "enabled": True,
        "schedule": {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
            "hours": {"start": 0, "end": 23}
        },
        "targets": {
            "services": ["api-service", "auth-service", "db-service", "cache-service"],
            "excluded_services": [],
            "min_healthy_instances": 1,
            "max_instances_to_kill": 1
        },
        "experiments": {
            "instance_termination": {"enabled": True, "probability": 0.3},
            "network_latency": {"enabled": True, "probability": 0.2, "delay_ms": 500},
            "resource_exhaustion": {"enabled": True, "probability": 0.1}
        },
        "monitoring": {
            "collection_interval_seconds": 5,
            "alert_thresholds": {
                "response_time_ms": 1000,
                "error_rate_percent": 5,
                "availability_percent": 80
            }
        },
        "safety": {
            "enabled": True,
            "dry_run_mode": False,
            "require_confirmation_for_destructive": False,
            "max_concurrent_experiments": 2
        },
        "services": {
            "api-service": {
                "type": "api-gateway",
                "initial_instances": 3,
                "min_instances": 2,
                "max_instances": 5,
                "region": "us-east-1"
            },
            "auth-service": {
                "type": "auth-service", 
                "initial_instances": 2,
                "min_instances": 1,
                "max_instances": 4,
                "region": "us-east-1"
            },
            "db-service": {
                "type": "database",
                "initial_instances": 2,
                "min_instances": 1,
                "max_instances": 3,
                "region": "us-east-1"
            },
            "cache-service": {
                "type": "cache",
                "initial_instances": 2,
                "min_instances": 1,
                "max_instances": 4,
                "region": "us-east-1"
            }
        },
        "load_balancer": {
            "strategy": "health_based"
        },
        "reporting": {
            "enabled": True,
            "output_directory": "./reports",
            "formats": ["html", "json"],
            "include_charts": True
        }
    }
    
    # Crear sistema con configuración de demo
    system = ChaosEngineeringSystem()
    system.config = demo_config
    
    return system

def run_quick_demo():
    """
    Ejecuta una demostración rápida de 10 minutos.
    """
    logger = logging.getLogger(__name__)

    print("\n" + "="*60)
    print("🔥 DEMOSTRACIÓN RÁPIDA DE CHAOS ENGINEERING")
    print("="*60)
    print("Duración: 10 minutos")
    print("Servicios: API Gateway, Auth, Database, Cache")
    print("Experimentos: Automáticos y manuales")
    print("="*60 + "\n")

    try:
        system = setup_demo_system()
        with system:
            logger.info("🚀 Iniciando demostración...")

            _demo_phase_1(system)
            _demo_phase_2(system, logger)
            _demo_phase_3(system, logger)
            _demo_phase_4(system, logger)
            _demo_generate_report(system, logger)

            print("\n" + "="*60)
            print("🎉 DEMOSTRACIÓN COMPLETADA")
            print("="*60)
            print("Revisa el reporte HTML generado para ver los resultados detallados.")
            print("="*60 + "\n")

    except KeyboardInterrupt:
        print("\n⚠️ Demostración interrumpida por el usuario")
    except Exception as e:
        logger.error(f"❌ Error en demostración: {e}")
        raise

def _monitor_experiment_progress(exp_runner, exp_id, interval, total_duration):
    """Monitorea el progreso de un experimento cada 'interval' segundos hasta 'total_duration'."""
    for i in range(total_duration // interval):
        time.sleep(interval)
        exp_status = exp_runner.get_experiment_status(exp_id)
        if exp_status:
            print(f"   📊 Estado: {exp_status['status']} - {(i+1)*interval}s transcurridos")
        if exp_status and exp_status['status'] != 'running':
            break

def _handle_experiment_error(logger, context, e):
    logger.error(f"Error en {context}: {e}")

def _print_phase(title, subtitle, duration_min):
    print(f"\n{title} {subtitle} ({duration_min} min)")
    print("-" * 50)

def _show_initial_status(system):
    status = system.get_system_status()
    print(f"✅ Servicios activos: {len(status['services'])}")
    for service_name, service_data in status['services'].items():
        instances = f"{service_data['healthy_instances']}/{service_data['total_instances']}"
        availability = service_data['availability']
        print(f"   {service_name}: {instances} instancias, {availability:.1f}% disponibilidad")

def _run_and_monitor_experiment(system, exp_type, exp_name, exp_args, monitor_interval, monitor_duration, logger, context):
    try:
        exp_id = system.run_chaos_experiment(exp_type, name=exp_name, **exp_args)
        print(f"🔬 Experimento {exp_type} iniciado: {exp_id}")
        _monitor_experiment_progress(system.experiment_runner, exp_id, monitor_interval, monitor_duration)
        return exp_id
    except Exception as e:
        _handle_experiment_error(logger, context, e)
        return None

def _demo_phase_1(system):
    _print_phase("📋 FASE 1:", "Configuración del sistema", 2)
    time.sleep(5)
    _show_initial_status(system)
    time.sleep(115)

def _demo_phase_2(system, logger):
    _print_phase("🧪 FASE 2:", "Experimento de Latencia", 3)
    print("   Añadiendo 800ms de latencia al API Gateway...")
    _run_and_monitor_experiment(
        system,
        "latency",
        "demo-latency",
        {"target_service": "api-service", "latency_ms": 800, "duration_seconds": 180},
        30,
        180,
        logger,
        "experimento de latencia"
    )

def _demo_phase_3(system, logger):
    _print_phase("🐒 FASE 3:", "Chaos Monkey en acción", 3)
    print("🔥 Activando Chaos Monkey...")
    for _ in range(3):
        try:
            result = system.force_chaos_monkey()
            if result['status'] == 'success':
                print(f"   💥 Instancia terminada: {result['service_name']}/{result['instance_id']}")
            else:
                print(f"   🛡️ Terminación bloqueada: {result['message']}")
            time.sleep(60)
        except Exception as e:
            _handle_experiment_error(logger, "Chaos Monkey", e)

def _demo_phase_4(system, logger):
    _print_phase("🩺 FASE 4:", "Diagnóstico final", 2)
    exp_id = _run_and_monitor_experiment(
        system,
        "doctor_monkey",
        "demo-diagnosis",
        {"duration_seconds": 120},
        120,
        120,
        logger,
        "diagnóstico"
    )
    if exp_id:
        exp_status = system.experiment_runner.get_experiment_status(exp_id)
        if exp_status and exp_status.get('results'):
            results = exp_status['results']
            summary = results.get('summary', {})
            print(f"   📊 Salud general: {summary.get('health_status', 'UNKNOWN')}")
            print(f"   📈 Disponibilidad: {summary.get('overall_availability', 0):.1f}%")

def _demo_generate_report(system, logger):
    print("\n📊 Generando reporte final...")
    try:
        report_files = system.generate_report(formats=["html"])
        print(f"✅ Reporte generado: {report_files.get('html', 'No disponible')}")
    except Exception as e:
        _handle_experiment_error(logger, "generando reporte", e)

def run_interactive_mode():
    """
    Ejecuta el modo interactivo donde el usuario puede controlar los experimentos.
    """
    logger = logging.getLogger(__name__)
    system = setup_demo_system()
    
    print("\n" + "="*60)
    print("🎮 MODO INTERACTIVO DE CHAOS ENGINEERING")
    print("="*60)
    print("Comandos disponibles:")
    print("  1 - Ver estado del sistema")
    print("  2 - Ejecutar Chaos Monkey")
    print("  3 - Experimento de latencia")
    print("  4 - Experimento de recursos")
    print("  5 - Diagnóstico del sistema")
    print("  6 - Generar reporte")
    print("  q - Salir")
    print("="*60 + "\n")
    
    try:
        with system:
            while True:
                try:
                    command = input("\n🔥 Ingresa comando: ").strip().lower()
                    
                    if command == 'q':
                        break
                    elif command == '1':
                        show_system_status(system)
                    elif command == '2':
                        run_chaos_monkey_interactive(system)
                    elif command == '3':
                        run_latency_experiment_interactive(system)
                    elif command == '4':
                        run_resource_experiment_interactive(system)
                    elif command == '5':
                        run_diagnosis_interactive(system)
                    elif command == '6':
                        generate_report_interactive(system)
                    else:
                        print("❌ Comando inválido")
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error(f"Error ejecutando comando: {e}")
                    print(f"❌ Error: {e}")
    
    except Exception as e:
        logger.error(f"Error en modo interactivo: {e}")
    
    print("\n👋 ¡Hasta luego!")

def show_system_status(system: ChaosEngineeringSystem):
    """Muestra el estado del sistema"""
    print("\n📊 ESTADO DEL SISTEMA")
    print("-" * 40)
    
    status = system.get_system_status()
    
    print(f"🔄 Sistema activo: {'Sí' if status['is_running'] else 'No'}")
    print(f"⏱️ Tiempo activo: {format_duration(status['uptime_seconds'])}")
    print(f"🔧 Servicios: {len(status['services'])}")
    
    # Detalles de servicios
    for service_name, service_data in status['services'].items():
        instances = f"{service_data['healthy_instances']}/{service_data['total_instances']}"
        availability = service_data['availability']
        response_time = service_data['avg_response_time_ms']
        error_rate = service_data['error_rate']
        
        print(f"\n  📦 {service_name}:")
        print(f"     Instancias: {instances}")
        print(f"     Disponibilidad: {availability:.1f}%")
        print(f"     Tiempo respuesta: {response_time:.1f}ms")
        print(f"     Tasa de error: {error_rate:.2f}%")
    
    # Alertas activas
    monitoring_data = status.get('monitoring', {})
    alerts = monitoring_data.get('alerts', [])
    if alerts:
        print(f"\n⚠️ Alertas activas: {len(alerts)}")
        for alert in alerts[:3]:  # Mostrar solo las primeras 3
            print(f"   {alert['severity']}: {alert['message']}")

def run_chaos_monkey_interactive(system: ChaosEngineeringSystem):
    """Ejecuta Chaos Monkey interactivamente"""
    print("\n🐒 CHAOS MONKEY")
    print("-" * 30)
    
    services = list(system.services.keys())
    if not services:
        print("❌ No hay servicios disponibles")
        return
    
    print("Servicios disponibles:")
    for i, service in enumerate(services, 1):
        print(f"  {i}. {service}")
    print(f"  {len(services)+1}. Aleatorio")
    
    try:
        choice = input("Selecciona servicio (número): ").strip()
        
        if choice.isdigit():
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(services):
                target_service = services[choice_idx]
            elif choice_idx == len(services):
                target_service = None
            else:
                print("❌ Selección inválida")
                return
        else:
            print("❌ Entrada inválida")
            return
        
        print(f"\n🔥 Ejecutando Chaos Monkey en {target_service or 'servicio aleatorio'}...")
        result = system.force_chaos_monkey(target_service)
        
        if result['status'] == 'success':
            print(f"✅ Instancia terminada: {result['service_name']}/{result['instance_id']}")
        else:
            print(f"🛡️ {result['message']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def run_latency_experiment_interactive(system: ChaosEngineeringSystem):
    """Ejecuta experimento de latencia interactivamente"""
    print("\n🌐 EXPERIMENTO DE LATENCIA")
    print("-" * 35)
    
    services = list(system.services.keys())
    if not services:
        print("❌ No hay servicios disponibles")
        return
    
    print("Servicios disponibles:")
    for i, service in enumerate(services, 1):
        print(f"  {i}. {service}")
    
    try:
        choice = int(input("Selecciona servicio (número): ").strip()) - 1
        if not (0 <= choice < len(services)):
            print("❌ Selección inválida")
            return
        
        target_service = services[choice]
        latency = int(input("Latencia en ms (default 500): ").strip() or "500")
        duration = int(input("Duración en segundos (default 120): ").strip() or "120")
        
        print("🔬 Iniciando experimento de latencia...")
        print(f"   Servicio: {target_service}")
        print(f"   Latencia: {latency}ms")
        print(f"   Duración: {duration}s")
        
        exp_id = system.run_chaos_experiment(
            "latency",
            name="interactive-latency",
            target_service=target_service,
            latency_ms=latency,
            duration_seconds=duration
        )
        
        print(f"✅ Experimento iniciado: {exp_id}")
        print("   Monitoreando progreso...")
        
        # Monitorear progreso
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(10)
            exp_status = system.experiment_runner.get_experiment_status(exp_id)
            if exp_status:
                elapsed = time.time() - start_time
                print(f"   📊 Estado: {exp_status['status']} - {elapsed:.0f}s transcurridos")
                
                if exp_status['status'] != 'running':
                    break
        
        print("✅ Experimento completado")
        
    except (ValueError, KeyboardInterrupt):
        print("❌ Entrada inválida o operación cancelada")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_resource_experiment_interactive(system: ChaosEngineeringSystem):
    """Ejecuta experimento de recursos interactivamente"""
    print("\n💾 EXPERIMENTO DE RECURSOS")
    print("-" * 35)
    
    services = list(system.services.keys())
    if not services:
        print("❌ No hay servicios disponibles")
        return
    
    print("Servicios disponibles:")
    for i, service in enumerate(services, 1):
        print(f"  {i}. {service}")
    
    print("\nTipos de recurso:")
    print("  1. CPU")
    print("  2. Memoria")
    
    try:
        service_choice = int(input("Selecciona servicio (número): ").strip()) - 1
        resource_choice = int(input("Selecciona recurso (número): ").strip())
        
        if not (0 <= service_choice < len(services)):
            print("❌ Selección de servicio inválida")
            return
        
        if resource_choice not in [1, 2]:
            print("❌ Selección de recurso inválida")
            return
        
        target_service = services[service_choice]
        resource_type = "cpu" if resource_choice == 1 else "memory"
        exhaustion_level = float(input("Nivel de agotamiento (0.0-1.0, default 0.9): ").strip() or "0.9")
        duration = int(input("Duración en segundos (default 120): ").strip() or "120")
        
        print("\n💥 Iniciando experimento de recursos...")
        print(f"   Servicio: {target_service}")
        print(f"   Recurso: {resource_type.upper()}")
        print(f"   Nivel: {exhaustion_level*100:.0f}%")
        print(f"   Duración: {duration}s")
        
        exp_id = system.run_chaos_experiment(
            "resource_exhaustion",
            name="interactive-resources",
            target_service=target_service,
            resource_type=resource_type,
            exhaustion_level=exhaustion_level,
            duration_seconds=duration
        )
        
        print(f"✅ Experimento iniciado: {exp_id}")
        
    except (ValueError, KeyboardInterrupt):
        print("❌ Entrada inválida o operación cancelada")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_diagnosis_interactive(system: ChaosEngineeringSystem):
    """Ejecuta diagnóstico del sistema"""
    print("\n🩺 DIAGNÓSTICO DEL SISTEMA")
    print("-" * 35)
    
    duration = int(input("Duración del diagnóstico en segundos (default 60): ").strip() or "60")
    
    try:
        print(f"\n🔍 Iniciando diagnóstico por {duration} segundos...")
        
        exp_id = system.run_chaos_experiment(
            "doctor_monkey",
            name="interactive-diagnosis",
            duration_seconds=duration
        )
        
        print(f"✅ Diagnóstico iniciado: {exp_id}")
        print("   Analizando salud del sistema...")
        
        # Esperar a que termine
        time.sleep(duration + 5)
        
        # Obtener resultados
        exp_status = system.experiment_runner.get_experiment_status(exp_id)
        if exp_status and exp_status.get('results'):
            results = exp_status['results']
            summary = results.get('summary', {})
            
            print("\n📊 RESULTADOS DEL DIAGNÓSTICO:")
            print(f"   Salud general: {summary.get('health_status', 'UNKNOWN')}")
            print(f"   Disponibilidad: {summary.get('overall_availability', 0):.1f}%")
            print(f"   Instancias totales: {summary.get('total_instances', 0)}")
            print(f"   Instancias saludables: {summary.get('healthy_instances', 0)}")
            print(f"   Instancias degradadas: {summary.get('degraded_instances', 0)}")
        else:
            print("⚠️ No se pudieron obtener resultados del diagnóstico")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def generate_report_interactive(system: ChaosEngineeringSystem):
    """Genera reporte interactivamente"""
    print("\n📊 GENERAR REPORTE")
    print("-" * 25)
    
    print("Formatos disponibles:")
    print("  1. HTML")
    print("  2. JSON")
    print("  3. Ambos")
    
    try:
        choice = int(input("Selecciona formato (número): ").strip())
        
        if choice == 1:
            formats = ["html"]
        elif choice == 2:
            formats = ["json"]
        elif choice == 3:
            formats = ["html", "json"]
        else:
            print("❌ Selección inválida")
            return
        
        include_charts = input("¿Incluir gráficos? (s/n, default s): ").strip().lower()
        include_charts = include_charts != 'n'
        
        print("\n📈 Generando reporte...")
        print(f"   Formatos: {', '.join(formats)}")
        print(f"   Gráficos: {'Sí' if include_charts else 'No'}")
        
        report_files = system.generate_report(formats=formats, include_charts=include_charts)
        
        print("\n✅ Reporte generado exitosamente:")
        for format_type, file_path in report_files.items():
            print(f"   {format_type.upper()}: {file_path}")
        
    except (ValueError, KeyboardInterrupt):
        print("❌ Entrada inválida o operación cancelada")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Simulador de Chaos Engineering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --demo                          # Demostración rápida de 10 minutos
  python main.py --duration 30                  # Simulación de 30 minutos
  python main.py --config config/custom.yaml    # Usar configuración personalizada
  python main.py --interactive                  # Modo interactivo
  python main.py --log-level DEBUG              # Logs detallados
        """
    )
    
    parser.add_argument(
        "--config",
        help="Archivo de configuración YAML (opcional)",
        type=str
    )
    
    parser.add_argument(
        "--duration",
        help="Duración de la simulación en minutos (default: 30)",
        type=int,
        default=30
    )
    
    parser.add_argument(
        "--interactive",
        help="Modo interactivo",
        action="store_true"
    )
    
    parser.add_argument(
        "--demo",
        help="Demostración rápida de 10 minutos",
        action="store_true"
    )
    
    parser.add_argument(
        "--log-level",
        help="Nivel de logging (DEBUG, INFO, WARNING, ERROR)",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO"
    )
    
    parser.add_argument(
        "--no-colors",
        help="Deshabilitar colores en logs",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    if args.no_colors:
        from utils.helpers import setup_logging
        setup_logging(args.log_level)
    else:
        setup_colored_logging(args.log_level)
    
    logger = logging.getLogger(__name__)
    
    # Banner de inicio
    print("\n" + "="*80)
    print("🔥 SIMULADOR DE CHAOS ENGINEERING")
    print("="*80)
    print("Versión: 1.0.0")
    print("Autor: Sistema de Demostración")
    print(f"Inicio: {format_timestamp()}")
    print("="*80)
    
    try:
        if args.demo:
            run_quick_demo()
        elif args.interactive:
            run_interactive_mode()
        else:
            # Simulación estándar
            logger.info(f"🚀 Iniciando simulación de {args.duration} minutos...")
            
            if args.config:
                if not os.path.exists(args.config):
                    logger.error(f"❌ Archivo de configuración no encontrado: {args.config}")
                    sys.exit(1)
                system = ChaosEngineeringSystem(args.config)
            else:
                logger.info("📋 Usando configuración por defecto")
                system = setup_demo_system()
            
            # Ejecutar simulación
            with system:
                system.run_simulation(duration_minutes=args.duration)
    
    except KeyboardInterrupt:
        logger.info("\n⚠️ Simulación interrumpida por el usuario")
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        if args.log_level == "DEBUG":
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "="*80)
    print("🎉 SIMULACIÓN COMPLETADA")
    print("="*80)
    print("Gracias por usar el Simulador de Chaos Engineering!")
    print("Revisa los reportes generados en el directorio ./reports/")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
