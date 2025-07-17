#!/usr/bin/env python3
"""
SIMULADOR DE CHAOS ENGINEERING - VERSIÓN SIMPLIFICADA
======================================================

Sistema unificado y centralizado para demostraciones de Chaos Engineering.

Uso:
    python demo_chaos.py                    # Demo rápida de 3 minutos
    python demo_chaos.py --duration 2       # Demo de 2 minutos
    python demo_chaos.py --interactive      # Modo interactivo
    python demo_chaos.py --help            # Ayuda

Características:
- Sistema simplificado y centralizado
- Experimentos unificados
- Interfaz limpia y clara
- Demostraciones automáticas
- Reportes integrados
"""

import argparse
import sys
import time
import logging

# Añadir directorio actual al path
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simple_chaos_system import SimpleChaosSystem, SystemConfig
from utils.helpers import setup_logging, format_timestamp

def print_banner():
    """Muestra el banner principal."""
    print("\n" + "="*70)
    print("🔥 SIMULADOR DE CHAOS ENGINEERING - VERSIÓN SIMPLIFICADA")
    print("="*70)
    print("🎯 Sistema centralizado para demostraciones de chaos")
    print("⚡ Experimentos unificados y automatizados")
    print("📊 Monitoreo y reportes integrados")
    print("="*70 + "\n")

def run_automatic_demo(duration_minutes: int):
    """Ejecuta una demostración automática."""
    print(f"🚀 Iniciando demostración automática de {duration_minutes} minutos\n")
    
    # Crear sistema con configuración optimizada para demo
    config = SystemConfig(
        monitoring_interval_seconds=3,  # Monitoreo más frecuente
        max_concurrent_experiments=2,   # Menos experimentos concurrentes
        safety_checks_enabled=True      # Seguridad habilitada
    )
    
    try:
        with SimpleChaosSystem(config) as system:
            system.run_basic_demo(duration_minutes)
    except KeyboardInterrupt:
        print("\n⚠️ Demostración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error en demostración: {e}")
        return False
    
    return True

def run_interactive_mode():
    """Ejecuta el modo interactivo."""
    print("🎮 MODO INTERACTIVO")
    print("-" * 50)
    
    system = SimpleChaosSystem()
    
    try:
        system.initialize()
        system.start()
        
        print("\nSistema iniciado. Comandos disponibles:")
        print("  1 - Ver estado del sistema")
        print("  2 - Experimento de latencia")
        print("  3 - Experimento de terminación")
        print("  4 - Experimento de recursos")
        print("  5 - Diagnóstico del sistema")
        print("  6 - Generar reporte")
        print("  7 - Parar todos los experimentos")
        print("  0 - Salir")
        print("-" * 50)
        
        while True:
            try:
                choice = input("\n👉 Selecciona una opción: ").strip()
                
                if choice == "0":
                    break
                elif choice == "1":
                    show_system_status_interactive(system)
                elif choice == "2":
                    run_latency_experiment_interactive(system)
                elif choice == "3":
                    run_termination_experiment_interactive(system)
                elif choice == "4":
                    run_resource_experiment_interactive(system)
                elif choice == "5":
                    run_health_check_interactive(system)
                elif choice == "6":
                    generate_report_interactive(system)
                elif choice == "7":
                    stop_all_experiments_interactive(system)
                else:
                    print("❌ Opción inválida")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
    finally:
        system.stop()
        print("\n👋 Sistema detenido. ¡Hasta luego!")

def show_system_status_interactive(system: SimpleChaosSystem):
    """Muestra el estado del sistema en modo interactivo."""
    print("\n📊 ESTADO DEL SISTEMA")
    print("-" * 40)
    
    status = system.get_system_status()
    
    print(f"🔄 Sistema: {'Activo' if status['system_running'] else 'Inactivo'}")
    print(f"⏱️ Tiempo activo: {status['uptime_formatted']}")
    print(f"🔧 Servicios: {len(status['services'])}")
    
    # Mostrar servicios
    for service_name, service_data in status['services'].items():
        instances = f"{service_data['healthy_instances']}/{service_data['total_instances']}"
        availability = service_data['availability']
        response_time = service_data['avg_response_time_ms']
        
        print(f"\n  📦 {service_name}:")
        print(f"     Instancias: {instances}")
        print(f"     Disponibilidad: {availability:.1f}%")
        print(f"     Tiempo respuesta: {response_time:.1f}ms")
    
    # Mostrar experimentos
    exp_status = status.get('experiments', {})
    if exp_status:
        print(f"\n🧪 Experimentos:")
        print(f"   Activos: {exp_status.get('active_experiments', 0)}")
        print(f"   Completados: {exp_status.get('completed_experiments', 0)}")
        print(f"   Tasa de éxito: {exp_status.get('success_rate', 0):.1f}%")
    
    # Mostrar alertas
    monitoring = status.get('monitoring', {})
    if monitoring.get('active_alerts', 0) > 0:
        print(f"\n⚠️ Alertas activas: {monitoring['active_alerts']}")

