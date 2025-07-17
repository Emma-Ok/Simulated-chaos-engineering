"""
Interfaz de menús para el simulador de Chaos Engineering.
Proporciona una navegación fácil e intuitiva para todas las funcionalidades.
"""

import os
import sys
import time
from typing import Dict, List, Optional, Any
import logging

# Añadir el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chaos_system import ChaosEngineeringSystem
from utils.helpers import setup_colored_logging

logger = logging.getLogger(__name__)

class MenuInterface:
    """Interfaz principal de menús para el simulador de Chaos Engineering"""
    
    def __init__(self):
        self.system: Optional[ChaosEngineeringSystem] = None
        self.system_running = False
        self.current_config = None
        
        # Configurar logging silencioso para la interfaz
        setup_colored_logging("WARNING")
    
    def run(self):
        """Ejecuta la interfaz principal"""
        self.clear_screen()
        self.show_welcome()
        
        while True:
            try:
                choice = self.show_main_menu()
                
                if choice == '1':
                    self.quick_start_menu()
                elif choice == '2':
                    self.system_management_menu()
                elif choice == '3':
                    self.experiment_menu()
                elif choice == '4':
                    self.monitoring_menu()
                elif choice == '5':
                    self.configuration_menu()
                elif choice == '6':
                    self.examples_menu()
                elif choice == '7':
                    self.help_menu()
                elif choice == '0':
                    if self.confirm_exit():
                        break
                else:
                    self.show_error("Opción inválida. Intenta de nuevo.")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ Interrupción detectada...")
                if self.confirm_exit():
                    break
            except Exception as e:
                self.show_error(f"Error inesperado: {e}")
                time.sleep(2)
        
        self.cleanup_and_exit()
    
    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self):
        """Muestra el mensaje de bienvenida"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🔥 SIMULADOR DE CHAOS ENGINEERING 🔥                      ║
║                                                                              ║
║              Simula fallas en sistemas distribuidos para mejorar             ║
║                        la resiliencia y robustez                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
    
    def show_main_menu(self) -> str:
        """Muestra el menú principal y retorna la opción seleccionada"""
        status = "🟢 FUNCIONANDO" if self.system_running else "🔴 DETENIDO"
        services_count = len(self.system.services) if self.system else 0
        
        print(f"""
┌─────────────────── MENÚ PRINCIPAL ───────────────────┐
│                                                      │
│  Estado del Sistema: {status}                │
│  Servicios configurados: {services_count}                           │
│                                                      │
│  🚀 1. Inicio Rápido                                │
│  🔧 2. Gestión del Sistema                          │
│  🧪 3. Experimentos de Chaos                        │
│  📊 4. Monitoreo y Métricas                         │
│  ⚙️  5. Configuración                               │
│  📚 6. Ejemplos y Tutoriales                        │
│  ❓ 7. Ayuda                                        │
│                                                      │
│  🚪 0. Salir                                        │
│                                                      │
└──────────────────────────────────────────────────────┘
        """)
        
        return input("Selecciona una opción: ").strip()
    
    def quick_start_menu(self):
        """Menú de inicio rápido"""
        self.clear_screen()
        print("""
┌─────────────────── INICIO RÁPIDO ────────────────────┐
│                                                      │
│  🎯 1. Demo de 5 minutos                            │
│  🎮 2. Simulación interactiva                       │
│  ⚡ 3. Experimento básico                           │
│  🏗️  4. Configurar sistema desde cero               │
│                                                      │
│  ← 0. Volver al menú principal                      │
│                                                      │
└──────────────────────────────────────────────────────┘
        """)
        
        choice = input("Selecciona una opción: ").strip()
        
        if choice == '1':
            self.run_quick_demo()
        elif choice == '2':
            self.run_interactive_simulation()
        elif choice == '3':
            self.run_basic_experiment()
        elif choice == '4':
            self.setup_system_from_scratch()
        elif choice == '0':
            return
        else:
            self.show_error("Opción inválida")
    
    def system_management_menu(self):
        """Menú de gestión del sistema"""
        while True:
            self.clear_screen()
            print("""
┌─────────────── GESTIÓN DEL SISTEMA ──────────────────┐
│                                                      │
│  🔄 1. Iniciar/Reiniciar Sistema                    │
│  ⏹️  2. Detener Sistema                             │
│  🏗️  3. Agregar Servicio                           │
│  🗑️  4. Remover Servicio                           │
│  👀 5. Ver Estado del Sistema                       │
│  🔧 6. Configurar Load Balancer                     │
│  📊 7. Ver Métricas en Tiempo Real                  │
│                                                      │
│  ← 0. Volver al menú principal                      │
│                                                      │
└──────────────────────────────────────────────────────┘
            """)
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self.start_restart_system()
            elif choice == '2':
                self.stop_system()
            elif choice == '3':
                self.add_service_interactive()
            elif choice == '4':
                self.remove_service_interactive()
            elif choice == '5':
                self.show_system_status()
            elif choice == '6':
                self.configure_load_balancer()
            elif choice == '7':
                self.show_real_time_metrics()
            elif choice == '0':
                break
            else:
                self.show_error("Opción inválida")
    
    def experiment_menu(self):
        """Menú de experimentos de chaos"""
        while True:
            self.clear_screen()
            print("""
