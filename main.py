#!/usr/bin/env python3
"""
Simulador de Chaos Engineering - Archivo principal
Demonstración completa de principios y prácticas de Chaos Engineering

TIEMPOS OPTIMIZADOS:
- Demo rápida: 4 minutos máximo
- Simulación por defecto: 4 minutos
- Fases de demo: 30-60 segundos cada una

Uso:
    python main.py                              # Interfaz de menús (recomendado)
    python main.py --demo                       # Demostración rápida de 4 minutos
    python main.py --duration 4                 # Simulación de 4 minutos
    python main.py --config config/custom.yaml # Usar configuración personalizada
    python main.py --interactive               # Modo interactivo original
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
    
    CONFIGURACIÓN OPTIMIZADA PARA VELOCIDAD:
    - Intervalos cortos para demostración rápida
    - Probabilidades altas para actividad visible
    - Tiempos de monitoreo reducidos
    """
    logger = logging.getLogger(__name__)
    logger.info("🎮 Configurando sistema de demostración...")
    
    # Configuración de demostración con TIEMPOS OPTIMIZADOS
    demo_config = {
        "enabled": True,
        "schedule": {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
            "hours": {"start": 0, "end": 23}  # 24/7 para demos
        },
        "targets": {
            "services": ["api-service", "auth-service", "db-service", "cache-service"],
            "excluded_services": [],
            "min_healthy_instances": 1,  # Permitir más chaos para demos
            "max_instances_to_kill": 1
        },
        "experiments": {
            # PROBABILIDADES ALTAS para demostración visible
            "instance_termination": {"enabled": True, "probability": 0.5},  # 50% vs 30%
            "network_latency": {"enabled": True, "probability": 0.3, "delay_ms": 300},  # 30% vs 20%, 300ms vs 500ms
            "resource_exhaustion": {"enabled": True, "probability": 0.2}  # 20% vs 10%
        },
        "monitoring": {
            "collection_interval_seconds": 2,  # 2s vs 5s - más frecuente
            "alert_thresholds": {
                "response_time_ms": 800,   # 800ms vs 1000ms - más sensible
                "error_rate_percent": 3,   # 3% vs 5% - más estricto
                "availability_percent": 85  # 85% vs 80% - más exigente
            }
        },
        "safety": {
            "enabled": True,
            "dry_run_mode": False,
            "require_confirmation_for_destructive": False,  # Sin confirmación para demos
            "max_concurrent_experiments": 3  # Más experimentos simultáneos
        },
        "services": {
            "api-service": {
                "type": "api-gateway",
                "initial_instances": 3,
                "min_instances": 1,  # Menos mínimo para más drama
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
    Ejecuta una demostración rápida de 4 minutos.
    
    ESTRUCTURA DE LA DEMO (4 minutos total):
    - Fase 1: Configuración (30s)
    - Fase 2: Experimento de Latencia (60s) 
    - Fase 3: Chaos Monkey (90s)
    - Fase 4: Diagnóstico final (60s)
    """
    logger = logging.getLogger(__name__)

    print("\n" + "="*60)
    print("🔥 DEMOSTRACIÓN RÁPIDA DE CHAOS ENGINEERING")
    print("="*60)
    print("⏱️ Duración: 4 minutos optimizados")
    print("🏗️ Servicios: API Gateway, Auth, Database, Cache")
    print("🧪 Experimentos: Automáticos y manuales")
    print("📊 Métricas: Monitoreo en tiempo real")
    print("="*60 + "\n")

    try:
        system = setup_demo_system()
        with system:
            logger.info("🚀 Iniciando demostración...")

            _demo_phase_1(system)      # 30 segundos
            _demo_phase_2(system, logger)  # 60 segundos  
            _demo_phase_3(system, logger)  # 90 segundos
            _demo_phase_4(system, logger)  # 60 segundos
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
    """Maneja errores de experimentos de forma consistente."""
    logger.error(f"Error en {context}: {e}")

def _print_phase(title, subtitle, duration_min):
    """Imprime el header de una fase de la demo."""
    duration_seconds = int(duration_min * 60)
    print(f"\n{title} {subtitle} ({duration_seconds}s)")
    print("-" * 50)

def _show_initial_status(system):
    """Muestra el estado inicial del sistema."""
    status = system.get_system_status()
    print(f"✅ Servicios activos: {len(status['services'])}")
    for service_name, service_data in status['services'].items():
        instances = f"{service_data['healthy_instances']}/{service_data['total_instances']}"
        availability = service_data['availability']
        print(f"   {service_name}: {instances} instancias, {availability:.1f}% disponibilidad")

def _run_and_monitor_experiment(system, exp_type, exp_name, exp_args, monitor_interval, monitor_duration, logger, context):
    """Ejecuta y monitorea un experimento con manejo de errores."""
    try:
        exp_id = system.run_chaos_experiment(exp_type, name=exp_name, **exp_args)
        print(f"🔬 Experimento {exp_type} iniciado: {exp_id}")
        _monitor_experiment_progress(system.experiment_runner, exp_id, monitor_interval, monitor_duration)
        return exp_id
    except Exception as e:
        _handle_experiment_error(logger, context, e)
        return None

def _demo_phase_1(system):
    """FASE 1: Configuración inicial del sistema (30 segundos)"""
    _print_phase("📋 FASE 1:", "Configuración del sistema", 0.5)
    print("   Inicializando servicios...")
    time.sleep(2)
    _show_initial_status(system)
    print("   Esperando estabilización...")
    time.sleep(28)  # Total: 30 segundos

def _demo_phase_2(system, logger):
    """FASE 2: Experimento de Latencia (60 segundos)"""
    _print_phase("🧪 FASE 2:", "Experimento de Latencia", 1)
    print("   Añadiendo 500ms de latencia al API Gateway...")
    
    exp_id = _run_and_monitor_experiment(
        system,
        "latency",
        "demo-latency",
        {"target_service": "api-service", "latency_ms": 500, "duration_seconds": 60},
        15,  # Monitorear cada 15s
        60,  # Por 60s total
        logger,
        "experimento de latencia"
    )

def _demo_phase_3(system, logger):
    """FASE 3: Chaos Monkey en acción (90 segundos)"""
    _print_phase("🐒 FASE 3:", "Chaos Monkey en acción", 1.5)
    print("🔥 Activando Chaos Monkey...")
    
    # 3 terminaciones con intervalos de 30s
    for i in range(3):
        try:
            result = system.force_chaos_monkey()
            if result['status'] == 'success':
                print(f"   💥 Instancia terminada: {result['service_name']}/{result['instance_id']}")
            else:
                print(f"   🛡️ Terminación bloqueada: {result['message']}")
            time.sleep(30)  # 30s entre terminaciones
        except Exception as e:
            _handle_experiment_error(logger, "Chaos Monkey", e)

def _demo_phase_4(system, logger):
    """FASE 4: Diagnóstico final (60 segundos)"""
    _print_phase("🩺 FASE 4:", "Diagnóstico final", 1)
    
    exp_id = _run_and_monitor_experiment(
        system,
        "doctor_monkey",
        "demo-diagnosis",
        {"duration_seconds": 60},
        30,  # Monitorear cada 30s
        60,  # Por 60s total
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
    """Genera el reporte final de la demo."""
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
    """Función principal con configuraciones optimizadas de tiempo"""
    parser = argparse.ArgumentParser(
        description="Simulador de Chaos Engineering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso (TIEMPOS OPTIMIZADOS):
  python main.py                                 # Interfaz de menús (por defecto)
  python main.py --demo                          # Demostración rápida de 4 minutos
  python main.py --duration 4                   # Simulación de 4 minutos máximo
  python main.py --config config/custom.yaml    # Usar configuración personalizada
  python main.py --interactive                  # Modo interactivo original
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
        help="Duración de la simulación en minutos (default: 4, máximo recomendado: 4)",
        type=int,
        default=4  # Cambiado de 30 a 4 minutos
    )
    
    parser.add_argument(
        "--interactive",
        help="Modo interactivo original (línea de comandos)",
        action="store_true"
    )
    
    parser.add_argument(
        "--menu",
        help="Usar interfaz de menús (por defecto)",
        action="store_true"
    )
    
    parser.add_argument(
        "--cli",
        help="Forzar modo línea de comandos",
        action="store_true"
    )
    
    parser.add_argument(
        "--demo",
        help="Demostración rápida de 4 minutos",
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
    
    # Validar duración máxima
    if args.duration > 4:
        print("⚠️ ADVERTENCIA: Duración máxima recomendada es 4 minutos para demos rápidas")
        print(f"   Configurando duración a {args.duration} minutos como solicitado...")
    
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
        # Determinar el modo de ejecución
        if args.demo:
            run_quick_demo()
        elif args.interactive:
            run_interactive_mode()
        elif args.cli or args.config or args.duration != 4:  # Cambiado de 30 a 4
            # Modo línea de comandos tradicional
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
        else:
            # Modo interfaz de menús (por defecto)
            from utils.menu_interface import MenuInterface
            menu_interface = MenuInterface()
            menu_interface.run()
    
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