def run_latency_experiment_interactive(system: SimpleChaosSystem):
    """Ejecuta experimento de latencia en modo interactivo."""
    print("\n🌐 EXPERIMENTO DE LATENCIA")
    print("-" * 35)
    
    services = list(system.services.keys())
    print("Servicios disponibles:")
    for i, service in enumerate(services, 1):
        print(f"  {i}. {service}")
    
    try:
        choice = int(input("Selecciona servicio (número): ")) - 1
        if not (0 <= choice < len(services)):
            print("❌ Selección inválida")
            return
        
        target_service = services[choice]
        latency = int(input("Latencia en ms (default 500): ") or "500")
        duration = int(input("Duración en segundos (default 60): ") or "60")
        
        print(f"\n🔬 Iniciando experimento de latencia...")
        exp_id = system.run_latency_experiment(target_service, latency, duration)
        print(f"✅ Experimento iniciado: {exp_id}")
        
    except (ValueError, KeyboardInterrupt):
        print("❌ Operación cancelada")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_termination_experiment_interactive(system: SimpleChaosSystem):
    """Ejecuta experimento de terminación en modo interactivo."""
    print("\n💀 EXPERIMENTO DE TERMINACIÓN")
    print("-" * 35)
    
    services = list(system.services.keys())
    print("Servicios disponibles:")
    for i, service in enumerate(services, 1):
        print(f"  {i}. {service}")
    print(f"  {len(services)+1}. Aleatorio")
    
    try:
        choice = int(input("Selecciona servicio (número): "))
        
        if choice == len(services) + 1:
            target_service = None
        elif 1 <= choice <= len(services):
            target_service = services[choice - 1]
        else:
            print("❌ Selección inválida")
            return
        
        print(f"\n💥 Terminando instancia...")
        exp_id = system.run_termination_experiment(target_service)
        print(f"✅ Experimento iniciado: {exp_id}")
        
    except (ValueError, KeyboardInterrupt):
        print("❌ Operación cancelada")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_resource_experiment_interactive(system: SimpleChaosSystem):
    """Ejecuta experimento de recursos en modo interactivo."""
    print("\n💾 EXPERIMENTO DE RECURSOS")
    print("-" * 35)
    
    services = list(system.services.keys())
    print("Servicios disponibles:")
    for i, service in enumerate(services, 1):
        print(f"  {i}. {service}")
    
    print("\nTipos de recurso:")
    print("  1. CPU")
    print("  2. Memoria")
    
    try:
        service_choice = int(input("Selecciona servicio (número): ")) - 1
        resource_choice = int(input("Selecciona recurso (número): "))
        
        if not (0 <= service_choice < len(services)) or resource_choice not in [1, 2]:
            print("❌ Selección inválida")
            return
        
        target_service = services[service_choice]
        resource_type = "cpu" if resource_choice == 1 else "memory"
        exhaustion = float(input("Nivel de agotamiento (0.0-1.0, default 0.8): ") or "0.8")
        duration = int(input("Duración en segundos (default 60): ") or "60")
        
        print(f"\n💥 Iniciando experimento de recursos...")
        exp_id = system.run_resource_experiment(target_service, resource_type, exhaustion, duration)
        print(f"✅ Experimento iniciado: {exp_id}")
        
    except (ValueError, KeyboardInterrupt):
        print("❌ Operación cancelada")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_health_check_interactive(system: SimpleChaosSystem):
    """Ejecuta diagnóstico en modo interactivo."""
    print("\n🩺 DIAGNÓSTICO DEL SISTEMA")
    print("-" * 35)
    
    duration = int(input("Duración del diagnóstico en segundos (default 30): ") or "30")
    
    try:
        print(f"\n🔍 Ejecutando diagnóstico...")
        exp_id = system.run_health_check(duration)
        print(f"✅ Diagnóstico iniciado: {exp_id}")
        
        # Esperar un poco y mostrar resultado
        time.sleep(duration + 5)
        status = system.get_experiment_status(exp_id)
        if status and status.get('results'):
            results = status['results']
            print(f"\n📊 Resultado del diagnóstico:")
            print(f"   Estado del sistema: {results.get('system_status', 'DESCONOCIDO')}")
            print(f"   Salud general: {results.get('overall_health', 0):.1f}%")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def generate_report_interactive(system: SimpleChaosSystem):
    """Genera reporte en modo interactivo."""
    print("\n📊 GENERAR REPORTE")
    print("-" * 25)
    
    try:
        print("🔄 Generando reporte...")
        report_path = system.generate_report()
        
        if report_path:
            print(f"✅ Reporte generado: {report_path}")
        else:
            print("❌ Error generando reporte")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def stop_all_experiments_interactive(system: SimpleChaosSystem):
    """Para todos los experimentos en modo interactivo."""
    print("\n🛑 PARAR TODOS LOS EXPERIMENTOS")
    print("-" * 35)
    
    try:
        if system.experiment_manager:
            system.experiment_manager.stop_all_experiments()
            print("✅ Todos los experimentos detenidos")
        else:
            print("❌ Gestor de experimentos no disponible")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Simulador simplificado de Chaos Engineering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python demo_chaos.py                    # Demo automática de 3 minutos
  python demo_chaos.py --duration 2       # Demo de 2 minutos
  python demo_chaos.py --interactive      # Modo interactivo
  python demo_chaos.py --verbose          # Logs detallados
        """
    )
    
    parser.add_argument(
        "--duration",
        type=int,
        default=3,
        help="Duración de la demo automática en minutos (1-4, default: 3)"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Ejecutar en modo interactivo"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostrar logs detallados (DEBUG)"
    )
    
    parser.add_argument(
        "--no-colors",
        action="store_true",
        help="Deshabilitar colores en logs"
    )
    
    args = parser.parse_args()
    
    # Validar duración
    if args.duration < 1 or args.duration > 4:
        print("❌ Error: La duración debe estar entre 1 y 4 minutos")
        sys.exit(1)
    
    # Configurar logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level, colors=not args.no_colors)
    
    # Mostrar banner
    print_banner()
    print(f"🕐 Inicio: {format_timestamp()}")
    
    try:
        if args.interactive:
            run_interactive_mode()
        else:
            success = run_automatic_demo(args.duration)
            if not success:
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️ Programa interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("🎉 SIMULACIÓN COMPLETADA")
    print("="*70)
    print("✅ Gracias por usar el Simulador de Chaos Engineering")
    print("📋 Revisa los reportes en el directorio ./reports/")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