┌─────────────── EXPERIMENTOS DE CHAOS ────────────────┐
│                                                      │
│  🐒 1. Chaos Monkey (Terminación de instancias)     │
│  🌐 2. Experimento de Latencia                      │
│  💾 3. Agotamiento de Recursos                      │
│  🔌 4. Partición de Red                             │
│  🦍 5. Chaos Gorilla (Falla de zona)               │
│  🏢 6. Chaos Kong (Falla regional)                 │
│  🩺 7. Doctor Monkey (Diagnóstico)                 │
│  📋 8. Ver Experimentos Activos                     │
│  ⏹️  9. Detener Todos los Experimentos              │
│                                                      │
│  ← 0. Volver al menú principal                      │
│                                                      │
└──────────────────────────────────────────────────────┘
            """)
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self.run_chaos_monkey()
            elif choice == '2':
                self.run_latency_experiment()
            elif choice == '3':
                self.run_resource_experiment()
            elif choice == '4':
                print("🔌 Partición de red - Funcionalidad no implementada")
                self.wait_for_user()
            elif choice == '5':
                print("🦍 Chaos Gorilla - Funcionalidad no implementada")
                self.wait_for_user()
            elif choice == '6':
                print("🏢 Chaos Kong - Funcionalidad no implementada")
                self.wait_for_user()
            elif choice == '7':
                print("🩺 Doctor Monkey - Funcionalidad no implementada")
                self.wait_for_user()
            elif choice == '8':
                self.show_active_experiments()
            elif choice == '9':
                self.stop_all_experiments()
            elif choice == '0':
                break
            else:
                self.show_error("Opción inválida")
    
    def monitoring_menu(self):
        """Menú de monitoreo"""
        while True:
            self.clear_screen()
            print("""
┌─────────────── MONITOREO Y MÉTRICAS ─────────────────┐
│                                                      │
│  📊 1. Dashboard en Tiempo Real                     │
│  📈 2. Historial de Métricas                        │
│  🚨 3. Alertas Activas                              │
│  📋 4. Generar Reporte HTML                         │
│  💾 5. Exportar Métricas (JSON)                     │
│  📊 6. Gráficos de Performance                      │
│  🏥 7. Reporte de Salud del Sistema                 │
│                                                      │
│  ← 0. Volver al menú principal                      │
│                                                      │
└──────────────────────────────────────────────────────┘
            """)
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self.show_realtime_dashboard()
            elif choice == '2':
                self.show_metrics_history()
            elif choice == '3':
                self.show_active_alerts()
            elif choice == '4':
                self.generate_html_report()
            elif choice == '5':
                self.export_metrics()
            elif choice == '6':
                self.show_performance_charts()
            elif choice == '7':
                self.show_health_report()
            elif choice == '0':
                break
            else:
                self.show_error("Opción inválida")
    
    def configuration_menu(self):
        """Menú de configuración"""
        while True:
            self.clear_screen()
            print("""
┌─────────────────── CONFIGURACIÓN ────────────────────┐
│                                                      │
│  ⚙️  1. Configuración General                       │
│  🐒 2. Configurar Chaos Monkey                      │
│  🔔 3. Configurar Alertas                           │
│  🔧 4. Patrones de Resiliencia                      │
│  📁 5. Cargar Configuración desde Archivo           │
│  💾 6. Guardar Configuración Actual                 │
│  🔄 7. Restaurar Configuración por Defecto          │
│                                                      │
│  ← 0. Volver al menú principal                      │
│                                                      │
└──────────────────────────────────────────────────────┘
            """)
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self.general_configuration()
            elif choice == '2':
                print("🐒 Configurar Chaos Monkey - Funcionalidad no implementada")
                self.wait_for_user()
            elif choice == '3':
                print("🔔 Configurar alertas - Funcionalidad no implementada")
                self.wait_for_user()
            elif choice == '4':
                print("🔧 Patrones de resiliencia - Funcionalidad no implementada")
                self.wait_for_user()
            elif choice == '5':
                print("📁 Cargar configuración - Funcionalidad no implementada")
                self.wait_for_user()
            elif choice == '6':
                print("💾 Guardar configuración - Funcionalidad no implementada")
                self.wait_for_user()
            elif choice == '7':
                print("🔄 Restaurar configuración - Funcionalidad no implementada")
                self.wait_for_user()
            elif choice == '0':
                break
            else:
                self.show_error("Opción inválida")
    
    def examples_menu(self):
        """Menú de ejemplos y tutoriales"""
        while True:
            self.clear_screen()
            print("""
┌─────────────── EJEMPLOS Y TUTORIALES ────────────────┐
│                                                      │
│  📚 1. Tutorial: Conceptos Básicos                  │
│  🎮 2. Ejecutar Quick Start                         │
│  🏗️  3. Simulación Básica                          │
│  🧪 4. Experimentos Avanzados                       │
│  📊 5. Dashboard de Monitoreo                       │
│  ⚙️  6. Configuración con YAML                      │
│  📖 7. Ver Documentación                            │
│                                                      │
│  ← 0. Volver al menú principal                      │
│                                                      │
└──────────────────────────────────────────────────────┘
            """)
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self.show_basic_concepts()
            elif choice == '2':
                self.run_example_quick_start()
            elif choice == '3':
                self.run_example_basic_simulation()
            elif choice == '4':
                self.run_example_advanced_experiments()
            elif choice == '5':
                self.run_example_monitoring_dashboard()
            elif choice == '6':
                self.run_example_configuration()
            elif choice == '7':
                self.show_documentation()
            elif choice == '0':
                break
            else:
                self.show_error("Opción inválida")
    
    def help_menu(self):
        """Menú de ayuda"""
        while True:
            self.clear_screen()
            print("""
┌──────────────────────── AYUDA ───────────────────────┐
│                                                      │
│  ❓ 1. ¿Qué es Chaos Engineering?                   │
│  🎯 2. Conceptos Fundamentales                      │
│  🔧 3. Guía de Uso de la Interfaz                   │
│  🧪 4. Tipos de Experimentos                        │
│  📊 5. Interpretación de Métricas                   │
│  🛠️  6. Solución de Problemas                       │
│  📞 7. Soporte y Contacto                           │
│                                                      │
│  ← 0. Volver al menú principal                      │
│                                                      │
└──────────────────────────────────────────────────────┘
            """)
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self.explain_chaos_engineering()
            elif choice == '2':
                self.show_fundamental_concepts()
            elif choice == '3':
                self.show_interface_guide()
            elif choice == '4':
                self.explain_experiment_types()
            elif choice == '5':
                self.explain_metrics()
            elif choice == '6':
                self.show_troubleshooting()
            elif choice == '7':
                self.show_support_info()
            elif choice == '0':
                break
            else:
                self.show_error("Opción inválida")
    
    # Implementaciones de funciones específicas
    
    def ensure_system_exists(self):
        """Asegura que el sistema esté inicializado"""
        if not self.system:
            self.system = ChaosEngineeringSystem()
            print("✅ Sistema inicializado")
    
    def run_quick_demo(self):
        """Ejecuta la demostración rápida"""
        self.clear_screen()
        print("🚀 Iniciando demostración rápida...")
        print("Esto tomará aproximadamente 5 minutos\n")
        
        if self.confirm_action("¿Deseas continuar?"):
            try:
                # Importar y ejecutar el main con modo demo
                import subprocess
                result = subprocess.run([sys.executable, "main.py", "--demo"], 
                                      capture_output=False, text=True)
                
                if result.returncode == 0:
                    print("\n✅ Demostración completada exitosamente!")
                else:
                    print("\n❌ Error en la demostración")
                    
            except Exception as e:
                self.show_error(f"Error ejecutando demo: {e}")
            
            self.wait_for_user()
    
    def start_restart_system(self):
        """Inicia o reinicia el sistema"""
        self.clear_screen()
        
        if self.system_running:
            print("⚠️ El sistema ya está funcionando")
            if self.confirm_action("¿Deseas reiniciarlo?"):
                self.stop_system()
                time.sleep(1)
            else:
                return
        
        self.ensure_system_exists()
        
        print("🔄 Configurando servicios por defecto...")
        
        # Agregar servicios por defecto si no existen
        if not self.system.services:
            default_services = [
                ("api-gateway", "api-gateway", 3),
                ("auth-service", "auth-service", 2), 
                ("user-service", "user-profile", 2),
                ("db-service", "database", 2)
            ]
            
            for name, service_type, instances in default_services:
                self.system.add_service(name, service_type, instances)
                print(f"  ✅ {name} agregado ({instances} instancias)")
        
        print("\n🚀 Iniciando sistema...")
        self.system.start()
        self.system_running = True
        
        print("✅ Sistema iniciado exitosamente!")
        self.wait_for_user()
    
    def show_system_status(self):
        """Muestra el estado actual del sistema"""
        self.clear_screen()
        
        if not self.system or not self.system_running:
            print("❌ El sistema no está funcionando")
            self.wait_for_user()
            return
        
        print("📊 ESTADO DEL SISTEMA")
        print("=" * 50)
        
        status = self.system.get_system_status()
        
        print(f"🔄 Estado: {'🟢 Funcionando' if status['is_running'] else '🔴 Detenido'}")
        print(f"⏱️ Tiempo activo: {self.format_duration(status['uptime_seconds'])}")
        print(f"🏗️ Servicios: {len(status['services'])}")
        
        print("\n📋 SERVICIOS:")
        print("-" * 50)
        
        for service_name, service_data in status['services'].items():
            health_status = "🟢" if service_data['availability'] > 90 else "🟡" if service_data['availability'] > 50 else "🔴"
            print(f"{health_status} {service_name}")
            print(f"   Instancias: {service_data['healthy_instances']}/{service_data['total_instances']}")
            print(f"   Disponibilidad: {service_data['availability']:.1f}%")
            print(f"   Tiempo respuesta: {service_data['avg_response_time_ms']:.1f}ms")
            print(f"   Tasa de error: {service_data['error_rate']:.2f}%")
            print()
        
        self.wait_for_user()
    
    def run_chaos_monkey(self):
        """Ejecuta Chaos Monkey interactivamente"""
        self.clear_screen()
        
        if not self.system or not self.system_running:
            print("❌ El sistema debe estar funcionando para ejecutar experimentos")
            self.wait_for_user()
            return
        
        print("🐒 CHAOS MONKEY")
        print("=" * 30)
        
        services = list(self.system.services.keys())
        if not services:
            print("❌ No hay servicios configurados")
            self.wait_for_user()
            return
        
        print("Servicios disponibles:")
        for i, service in enumerate(services, 1):
            print(f"  {i}. {service}")
        print(f"  {len(services)+1}. Aleatorio")
        
        try:
            choice = input("\nSelecciona servicio (número): ").strip()
            
            if choice.isdigit():
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(services):
                    target_service = services[choice_idx]
                elif choice_idx == len(services):
                    target_service = None
                else:
                    self.show_error("Selección inválida")
                    return
            else:
                self.show_error("Entrada inválida")
                return
            
            print(f"\n🔥 Ejecutando Chaos Monkey en {target_service or 'servicio aleatorio'}...")
            result = self.system.force_chaos_monkey(target_service)
            
            if result['status'] == 'success':
                print(f"✅ Instancia terminada: {result['service_name']}/{result['instance_id']}")
            else:
                print(f"🛡️ {result['message']}")
                
        except Exception as e:
            self.show_error(f"Error: {e}")
        
        self.wait_for_user()
    
    def generate_html_report(self):
        """Genera un reporte HTML"""
        self.clear_screen()
        
        if not self.system:
            print("❌ El sistema debe estar inicializado")
            self.wait_for_user()
            return
        
        print("📄 Generando reporte HTML...")
        
        try:
            report_files = self.system.generate_report(formats=["html"])
            html_file = report_files.get('html', 'No disponible')
            
            print(f"✅ Reporte generado exitosamente!")
            print(f"📁 Archivo: {html_file}")
            print(f"🌐 Abre el archivo en tu navegador para ver el reporte completo")
            
        except Exception as e:
            self.show_error(f"Error generando reporte: {e}")
        
        self.wait_for_user()
    
    def show_active_experiments(self):
        """Muestra los experimentos activos"""
        self.clear_screen()
        
        if not self.system or not hasattr(self.system, 'experiment_runner'):
            print("❌ Sistema no inicializado o sin runner de experimentos")
            self.wait_for_user()
            return
        
        print("🧪 EXPERIMENTOS ACTIVOS")
        print("=" * 40)
        
        try:
            experiments = self.system.experiment_runner.get_all_experiments_status()
            
            if not experiments:
                print("ℹ️ No hay experimentos activos")
            else:
                for exp_id, exp_data in experiments.items():
                    status_icon = "🟢" if exp_data['status'] == 'running' else "🔴"
                    print(f"{status_icon} {exp_data['name']}")
                    print(f"   Tipo: {exp_data['type']}")
                    print(f"   Estado: {exp_data['status']}")
                    print(f"   Servicio objetivo: {exp_data.get('target_service', 'N/A')}")
                    print()
                    
        except Exception as e:
            self.show_error(f"Error obteniendo experimentos: {e}")
        
        self.wait_for_user()
    
    # Funciones de utilidad
    
    def show_error(self, message: str):
        """Muestra un mensaje de error"""
        print(f"\n❌ Error: {message}")
        time.sleep(2)
    
    def show_success(self, message: str):
        """Muestra un mensaje de éxito"""
        print(f"\n✅ {message}")
    
    def confirm_action(self, message: str) -> bool:
        """Pide confirmación al usuario"""
        response = input(f"\n{message} (s/N): ").strip().lower()
        return response in ['s', 'sí', 'si', 'y', 'yes']
    
    def confirm_exit(self) -> bool:
        """Confirma si el usuario quiere salir"""
        return self.confirm_action("¿Estás seguro que deseas salir?")
    
    def wait_for_user(self):
        """Espera a que el usuario presione Enter"""
        input("\nPresiona Enter para continuar...")
    
    def format_duration(self, seconds: float) -> str:
        """Formatea una duración en segundos"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
    
    def cleanup_and_exit(self):
        """Limpia recursos y sale de la aplicación"""
        print("\n🧹 Limpiando recursos...")
        
        if self.system and self.system_running:
            self.system.stop()
        
        print("👋 ¡Gracias por usar el Simulador de Chaos Engineering!")
        print("🔗 Visita nuestro repositorio para más información")
        sys.exit(0)
    
    # Stubs para funciones que necesitan implementación completa
    def run_interactive_simulation(self):
        """Ejecuta una simulación interactiva paso a paso"""
        self.clear_screen()
        print("🎮 SIMULACIÓN INTERACTIVA")
        print("=" * 40)
        
        if not self.confirm_action("¿Deseas iniciar una simulación interactiva guiada?"):
            return
        
        # Paso 1: Configurar sistema
        self.ensure_system_exists()
        if not self.system_running:
            print("\n🔄 Paso 1: Iniciando sistema...")
            self.start_restart_system()
        
        # Paso 2: Mostrar estado inicial
        print("\n📊 Paso 2: Estado inicial del sistema")
        self.show_system_status()
        
        # Paso 3: Ejecutar experimento
        print("\n🧪 Paso 3: ¿Deseas ejecutar un experimento?")
        if self.confirm_action("Ejecutar Chaos Monkey"):
            self.run_chaos_monkey()
        
        # Paso 4: Ver resultados
        print("\n📈 Paso 4: Generando reporte...")
        self.generate_html_report()
        
        print("\n✅ Simulación interactiva completada!")
        self.wait_for_user()
    
    def run_basic_experiment(self):
        """Ejecuta un experimento básico paso a paso"""
        self.clear_screen()
        print("⚡ EXPERIMENTO BÁSICO")
        print("=" * 30)
        
        if not self.system or not self.system_running:
            print("❌ El sistema debe estar funcionando para ejecutar experimentos")
            if self.confirm_action("¿Deseas iniciar el sistema ahora?"):
                self.start_restart_system()
            else:
                return
        
        print("\nExperimentos disponibles:")
        print("1. 🐒 Chaos Monkey (Recomendado para empezar)")
        print("2. 🌐 Experimento de Latencia") 
        print("3. 💾 Agotamiento de Recursos")
        
        choice = input("\nSelecciona experimento (1-3): ").strip()
        
        if choice == '1':
            self.run_chaos_monkey()
        elif choice == '2':
            self.run_latency_experiment_basic()
        elif choice == '3':
            self.run_resource_experiment_basic()
        else:
            self.show_error("Opción inválida")
    
    def setup_system_from_scratch(self):
        """Configura el sistema completamente desde cero"""
        self.clear_screen()
        print("🏗️ CONFIGURACIÓN DESDE CERO")
        print("=" * 40)
        
        if self.system:
            print("⚠️ Ya existe un sistema configurado")
            if not self.confirm_action("¿Deseas reiniciar desde cero?"):
                return
        
        # Crear nuevo sistema
        self.system = ChaosEngineeringSystem()
        print("✅ Sistema base creado")
        
        # Configurar servicios
        print("\n🏗️ Configurando servicios...")
        self.add_services_wizard()
        
        # Iniciar sistema
        print("\n🚀 Iniciando sistema...")
        self.system.start()
        self.system_running = True
        
        print("✅ Sistema configurado y iniciado exitosamente!")
        self.wait_for_user()
    
    def add_services_wizard(self):
        """Asistente para agregar servicios"""
        print("\n📝 Asistente de servicios:")
        print("Configuremos algunos servicios básicos\n")
        
        default_services = [
            ("api-gateway", "api-gateway", "Puerta de entrada principal"),
            ("auth-service", "auth-service", "Servicio de autenticación"),
            ("user-service", "user-profile", "Gestión de usuarios"),
            ("db-service", "database", "Base de datos principal")
        ]
        
        for name, service_type, description in default_services:
            print(f"🔧 {name}: {description}")
            if self.confirm_action(f"¿Agregar {name}?"):
                instances = self.get_number_input("Número de instancias (2-5)", 2, 5, 3)
                self.system.add_service(name, service_type, instances)
                print(f"  ✅ {name} agregado con {instances} instancias")
            print()
    
    def get_number_input(self, prompt: str, min_val: int, max_val: int, default: int) -> int:
        """Obtiene un número del usuario con validación"""
        while True:
            try:
                response = input(f"{prompt} (default {default}): ").strip()
                if not response:
                    return default
                
                value = int(response)
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"❌ Valor debe estar entre {min_val} y {max_val}")
            except ValueError:
                print("❌ Por favor ingresa un número válido")
    
    def stop_system(self):
        if self.system and self.system_running:
            self.system.stop()
            self.system_running = False
            print("⏹️ Sistema detenido")
        else:
            print("ℹ️ El sistema ya está detenido")
        self.wait_for_user()
    
    def add_service_interactive(self):
        """Agrega un servicio de forma interactiva"""
        self.clear_screen()
        print("🏗️ AGREGAR SERVICIO")
        print("=" * 25)
        
        if not self.system:
            self.ensure_system_exists()
        
        print("Tipos de servicios disponibles:")
        service_types = [
            ("api-gateway", "Puerta de entrada principal"),
            ("auth-service", "Servicio de autenticación"),
            ("user-profile", "Gestión de perfiles de usuario"),
            ("database", "Base de datos"),
            ("cache", "Sistema de caché"),
            ("notification", "Servicio de notificaciones"),
            ("payment", "Procesamiento de pagos")
        ]
        
        for i, (service_type, description) in enumerate(service_types, 1):
            print(f"  {i}. {service_type}: {description}")
        
        try:
            choice = int(input("\nSelecciona tipo (1-7): ").strip()) - 1
            if not (0 <= choice < len(service_types)):
                self.show_error("Selección inválida")
                return
            
            service_type, description = service_types[choice]
            service_name = input(f"Nombre del servicio (default: {service_type}): ").strip() or service_type
            instances = self.get_number_input("Número de instancias", 1, 10, 2)
            
            self.system.add_service(service_name, service_type, instances)
            print(f"\n✅ Servicio '{service_name}' agregado con {instances} instancias")
            
        except ValueError:
            self.show_error("Entrada inválida")
        except Exception as e:
            self.show_error(f"Error agregando servicio: {e}")
        
        self.wait_for_user()
    
    def remove_service_interactive(self):
        """Remueve un servicio de forma interactiva"""
        self.clear_screen()
        print("🗑️ REMOVER SERVICIO")
        print("=" * 25)
        
        if not self.system or not self.system.services:
            print("❌ No hay servicios configurados")
            self.wait_for_user()
            return
        
        services = list(self.system.services.keys())
        print("Servicios disponibles:")
        
        for i, service_name in enumerate(services, 1):
            print(f"  {i}. {service_name}")
        
        try:
            choice = int(input("\nSelecciona servicio a remover (número): ").strip()) - 1
            if not (0 <= choice < len(services)):
                self.show_error("Selección inválida")
                return
            
            service_name = services[choice]
            
            if self.confirm_action(f"¿Estás seguro de remover '{service_name}'?"):
                # Aquí necesitaríamos implementar remove_service en ChaosEngineeringSystem
                if hasattr(self.system, 'remove_service'):
                    self.system.remove_service(service_name)
                else:
                    # Workaround: remover del diccionario directamente
                    del self.system.services[service_name]
                
                print(f"✅ Servicio '{service_name}' removido")
            
        except ValueError:
            self.show_error("Entrada inválida")
        except Exception as e:
            self.show_error(f"Error removiendo servicio: {e}")
        
        self.wait_for_user()
    
    def configure_load_balancer(self):
        print("🔧 Configurar Load Balancer - En desarrollo")
        self.wait_for_user()
    
    def show_real_time_metrics(self):
        """Muestra métricas en tiempo real"""
        self.clear_screen()
        print("📊 MÉTRICAS EN TIEMPO REAL")
        print("=" * 35)
        
        if not self.system or not self.system_running:
            print("❌ El sistema debe estar funcionando")
            self.wait_for_user()
            return
        
        print("⏱️ Actualizando cada 5 segundos... (Ctrl+C para salir)")
        print()
        
        try:
            import time
            while True:
                self.clear_screen()
                print("📊 MÉTRICAS EN TIEMPO REAL - " + time.strftime("%H:%M:%S"))
                print("=" * 50)
                
                # Mostrar estado general
                status = self.system.get_system_status()
                print(f"🔄 Sistema: {'🟢 FUNCIONANDO' if status['is_running'] else '🔴 DETENIDO'}")
                print(f"⏱️ Uptime: {self.format_duration(status['uptime_seconds'])}")
                print(f"🏗️ Servicios: {len(status['services'])}")
                print()
                
                # Métricas por servicio con formato mejorado
                print("📋 SERVICIOS:")
                print("-" * 70)
                
                for service_name, service_data in status['services'].items():
                    health_icon = "🟢" if service_data['availability'] > 90 else "🟡" if service_data['availability'] > 50 else "🔴"
                    
                    # Información básica del servicio
                    print(f"{health_icon} {service_name.upper()}")
                    print(f"   📊 Disponibilidad: {service_data['availability']:.1f}%")
                    print(f"   ⏱️ Tiempo Respuesta: {service_data['avg_response_time_ms']:.2f}ms")
                    print(f"   ❌ Tasa de Error: {service_data['error_rate']:.3f}%")
                    print(f"   📈 Requests Totales: {service_data.get('total_requests', 0)}")
                    print(f"   ✅ Requests Exitosos: {service_data.get('successful_requests', 0)}")
                    print(f"   🔧 Instancias: {service_data['healthy_instances']}/{service_data['total_instances']}")
                    
                    # Mostrar detalle de instancias si hay espacio
                    instances = service_data.get('instances', {})
                    if instances and len(instances) <= 6:  # Solo si no son demasiadas
                        print(f"   📱 Detalle de Instancias:")
                        for inst_id, inst_data in instances.items():
                            status_icon = "🟢" if inst_data['status'] == 'HEALTHY' else "🟡" if inst_data['status'] == 'DEGRADED' else "🔴"
                            metrics = inst_data['metrics']
                            print(f"      {status_icon} {inst_id}: "
                                 f"CPU {metrics['cpu_usage']:.0f}% | "
                                 f"RAM {metrics['memory_usage']:.0f}% | "
                                 f"RT {metrics['response_time_ms']:.1f}ms")
                    
                    print()  # Línea en blanco entre servicios
                
                print("💡 Presiona Ctrl+C para volver al menú")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\n✅ Saliendo de métricas en tiempo real...")
            self.wait_for_user()
    
    def run_latency_experiment(self):
        """Ejecuta un experimento de latencia avanzado"""
        self.clear_screen()
        print("🌐 EXPERIMENTO DE LATENCIA")
        print("=" * 35)
        
        if not self.system or not self.system_running:
            print("❌ El sistema debe estar funcionando")
            self.wait_for_user()
            return
        
        services = list(self.system.services.keys())
        if not services:
            print("❌ No hay servicios configurados")
            self.wait_for_user()
            return
        
        print("Servicios disponibles:")
        for i, service in enumerate(services, 1):
            print(f"  {i}. {service}")
        
        try:
            choice = int(input("\nSelecciona servicio (número): ").strip()) - 1
            if not (0 <= choice < len(services)):
                self.show_error("Selección inválida")
                return
            
            target_service = services[choice]
            latency_ms = self.get_number_input("Latencia a introducir (ms)", 100, 5000, 500)
            duration_s = self.get_number_input("Duración del experimento (segundos)", 30, 600, 120)
            
            print(f"\n🔬 Ejecutando experimento de latencia:")
            print(f"   Servicio: {target_service}")
            print(f"   Latencia: {latency_ms}ms")
            print(f"   Duración: {duration_s}s")
            
            if hasattr(self.system, 'run_chaos_experiment'):
                exp_id = self.system.run_chaos_experiment(
                    "latency",
                    name="interactive-latency",
                    target_service=target_service,
                    latency_ms=latency_ms,
                    duration_seconds=duration_s
                )
                print(f"✅ Experimento iniciado: {exp_id}")
                print("   El experimento se ejecutará en segundo plano")
            else:
                # Fallback: usar método directo en el servicio
                service = self.system.services[target_service]
                service.chaos_introduce_latency(latency_ms)
                print(f"✅ Latencia de {latency_ms}ms aplicada a {target_service}")
                
        except ValueError:
            self.show_error("Entrada inválida")
        except Exception as e:
            self.show_error(f"Error en experimento: {e}")
        
        self.wait_for_user()
    
    def run_latency_experiment_basic(self):
        """Versión simplificada del experimento de latencia"""
        services = list(self.system.services.keys())
        if not services:
            print("❌ No hay servicios disponibles")
            return
        
        target_service = services[0]  # Usar el primer servicio
        print(f"🌐 Aplicando latencia de 800ms a {target_service}...")
        
        try:
            if hasattr(self.system, 'run_chaos_experiment'):
                exp_id = self.system.run_chaos_experiment(
                    "latency",
                    name="basic-latency",
                    target_service=target_service,
                    latency_ms=800,
                    duration_seconds=60
                )
                print(f"✅ Experimento iniciado: {exp_id}")
            else:
                service = self.system.services[target_service]
                service.chaos_introduce_latency(800)
                print("✅ Latencia aplicada exitosamente")
        except Exception as e:
            self.show_error(f"Error: {e}")
    
    def run_resource_experiment(self):
        """Ejecuta un experimento de agotamiento de recursos"""
        self.clear_screen()
        print("💾 EXPERIMENTO DE RECURSOS")
        print("=" * 35)
        
        if not self.system or not self.system_running:
            print("❌ El sistema debe estar funcionando")
            self.wait_for_user()
            return
        
        services = list(self.system.services.keys())
        if not services:
            print("❌ No hay servicios configurados")
            self.wait_for_user()
            return
        
        print("Servicios disponibles:")
        for i, service in enumerate(services, 1):
            print(f"  {i}. {service}")
        
        print("\nTipos de recurso:")
        print("  1. CPU")
        print("  2. Memoria")
        
        try:
            service_choice = int(input("\nSelecciona servicio (número): ").strip()) - 1
            resource_choice = int(input("Selecciona recurso (1-2): ").strip())
            
            if not (0 <= service_choice < len(services)):
                self.show_error("Selección de servicio inválida")
                return
            
            if resource_choice not in [1, 2]:
                self.show_error("Selección de recurso inválida")
                return
            
            target_service = services[service_choice]
            resource_type = "cpu" if resource_choice == 1 else "memory"
            exhaustion_level = self.get_number_input("Nivel de agotamiento (%)", 70, 95, 90) / 100
            duration_s = self.get_number_input("Duración (segundos)", 30, 300, 90)
            
            print(f"\n💥 Ejecutando experimento de recursos:")
            print(f"   Servicio: {target_service}")
            print(f"   Recurso: {resource_type.upper()}")
            print(f"   Nivel: {exhaustion_level*100:.0f}%")
            print(f"   Duración: {duration_s}s")
            
            if hasattr(self.system, 'run_chaos_experiment'):
                exp_id = self.system.run_chaos_experiment(
                    "resource_exhaustion",
                    name="interactive-resources",
                    target_service=target_service,
                    resource_type=resource_type,
                    exhaustion_level=exhaustion_level,
                    duration_seconds=duration_s
                )
                print(f"✅ Experimento iniciado: {exp_id}")
            else:
                print("✅ Experimento simulado (funcionalidad completa en desarrollo)")
                
        except ValueError:
            self.show_error("Entrada inválida")
        except Exception as e:
            self.show_error(f"Error: {e}")
        
        self.wait_for_user()
    
    def run_resource_experiment_basic(self):
        """Versión simplificada del experimento de recursos"""
        services = list(self.system.services.keys())
        if not services:
            print("❌ No hay servicios disponibles")
            return
        
        target_service = services[0]
        print(f"💾 Aplicando agotamiento de CPU (90%) a {target_service}...")
        
        try:
            if hasattr(self.system, 'run_chaos_experiment'):
                exp_id = self.system.run_chaos_experiment(
                    "resource_exhaustion",
                    name="basic-resources",
                    target_service=target_service,
                    resource_type="cpu",
                    exhaustion_level=0.9,
                    duration_seconds=60
                )
                print(f"✅ Experimento iniciado: {exp_id}")
            else:
                print("✅ Experimento simulado (CPU al 90%)")
        except Exception as e:
            self.show_error(f"Error: {e}")
    
    # Removed stub functions that were not implemented
    
    def show_basic_concepts(self):
        print("""
📚 CONCEPTOS BÁSICOS DE CHAOS ENGINEERING

Chaos Engineering es la disciplina de experimentar en un sistema distribuido
para generar confianza en la capacidad del sistema de resistir condiciones
turbulentas en producción.

Principios fundamentales:
1. Construir una hipótesis sobre el comportamiento del estado estable
2. Variar eventos del mundo real
3. Ejecutar experimentos en producción
4. Automatizar experimentos para ejecutar continuamente
5. Minimizar el radio de explosión

Beneficios:
- Identifica debilidades antes de que afecten a usuarios
- Mejora la confianza en el sistema
- Reduce el tiempo de recuperación ante fallas
- Fomenta una cultura de resiliencia
        """)
        self.wait_for_user()
    
    def run_example_quick_start(self):
        print("📚 Ejecutando ejemplo quick_start.py...")
        try:
            import subprocess
            subprocess.run([sys.executable, "examples/quick_start.py"])
        except Exception as e:
            self.show_error(f"Error: {e}")
        self.wait_for_user()
    
    def run_example_basic_simulation(self):
        print("📚 Ejecutando ejemplo basic_simulation.py...")
        try:
            import subprocess
            subprocess.run([sys.executable, "examples/basic_simulation.py"])
        except Exception as e:
            self.show_error(f"Error: {e}")
        self.wait_for_user()
    
    def run_example_advanced_experiments(self):
        print("📚 Ejecutando ejemplo advanced_experiments.py...")
        try:
            import subprocess
            subprocess.run([sys.executable, "examples/advanced_experiments.py"])
        except Exception as e:
            self.show_error(f"Error: {e}")
        self.wait_for_user()
    
    def run_example_monitoring_dashboard(self):
        print("📚 Ejecutando ejemplo monitoring_dashboard.py...")
        try:
            import subprocess
            subprocess.run([sys.executable, "examples/monitoring_dashboard.py"])
        except Exception as e:
            self.show_error(f"Error: {e}")
        self.wait_for_user()
    
    def run_example_configuration(self):
        print("📚 Ejecutando ejemplo configuration_example.py...")
        try:
            import subprocess
            subprocess.run([sys.executable, "examples/configuration_example.py"])
        except Exception as e:
            self.show_error(f"Error: {e}")
        self.wait_for_user()
    
    def show_documentation(self):
        print("""
📖 DOCUMENTACIÓN

Archivos principales:
- README.md: Documentación general del proyecto
- examples/README.md: Guía de ejemplos
- PROJECT_COMPLETED.md: Estado del proyecto

Para documentación completa, revisa estos archivos en el proyecto.
        """)
        self.wait_for_user()
    
    def explain_chaos_engineering(self):
        print("""
❓ ¿QUÉ ES CHAOS ENGINEERING?

Chaos Engineering es una disciplina que consiste en experimentar con sistemas
distribuidos para descubrir debilidades antes de que se manifiesten como
comportamientos aberrantes en producción.

Historia:
- Originado en Netflix con "Chaos Monkey" (2010)
- Evolucionó para incluir múltiples tipos de fallas
- Adoptado por empresas como Amazon, Google, Facebook

Objetivos:
- Encontrar puntos únicos de falla
- Probar la efectividad de mecanismos de fallback
- Mejorar la resiliencia del sistema
- Generar confianza en la infraestructura
        """)
        self.wait_for_user()
    
    def show_fundamental_concepts(self):
        print("""
🎯 CONCEPTOS FUNDAMENTALES

1. ESTADO ESTABLE
   - Define el comportamiento "normal" del sistema
   - Métricas base: latencia, throughput, disponibilidad

2. HIPÓTESIS
   - "El sistema continuará funcionando normalmente cuando..."
   - Debe ser medible y verificable

3. VARIABLES DEL MUNDO REAL
   - Fallas de hardware
   - Problemas de red
   - Picos de tráfico
   - Dependencias externas

4. MINIMIZAR EL RADIO DE EXPLOSIÓN
   - Comenzar con experimentos pequeños
   - Incrementar gradualmente la complejidad
   - Tener mecanismos de parada de emergencia
        """)
        self.wait_for_user()
    
    def show_interface_guide(self):
        print("""
🔧 GUÍA DE USO DE LA INTERFAZ

NAVEGACIÓN:
- Usa números para seleccionar opciones
- 0 siempre regresa al menú anterior
- Ctrl+C para interrumpir (con confirmación)

FLUJO RECOMENDADO:
1. Inicio Rápido → Demo de 5 minutos
2. Gestión del Sistema → Iniciar Sistema
3. Experimentos → Chaos Monkey
4. Monitoreo → Dashboard en Tiempo Real
5. Configuración → según necesidades

CONSEJOS:
- Siempre inicia el sistema antes de ejecutar experimentos
- Revisa el estado del sistema regularmente
- Genera reportes para analizar resultados
- Usa los ejemplos para aprender
        """)
        self.wait_for_user()
    
    def explain_experiment_types(self):
        print("""
🧪 TIPOS DE EXPERIMENTOS

🐒 CHAOS MONKEY
   - Termina instancias aleatoriamente
   - Prueba la recuperación automática

🌐 LATENCY MONKEY
   - Introduce latencia en servicios
   - Simula redes lentas

💾 RESOURCE EXHAUSTION
   - Agota CPU o memoria
   - Prueba límites de recursos

🔌 NETWORK PARTITION
   - Simula problemas de conectividad
   - Prueba tolerancia a particiones

🦍 CHAOS GORILLA
   - Falla una zona completa
   - Prueba recuperación regional

🏢 CHAOS KONG
   - Falla una región completa
   - Prueba recuperación global

🩺 DOCTOR MONKEY
   - Diagnóstica salud del sistema
   - Identifica instancias problemáticas
        """)
        self.wait_for_user()
    
    def explain_metrics(self):
        print("""
📊 INTERPRETACIÓN DE MÉTRICAS

MÉTRICAS CLAVE:
📈 Latencia: Tiempo de respuesta de requests
📊 Throughput: Requests procesados por segundo
📉 Error Rate: Porcentaje de requests fallidas
🔄 Disponibilidad: Porcentaje de tiempo operativo
💾 Uso de Recursos: CPU y memoria utilizados

RANGOS SALUDABLES:
- Latencia: < 500ms (web), < 100ms (APIs)
- Error Rate: < 1% (normal), < 5% (aceptable)
- Disponibilidad: > 99% (crítico), > 95% (aceptable)
- CPU: < 70% (normal), < 85% (carga alta)
- Memoria: < 80% (normal), < 90% (crítico)

ALERTAS:
🟢 Verde: Todo normal
🟡 Amarillo: Precaución
🔴 Rojo: Acción requerida
        """)
        self.wait_for_user()
    
    def show_troubleshooting(self):
        print("""
🛠️ SOLUCIÓN DE PROBLEMAS

PROBLEMAS COMUNES:

❌ Sistema no inicia:
   - Verifica dependencias: pip install -r requirements.txt
   - Revisa logs de error
   - Comprueba permisos de archivos

❌ Experimentos fallan:
   - Asegúrate que el sistema esté iniciado
   - Verifica que haya servicios configurados
   - Revisa configuración de Chaos Monkey

❌ Reportes no se generan:
   - Verifica permisos de escritura en ./reports/
   - Asegúrate que el sistema tenga datos

❌ Performance lenta:
   - Reduce número de instancias
   - Ajusta intervalos de monitoreo
   - Cierra otros programas pesados

LOGS Y DEBUG:
- Aumenta log level a DEBUG en configuración
- Revisa archivos en ./reports/
- Usa modo --log-level DEBUG en CLI
        """)
        self.wait_for_user()
    
    def show_support_info(self):
        print("""
📞 SOPORTE Y CONTACTO

RECURSOS:
📖 Documentación: README.md
🎮 Ejemplos: carpeta /examples/
🔧 Configuración: config/chaos_config.yaml

COMUNIDAD:
- Este es un proyecto de demostración educativo
- Revisa la documentación para entender conceptos
- Experimenta con diferentes configuraciones

DESARROLLO:
- Basado en principios reales de Chaos Engineering
- Inspirado en herramientas como Chaos Monkey de Netflix
- Implementa patrones de resiliencia estándar

APRENDIZAJE:
📚 Libros recomendados:
- "Chaos Engineering" por Casey Rosenthal
- "Building Microservices" por Sam Newman
- "Site Reliability Engineering" por Google
        """)
        self.wait_for_user()


# Entry point moved to main.py - no longer needed here 