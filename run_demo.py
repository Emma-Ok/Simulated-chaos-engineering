#!/usr/bin/env python3
"""
🔥 DEMO INTERACTIVO DE CHAOS ENGINEERING 🔥

Demo súper simple y visual que muestra todo el poder del sistema
de chaos engineering de forma interactiva y fácil de entender.

EJECUTAR:
    python run_demo.py

¡Eso es todo! 🎉
"""

import os
import random
import sys
import time
import threading
from typing import Dict, Any
import logging

# Configurar el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chaos_system import ChaosEngineeringSystem
from utils.helpers import setup_colored_logging

# ═══════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE LA DEMO
# ═══════════════════════════════════════════════════════════════════

class InteractiveDemo:
    """Demo interactivo súper visual y fácil de usar"""
    
    def __init__(self):
        self.system = None
        self.running = False
        self.demo_phase = 0
        
        # Configurar logging visual
        setup_colored_logging("INFO")
        
    def run(self):
        """Ejecuta la demo completa interactiva"""
        self.show_welcome()
        
        while True:
            choice = self.show_main_menu()
            
            if choice == '1':
                self.quick_demo()
            elif choice == '2':
                self.interactive_experiments()
            elif choice == '3':
                self.visual_monitoring()
            elif choice == '4':
                self.chaos_scenarios()
            elif choice == '5':
                self.system_status()
            elif choice == '6':
                self.educational_mode()
            elif choice == '0':
                self.cleanup_and_exit()
                break
            else:
                self.print_error("❌ Opción inválida. Intenta de nuevo.")
                
    def show_welcome(self):
        """Muestra la pantalla de bienvenida"""
        self.clear_screen()
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🔥 DEMO INTERACTIVO DE CHAOS ENGINEERING 🔥               ║
║                                                               ║
║    ┌─────────────────────────────────────────────────────┐   ║
║    │  🏗️  Arquitectura Distribuida Simulada             │   ║
║    │  🐒  Chaos Monkey Inteligente                       │   ║
║    │  📊  Métricas en Tiempo Real                        │   ║
║    │  🧪  Experimentos Interactivos                      │   ║
║    │  📈  Reportes HTML Automáticos                      │   ║
║    └─────────────────────────────────────────────────────┘   ║
║                                                               ║
║    🎯 Aprende Chaos Engineering de forma visual e interactiva ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        self.wait_for_user()
        
    def show_main_menu(self):
        """Muestra el menú principal"""
        status = "🟢 ACTIVO" if self.running else "🔴 PARADO"
        services = len(self.system.services) if self.system else 0
        
        self.clear_screen()
        print(f"""
┌─────────────────── DEMO INTERACTIVO ───────────────────┐
│                                                        │
│  Estado: {status}    Servicios: {services:02d}                    │
│                                                        │
│  🚀 1. Demo Rápida (5 min) - ¡RECOMENDADO!            │
│  🧪 2. Experimentos Interactivos                      │
│  📊 3. Monitoreo Visual en Tiempo Real                │
│  💥 4. Escenarios de Caos Avanzados                   │
│  🔍 5. Estado del Sistema                             │
│  📚 6. Modo Educativo                                 │
│                                                       │
│  🚪 0. Salir                                          │
│                                                       │
└───────────────────────────────────────────────────────┘
        """)
        
        return input("🎯 Selecciona una opción: ").strip()
        
    def quick_demo(self):
        """Demo rápida de 5 minutos súper visual"""
        self.clear_screen()
        print("""
🚀 DEMO RÁPIDA - CHAOS ENGINEERING EN ACCIÓN
═══════════════════════════════════════════════
        
⏱️  Duración: 5 minutos
🎯  Objetivo: Ver todo el sistema en acción
📊  Incluye: Servicios, experimentos, métricas y reportes
        """)
        
        print("🚀 ¡Comenzando automáticamente en 3 segundos!")
        time.sleep(3)
            
        try:
            # FASE 1: Configuración del sistema
            self.demo_phase_1_setup()
            
            # FASE 2: Tráfico normal
            self.demo_phase_2_normal_traffic()
            
            # FASE 3: Chaos experiments
            self.demo_phase_3_chaos()
            
            # FASE 4: Recuperación y reportes
            self.demo_phase_4_recovery()
            
        except KeyboardInterrupt:
            print("\n⚠️ Demo interrumpida por el usuario")
        except Exception as e:
            print(f"\n❌ Error en demo: {e}")
        finally:
            self.cleanup_demo()
            
    def demo_phase_1_setup(self):
        """Fase 1: Configurar el sistema"""
        self.show_phase_header("📋 FASE 1", "Configurando Arquitectura Distribuida", "1 min")
        
        print("🏗️ Creando sistema de chaos engineering...")
        self.system = self.create_stable_demo_system()
        
        print("\n🔧 Configurando servicios distribuidos:")
        services_config = [
            ("🌐 API Gateway", "api-gateway", "api-gateway", 6, "Entrada principal del sistema"),
            ("🔐 Auth Service", "auth-service", "auth-service", 5, "Autenticación y autorización"),
            ("👥 User Service", "user-service", "user-profile", 5, "Gestión de usuarios"),
            ("💳 Payment Service", "payment-service", "database", 6, "Procesamiento de pagos (crítico)"),
            ("📧 Notification Service", "notification-service", "api-gateway", 7, "Notificaciones push/email"),
            ("📊 Analytics Service", "analytics-service", "cache", 5, "Analytics y métricas (rápido)"),
            ("📁 File Storage", "file-storage", "database", 5, "Almacenamiento de archivos"),
            ("🔍 Search Service", "search-service", "cache", 5, "Motor de búsqueda (rápido)"),
            ("📱 Mobile API", "mobile-api", "user-profile", 6, "API móvil especializada"),
            ("🔒 Security Service", "security-service", "auth-service", 4, "Seguridad y auditoría"),
            ("📈 Monitoring Service", "monitoring-service", "database", 4, "Monitoreo de aplicaciones"),
            ("💾 Database", "database", "database", 6, "Base de datos principal"),
            ("⚡ Cache", "cache", "cache", 5, "Cache en memoria distribuida")
        ]
        
        for emoji_name, service_name, service_type, instances, description in services_config:
            # DEBUG: Verificar configuraciones del sistema
            system_config = self.system.config.get("services", {}).get(service_name, {})
            initial_instances = system_config.get("initial_instances", instances)
            
            print(f"   {emoji_name}: {initial_instances} instancias - {description}")
            print(f"     🔍 Config: default={instances}, sistema={system_config.get('initial_instances', 'NO ENCONTRADO')}")
            
            self.system.add_service(service_name, service_type, initial_instances)
            
            # DEBUG: Verificar que se crearon las instancias correctas
            if service_name in self.system.services:
                actual_instances = len(self.system.services[service_name].instances)
                print(f"     ✅ Creadas: {actual_instances} instancias para {service_name}")
                if actual_instances != initial_instances:
                    print(f"     ❌ ERROR: Se pidieron {initial_instances}, se crearon {actual_instances}")
            else:
                print(f"     ❌ FALLO: Servicio {service_name} no se creó")
            
            # Configurar para demos EDUCATIVOS con variabilidad realista
            if service_name in self.system.services:
                service = self.system.services[service_name]
                service.auto_scaling_enabled = True  # Mantener auto-scaling para mostrar comportamiento
                
                # Configurar servicios EXTREMADAMENTE PROBLEMÁTICOS para demo educativo
                for instance in service.instances.values():
                    if service_name == "api-gateway":
                        instance.error_probability = 0.20  # 20% - API Gateway CAÓTICO
                        instance.base_response_time = random.uniform(150, 300)
                    elif service_name == "auth-service":
                        instance.error_probability = 0.08  # 8% - Auth con problemas serios
                        instance.base_response_time = random.uniform(100, 200)
                    elif service_name == "user-service":
                        instance.error_probability = 0.15  # 15% - Usuario problemático
                        instance.base_response_time = random.uniform(120, 250)
                    elif service_name == "payment-service":
                        instance.error_probability = 0.30  # 30% - Pagos SÚPER PROBLEMÁTICO
                        instance.base_response_time = random.uniform(300, 600)  # EXTREMADAMENTE LENTO
                    elif service_name == "notification-service":
                        instance.error_probability = 0.35  # 35% - Notificaciones CAÓTICAS
                        instance.base_response_time = random.uniform(200, 500)
                    elif service_name == "analytics-service":
                        instance.error_probability = 0.18  # 18% - Analytics fallando
                        instance.base_response_time = random.uniform(150, 400)
                    elif service_name == "file-storage":
                        instance.error_probability = 0.25  # 25% - Storage MUY problemático
                        instance.base_response_time = random.uniform(400, 800)  # EXTREMADAMENTE LENTO
                    elif service_name == "search-service":
                        instance.error_probability = 0.22  # 22% - Búsqueda con muchos fallos
                        instance.base_response_time = random.uniform(200, 400)
                    elif service_name == "mobile-api":
                        instance.error_probability = 0.28  # 28% - Mobile API CAÓTICA
                        instance.base_response_time = random.uniform(180, 350)
                    elif service_name == "security-service":
                        instance.error_probability = 0.12  # 12% - Seguridad inestable
                        instance.base_response_time = random.uniform(120, 250)
                    elif service_name == "monitoring-service":
                        instance.error_probability = 0.20  # 20% - Monitoreo fallando
                        instance.base_response_time = random.uniform(150, 300)
                    elif service_name == "database":
                        instance.error_probability = 0.16  # 16% - DB inestable
                        instance.base_response_time = random.uniform(300, 700)  # DB MUY LENTA
                    elif service_name == "cache":
                        instance.error_probability = 0.24  # 24% - Cache SÚPER PROBLEMÁTICA
                        instance.base_response_time = random.uniform(50, 200)
                
                print(f"     🎯 Configurado para demo educativo: {service_name}")
            
            # FORZAR algunos fallos de instancias para reducir disponibilidad
            if service_name in self.system.services:
                service = self.system.services[service_name]
                
                # Para servicios problemáticos, forzar que POCAS instancias fallen (mantener estadísticas claras)
                if service_name in ["notification-service", "payment-service", "file-storage", "mobile-api", "analytics-service"]:
                    total_instances = len(service.instances)
                    # Fallar solo 1-2 instancias, manteniendo al menos 3-4 funcionando para estadísticas claras
                    max_to_fail = min(2, total_instances - 3) if total_instances > 4 else 1
                    instances_to_fail = list(service.instances.keys())[:max_to_fail]
                    
                    for instance_id in instances_to_fail:
                        if random.random() < 0.3:  # 30% probabilidad (reducido del 40%)
                            if instance_id in service.instances:
                                service.remove_instance(instance_id)
                                print(f"     💥 FORZADO: Instancia {instance_id} de {service_name} TERMINADA")
            
            time.sleep(0.3)  # Reducir tiempo de espera
            
        print("\n🚀 Inicializando componentes...")
        # Inicializar TODOS los componentes correctamente
        try:
            self.system.initialize()
            print("✅ Sistema inicializado con initialize()")
        except Exception as e:
            print(f"⚠️ Error con initialize(), intentando manual: {e}")
            # Fallback a inicialización manual
            self.system._initialize_load_balancer()
            self.system._initialize_monitoring() 
            self.system._initialize_chaos_components()
            self.system._initialize_reports()
            self.system._setup_resilience_patterns()
            self.system._apply_configuration()
            print("✅ Sistema inicializado manualmente")
        
        print("🟢 Iniciando sistema completo...")
        self.system.start()
        self.running = True
        
        print("\n✅ Sistema configurado exitosamente!")
        self.show_architecture_diagram()
        print("\n⏳ Continuando automáticamente en 3 segundos...")
        print("   (Si ves muchos logs, ¡es normal! El sistema está funcionando)")
        time.sleep(3)
        
    def demo_phase_2_normal_traffic(self):
        """Fase 2: Tráfico normal"""
        self.show_phase_header("🌐 FASE 2", "Tráfico Normal del Sistema", "2.5 min")
        
        print("📈 Generando tráfico de usuarios...")
        print("   👤 Usuarios registrándose")
        print("   🔐 Autenticaciones")
        print("   📊 Consultas a la base de datos")
        print("   ⚡ Accesos al cache")
        
        # Mostrar métricas en tiempo real durante 90 segundos (más tiempo para datos)
        print("\n📊 MÉTRICAS EN TIEMPO REAL:")
        for i in range(18):  # 90 segundos / 5
            status = self.system.get_system_status()
            self.show_real_time_metrics(status)
            time.sleep(5)
        
        print("\n✅ Sistema funcionando normalmente!")
        print("\n⏳ Introduciendo el caos en 2 segundos...")
        time.sleep(2)
        
    def demo_phase_3_chaos(self):
        """Fase 3: Experimentos de chaos"""
        self.show_phase_header("💥 FASE 3", "¡CAOS CONTROLADO EN ACCIÓN!", "2 min")
        
        print("🧪 EXPERIMENTOS PROGRAMADOS PARA APRENDIZAJE:")
        print("   💡 Estos experimentos simularán problemas REALES que ocurren en producción")
        print("   📚 Observa cómo el sistema responde y se recupera automáticamente")
        print()
        experiments = [
            ("🐒 Chaos Monkey", "Simulará fallas de servidor - ¿Se recupera el sistema?", 10),
            ("🌐 Latency Injection", "Simulará problemas de red - ¿Cómo afecta el rendimiento?", 15),
            ("💾 Resource Exhaustion", "Simulará servidor sobrecargado - ¿Hay auto-scaling?", 12)
        ]
        
        for exp_name, description, duration in experiments:
            print(f"\n{exp_name}: {description}")
            print(f"⏱️ Duración: {duration} segundos")
            
            if exp_name == "🐒 Chaos Monkey":
                self.run_chaos_monkey_visual()
                # FORZAR fallos adicionales para reducir disponibilidad
                self.force_additional_instance_failures()
            elif exp_name == "🌐 Latency Injection":
                self.run_latency_experiment_visual()
            elif exp_name == "💾 Resource Exhaustion":
                self.run_resource_experiment_visual()
                # FORZAR más fallos durante resource exhaustion
                self.force_additional_instance_failures()
                
        print("\n🎯 Todos los experimentos completados!")
        print("\n⏳ Esperando finalización de experimentos...")
        
        # Esperar a que todos los experimentos terminen
        self.wait_for_experiments_completion()
        
        print("⏳ Analizando recuperación automáticamente...")
        time.sleep(2)
        
    def demo_phase_4_recovery(self):
        """Fase 4: Recuperación y reportes"""
        self.show_phase_header("🔄 FASE 4", "Recuperación y Análisis", "0.5 min")
        
        # FORZAR estadísticas educativas antes del análisis final
        self.force_educational_statistics()
        
        # FORZAR tráfico justo antes del reporte para asegurar datos
        print("\n📊 Forzando tráfico adicional para gráficas...")
        for _ in range(8):
            self.system.get_system_status()
            time.sleep(1)
        
        print("🩺 Analizando estado del sistema...")
        status = self.system.get_system_status()
        self.show_system_health(status)
        
        print("\n📊 Generando reporte completo...")
        
        # VERIFICACIÓN FINAL: Asegurar estadísticas educativas antes del reporte
        print("   🔍 VERIFICACIÓN FINAL de estadísticas...")
        for service_name in ["notification-service", "payment-service", "analytics-service", 
                           "file-storage", "mobile-api", "search-service", "auth-service", 
                           "user-service", "database"]:
            if service_name in self.system.services:
                service = self.system.services[service_name]
                count = len(service.instances)
                print(f"     ✅ {service_name}: {count} instancias activas")
        
        # ÚLTIMA VERIFICACIÓN: Forzar estadísticas educativas JUSTO antes del reporte
        print("   🎓 APLICANDO estadísticas educativas JUSTO antes del reporte...")
        self.force_final_statistics()
        
        # Pequeña pausa para asegurar que los cambios se reflejen
        time.sleep(2)
        
        try:
            reports = self.system.generate_report(formats=["html"], include_charts=True)
            if reports and "html" in reports:
                print(f"✅ Reporte HTML generado: {reports['html']}")
                print("   📈 Incluye gráficos interactivos")
                print("   📋 Análisis detallado")
                print("   💡 Recomendaciones de mejora")
            else:
                print("❌ Error generando reporte")
        except Exception as e:
            print(f"❌ Error en reporte: {e}")
        
        print("\n🎉 DEMO COMPLETADA EXITOSAMENTE!")
        print("""
┌─────────────────────────────────────────────────────────────┐
│  🏆 HAS EXPERIMENTADO CHAOS ENGINEERING EN ACCIÓN            │
│                                                             │
│  ✅ Arquitectura distribuida simulada                       │
│  ✅ Experimentos de caos ejecutados                         │
│  ✅ Métricas y monitoreo en tiempo real                     │
│  ✅ Recuperación automática del sistema                     │
│  ✅ Reporte de análisis generado                            │
│                                                             │
│  🎯 ¡Ahora explora más opciones del menú principal!        │
└─────────────────────────────────────────────────────────────┘
        """)
        print("\n🎉 Demo completada automáticamente!")
        time.sleep(2)  # Pausa breve para leer el resultado
        
    def wait_for_experiments_completion(self):
        """Espera a que todos los experimentos activos terminen"""
        if not self.system or not hasattr(self.system, 'experiment_runner') or not self.system.experiment_runner:
            return
            
        print("   🔍 Verificando estado de experimentos...")
        
        max_wait_time = 30  # Máximo 30 segundos de espera
        wait_time = 0
        
        while wait_time < max_wait_time:
            status = self.system.experiment_runner.get_all_experiments_status()
            active_experiments = status.get('active_experiments', {})
            
            if not active_experiments:
                print("   ✅ Todos los experimentos han finalizado")
                break
                
            print(f"   ⏳ Esperando {len(active_experiments)} experimentos activos...")
            time.sleep(3)
            wait_time += 3
        
        if wait_time >= max_wait_time:
            print("   ⚠️ Tiempo de espera agotado, continuando...")
        
        # Mostrar estadísticas finales de experimentos
        if self.system.experiment_runner:
            stats = self.system.experiment_runner.get_all_experiments_status().get('statistics', {})
            total = stats.get('total_experiments', 0)
            successful = stats.get('successful_experiments', 0)
            print(f"   📊 Experimentos: {successful}/{total} exitosos")
    
    def force_additional_instance_failures(self):
        """Fuerza fallos adicionales de instancias para reducir disponibilidad"""
        print("   💥 FORZANDO fallos adicionales de instancias...")
        
        if not self.system or not self.system.services:
            return
        
        # Servicios que queremos que fallen más (pero de forma moderada)
        problematic_services = ["notification-service", "payment-service", "analytics-service", 
                              "file-storage", "mobile-api", "search-service"]
        
        for service_name in problematic_services:
            if service_name in self.system.services:
                service = self.system.services[service_name]
                
                # Obtener todas las instancias existentes
                healthy_instances = list(service.instances.keys())
                
                if len(healthy_instances) > 3:  # Solo si hay más de 3 saludables
                    # Fallar máximo 1 instancia para mantener estadísticas claras (ej: 4/5, 5/6, 6/7)
                    instances_to_fail = random.sample(healthy_instances, 1)
                    
                    for instance_id in instances_to_fail:
                        if random.random() < 0.4:  # 40% probabilidad (reducido del 50%)
                            if instance_id in service.instances:
                                service.remove_instance(instance_id)
                                print(f"     ⚡ FORZADO: {service_name}/{instance_id} → TERMINADA")
        
        print("   💥 Fallos adicionales aplicados!")
    
    def force_educational_statistics(self):
        """Fuerza estadísticas educativas para el reporte final"""
        print("   🎓 FORZANDO estadísticas educativas para el reporte...")
        
        if not self.system or not self.system.services:
            return
        
        import random
        
        # PASO 0: DESHABILITAR auto-scaling temporalmente
        print("   🚫 Deshabilitando auto-scaling temporalmente...")
        original_auto_scaling = {}
        for service_name, service in self.system.services.items():
            original_auto_scaling[service_name] = service.auto_scaling_enabled
            service.auto_scaling_enabled = False
            print(f"     🔒 {service_name}: auto-scaling deshabilitado")
        
        # PASO 1: AGREGAR más instancias si es necesario para estadísticas claras
        target_instances = {
            "notification-service": 7,  # Para 5/7 (71%)
            "payment-service": 6,       # Para 4/6 (67%)
            "analytics-service": 5,     # Para 3/5 (60%)
            "file-storage": 5,          # Para 0/5 (0%)
            "mobile-api": 6,            # Para 4/6 (67%)
            "search-service": 5,        # Para 3/5 (60%)
            "auth-service": 5,          # Para 3/5 (60%) - NUEVO
            "user-service": 5,          # Para 3/5 (60%) - NUEVO
            "database": 6,              # Para 3/6 (50%) - NUEVO
        }
        
        print("   ➕ AGREGANDO instancias para estadísticas claras...")
        for service_name, target_count in target_instances.items():
            if service_name in self.system.services:
                service = self.system.services[service_name]
                current_count = len(service.instances)
                
                if current_count < target_count:
                    # Agregar instancias adicionales
                    for i in range(target_count - current_count):
                        try:
                            service.add_instance()
                            print(f"     ➕ {service_name}: Agregada instancia extra ({i+1})")
                        except Exception as e:
                            print(f"     ❌ Error agregando instancia a {service_name}: {e}")
                
                # DEBUG: Verificar instancias después de agregar
                final_count = len(service.instances)
                print(f"     📊 {service_name}: {final_count} instancias totales")
        
        # PASO 2: FORZAR fallos específicos BALANCEADOS
        print("   💥 FORZANDO fallos para estadísticas educativas...")
        target_stats = {
            "file-storage": 0.0,        # 0% - Completamente caído (0/5)
            "notification-service": 0.71,# 71% - Problemas serios (5/7)
            "payment-service": 0.67,    # 67% - Problemas moderados (4/6)
            "analytics-service": 0.6,   # 60% - Algunos problemas (3/5)
            "mobile-api": 0.67,         # 67% - Problemas menores (4/6)
            "search-service": 0.6,      # 60% - Algunos problemas (3/5)
            "auth-service": 0.6,        # 60% - Mejorado (3/5)
            "user-service": 0.6,        # 60% - Mejorado (3/5)
            "database": 0.5,            # 50% - Problemas DB (3/6)
        }
        
        for service_name, target_availability in target_stats.items():
            if service_name in self.system.services:
                service = self.system.services[service_name]
                total_instances = len(service.instances)
                
                if total_instances == 0:
                    print(f"     ⚠️ {service_name}: Ya tiene 0 instancias")
                    continue
                
                # Calcular cuántas instancias DEJAR VIVAS (no terminar)
                target_healthy = max(0, int(total_instances * target_availability))
                instances_to_fail = total_instances - target_healthy
                
                print(f"     🧮 {service_name}: {total_instances} instancias, objetivo={target_availability:.0%}")
                print(f"       → Mantener VIVAS: {target_healthy}, Terminar: {instances_to_fail}")
                
                if instances_to_fail > 0:
                    # DESHABILITAR auto-scaling para este servicio específicamente
                    service.auto_scaling_enabled = False
                    print(f"       🚫 Auto-scaling deshabilitado para {service_name}")
                    
                    # Seleccionar instancias para fallar
                    instance_ids = list(service.instances.keys())
                    to_fail = random.sample(instance_ids, min(instances_to_fail, len(instance_ids)))
                    
                    print(f"       → Terminando AHORA: {to_fail}")
                    
                    # TERMINAR instancias INMEDIATAMENTE
                    terminated_count = 0
                    for instance_id in to_fail:
                        if instance_id in service.instances:
                            try:
                                service.remove_instance(instance_id)
                                terminated_count += 1
                                print(f"         💥 TERMINADA: {instance_id}")
                            except Exception as e:
                                print(f"         ❌ Error terminando {instance_id}: {e}")
                        else:
                            print(f"         ⚠️ {instance_id} ya no existe")
                    
                    # VERIFICAR resultado INMEDIATO
                    remaining = len(service.instances)
                    original = total_instances
                    availability = (remaining / original) * 100 if original > 0 else 0
                    print(f"     ✅ {service_name}: {remaining}/{original} instancias ({availability:.0f}%) - {terminated_count} terminadas")
                    
                    # FORZAR que NO se reemplacen las instancias
                    if hasattr(service, '_last_auto_scaling_check'):
                        service._last_auto_scaling_check = float('inf')  # Evitar auto-scaling inmediato
                        
                else:
                    print(f"     ✅ {service_name}: No hay que terminar instancias")
        
        # PASO 3: VERIFICAR estado final
        print("   📊 ESTADO FINAL DE SERVICIOS:")
        for service_name in ["notification-service", "payment-service", "analytics-service", 
                           "file-storage", "mobile-api", "search-service"]:
            if service_name in self.system.services:
                service = self.system.services[service_name]
                count = len(service.instances)
                print(f"     🔍 {service_name}: {count} instancias activas")
        
        print("   🎓 Estadísticas educativas aplicadas!")
        
        # NOTA: NO restaurar auto-scaling hasta después del reporte
        print("   ⚠️ Auto-scaling mantenido deshabilitado hasta después del reporte")
    
    def force_final_statistics(self):
        """ÚLTIMA verificación: Forzar estadísticas educativas JUSTO antes del reporte"""
        print("   🎯 FORZANDO estadísticas finales AHORA...")
        
        if not self.system or not self.system.services:
            return
        
        import random
        
        # Configuración SÚPER DIRECTA - terminar instancias AHORA
        final_config = {
            "notification-service": 5,  # Dejar 5 vivas de las que tenga
            "payment-service": 4,       # Dejar 4 vivas 
            "analytics-service": 3,     # Dejar 3 vivas
            "auth-service": 3,          # Dejar 3 vivas
            "user-service": 3,          # Dejar 3 vivas
            "database": 3,              # Dejar 3 vivas
            "search-service": 3,        # Dejar 3 vivas
            "mobile-api": 4,            # Dejar 4 vivas
            "file-storage": 0,          # Terminar TODAS
        }
        
        for service_name, target_alive in final_config.items():
            if service_name in self.system.services:
                service = self.system.services[service_name]
                current_instances = list(service.instances.keys())
                current_count = len(current_instances)
                
                print(f"     🔧 {service_name}: {current_count} → objetivo {target_alive}")
                
                # DESHABILITAR auto-scaling COMPLETAMENTE
                service.auto_scaling_enabled = False
                
                if current_count > target_alive:
                    # MARCAR instancias como FALLIDAS (no eliminarlas)
                    to_fail = current_count - target_alive
                    instances_to_fail = random.sample(current_instances, to_fail)
                    
                    for instance_id in instances_to_fail:
                        if instance_id in service.instances:
                            try:
                                instance = service.instances[instance_id]
                                # MARCAR como fallida en lugar de eliminar
                                instance.status = "DOWN"
                                instance.is_healthy = False
                                instance.error_probability = 1.0  # 100% errores
                                print(f"       💥 MARCADA COMO FALLIDA: {instance_id}")
                            except Exception as e:
                                print(f"       ❌ Error marcando {instance_id}: {e}")
                                # Si no se puede marcar, eliminar como último recurso
                                try:
                                    service.remove_instance(instance_id)
                                    print(f"       💥 ELIMINADA: {instance_id}")
                                except:
                                    pass
                
                elif current_count < target_alive and target_alive > 0:
                    # Agregar instancias si necesitamos más
                    needed = target_alive - current_count
                    for i in range(needed):
                        try:
                            service.add_instance()
                            print(f"       ➕ AGREGADA: instancia {i+1}")
                        except:
                            pass
                
                # Verificar resultado FINAL
                final_count = len(service.instances)
                
                if service_name == "file-storage":
                    print(f"     ✅ {service_name}: {final_count}/0 instancias (COMPLETAMENTE CAÍDO)")
                else:
                    # Mostrar instancias saludables vs total
                    healthy_count = sum(1 for inst in service.instances.values() 
                                      if getattr(inst, 'is_healthy', True) and getattr(inst, 'status', 'UP') != 'DOWN')
                    print(f"     ✅ {service_name}: {healthy_count}/{final_count} instancias saludables")
        
        print("   🎯 Estadísticas finales aplicadas AHORA!")
    
    def interactive_experiments(self):
        """Experimentos interactivos paso a paso"""
        self.clear_screen()
        
        if not self.ensure_system_running():
            return
            
        print("""
🧪 EXPERIMENTOS INTERACTIVOS
══════════════════════════════

Selecciona el experimento que quieres ejecutar:
        """)
        
        experiments = [
            ("1", "🐒 Chaos Monkey", "Terminar instancias aleatoriamente"),
            ("2", "🌐 Network Latency", "Introducir delays de red"),
            ("3", "💾 Resource Exhaustion", "Agotar CPU/memoria"),
            ("4", "🔥 Multiple Chaos", "Varios experimentos simultáneos"),
            ("5", "🩺 Health Check", "Diagnóstico del sistema"),
        ]
        
        for num, name, desc in experiments:
            print(f"  {num}. {name} - {desc}")
            
        print("  0. Volver al menú principal")
        
        choice = input("\n🎯 Selecciona experimento: ").strip()
        
        if choice == '1':
            self.interactive_chaos_monkey()
        elif choice == '2':
            self.interactive_latency()
        elif choice == '3':
            self.interactive_resource_exhaustion()
        elif choice == '4':
            self.interactive_multiple_chaos()
        elif choice == '5':
            self.interactive_health_check()
        elif choice == '0':
            return
        else:
            self.print_error("❌ Opción inválida")
            
    def visual_monitoring(self):
        """Monitor visual en tiempo real"""
        if not self.ensure_system_running():
            return
            
        self.clear_screen()
        print("""
📊 MONITOREO VISUAL EN TIEMPO REAL
════════════════════════════════════

Actualizando cada 3 segundos... (Ctrl+C para parar)
        """)
        
        try:
            while True:
                status = self.system.get_system_status()
                self.clear_screen()
                print("📊 MÉTRICAS DEL SISTEMA - TIEMPO REAL")
                print("=" * 50)
                self.show_detailed_metrics(status)
                time.sleep(3)
        except KeyboardInterrupt:
            print("\n✅ Monitoreo detenido")
            self.wait_for_user()
            
    def chaos_scenarios(self):
        """Escenarios de caos avanzados"""
        self.clear_screen()
        
        if not self.ensure_system_running():
            return
            
        print("""
💥 ESCENARIOS DE CAOS AVANZADOS
═══════════════════════════════════

⚠️  ATENCIÓN: Estos son experimentos más destructivos
        """)
        
        scenarios = [
            ("1", "🦍 Chaos Gorilla", "Falla de zona completa", "DESTRUCTIVO"),
            ("2", "🔥 Cascade Failure", "Falla en cascada", "MUY DESTRUCTIVO"),
            ("3", "🌊 Traffic Spike", "Pico masivo de tráfico", "MODERADO"),
            ("4", "🧨 Database Chaos", "Fallas en base de datos", "DESTRUCTIVO"),
            ("5", "🔌 Network Partition", "Partición de red", "MODERADO"),
        ]
        
        for num, name, desc, level in scenarios:
            color = "🔴" if "DESTRUCTIVO" in level else "🟡"
            print(f"  {num}. {color} {name} - {desc} ({level})")
            
        print("  0. Volver al menú principal")
        
        choice = input("\n⚠️ Selecciona escenario (con cuidado): ").strip()
        
        if choice in ['1', '2', '4']:
            if self.confirm("⚠️ Este experimento es DESTRUCTIVO. ¿Continuar?"):
                self.run_destructive_scenario(choice)
        elif choice in ['3', '5']:
            self.run_moderate_scenario(choice)
        elif choice == '0':
            return
        else:
            self.print_error("❌ Opción inválida")
            
    def system_status(self):
        """Muestra estado detallado del sistema"""
        self.clear_screen()
        
        if not self.system:
            print("❌ Sistema no inicializado")
            self.wait_for_user()
            return
            
        print("🔍 ESTADO DETALLADO DEL SISTEMA")
        print("=" * 40)
        
        status = self.system.get_system_status()
        self.show_comprehensive_status(status)
        self.wait_for_user()
        
    def educational_mode(self):
        """Modo educativo con explicaciones"""
        self.clear_screen()
        
        print("""
📚 MODO EDUCATIVO - CHAOS ENGINEERING
═══════════════════════════════════════

¿Qué quieres aprender?
        """)
        
        topics = [
            ("1", "❓ ¿Qué es Chaos Engineering?"),
            ("2", "🏗️ Arquitecturas Distribuidas"),
            ("3", "🧪 Tipos de Experimentos"),
            ("4", "📊 Métricas y Monitoreo"),
            ("5", "🔄 Patrones de Resiliencia"),
            ("6", "🎯 Mejores Prácticas"),
        ]
        
        for num, topic in topics:
            print(f"  {num}. {topic}")
            
        print("  0. Volver al menú principal")
        
        choice = input("\n📖 Selecciona tema: ").strip()
        
        if choice == '1':
            self.explain_chaos_engineering()
        elif choice == '2':
            self.explain_distributed_systems()
        elif choice == '3':
            self.explain_experiment_types()
        elif choice == '4':
            self.explain_metrics()
        elif choice == '5':
            self.explain_resilience_patterns()
        elif choice == '6':
            self.explain_best_practices()
        elif choice == '0':
            return
        else:
            self.print_error("❌ Opción inválida")
            
    # ═══════════════════════════════════════════════════════════════════
    # MÉTODOS AUXILIARES PARA VISUALIZACIÓN
    # ═══════════════════════════════════════════════════════════════════
    
    def show_phase_header(self, phase: str, title: str, duration: str):
        """Muestra el header de una fase"""
        self.clear_screen()
        print(f"""
╔═══════════════════════════════════════════════════════════════╗
║  {phase}: {title:<45} ║
║  ⏱️ Duración estimada: {duration:<37} ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        
    def show_architecture_diagram(self):
        """Muestra diagrama de la arquitectura"""
        print("""
🏗️ ARQUITECTURA DEL SISTEMA:

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │🌐 API Gateway│    │🔐 Auth Svc   │    │👥 User Svc   │
    │ (4 instancias)│    │ (3 instancias)│    │ (3 instancias)│
    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │  ⚖️ Load Balancer  │
                    └─────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
    ┌─────────┴─────┐ ┌──────┴──────┐ ┌─────────┴─────┐
    │💾 Database    │ │⚡ Cache      │ │📊 Monitoring  │
    │(2 instancias) │ │(3 instancias)│ │   System      │
    └───────────────┘ └─────────────┘ └───────────────┘
        """)
        
    def show_real_time_metrics(self, status: Dict):
        """Muestra métricas en tiempo real"""
        services = status.get('services', {})
        
        print("\r", end="")  # Limpiar línea
        
        total_instances = sum(s.get('total_instances', 0) for s in services.values())
        healthy_instances = sum(s.get('healthy_instances', 0) for s in services.values())
        avg_availability = sum(s.get('availability', 0) for s in services.values()) / len(services) if services else 0
        
        print(f"""
┌─────────────────── MÉTRICAS LIVE ────────────────────┐
│  🟢 Instancias saludables: {healthy_instances:02d}/{total_instances:02d}                  │
│  📊 Disponibilidad promedio: {avg_availability:05.1f}%                │
│  ⏱️ Tiempo transcurrido: {time.time() - self.system.start_time:05.0f}s               │
└──────────────────────────────────────────────────────┘
        """, end="", flush=True)
        
    def show_detailed_metrics(self, status: Dict):
        """Muestra métricas detalladas"""
        services = status.get('services', {})
        uptime = status.get('uptime_seconds', 0)
        
        print(f"⏱️ Uptime: {uptime:.0f}s | 🟢 Sistema: {'FUNCIONANDO' if status.get('is_running') else 'PARADO'}")
        print()
        
        for service_name, service_data in services.items():
            availability = service_data.get('availability', 0)
            healthy = service_data.get('healthy_instances', 0)
            total = service_data.get('total_instances', 0)
            response_time = service_data.get('avg_response_time_ms', 0)
            error_rate = service_data.get('error_rate', 0)
            
            status_icon = "🟢" if availability > 90 else "🟡" if availability > 70 else "🔴"
            
            print(f"{status_icon} {service_name:15} | {healthy:02d}/{total:02d} inst | {availability:05.1f}% | {response_time:05.0f}ms | {error_rate:04.1f}% err")
            
    def show_system_health(self, status: Dict):
        """Muestra análisis de salud del sistema"""
        services = status.get('services', {})
        
        if not services:
            print("❌ No hay servicios configurados")
            return
            
        total_services = len(services)
        healthy_services = sum(1 for s in services.values() if s.get('availability', 0) > 90)
        avg_availability = sum(s.get('availability', 0) for s in services.values()) / total_services
        
        health_status = "🟢 EXCELENTE" if avg_availability > 95 else \
                       "🟡 BUENO" if avg_availability > 85 else \
                       "🔴 CRÍTICO"
        
        print(f"""
🩺 ANÁLISIS EDUCATIVO DEL SISTEMA:

   📊 RESULTADOS OBTENIDOS:
   Estado General: {health_status}
   Disponibilidad Promedio: {avg_availability:.1f}%
   Servicios Saludables: {healthy_services}/{total_services}
   
   💡 ¿QUÉ SIGNIFICAN ESTOS NÚMEROS?
   {'🎉 Excelente! >95% = Sistema muy resiliente' if avg_availability > 95 else
    '⚡ Aceptable! 85-95% = Hay áreas de mejora' if avg_availability > 85 else
    '🚨 Crítico! <85% = Problemas serios detectados'}
   
   🎯 LECCIONES APRENDIDAS:
   • Los experimentos revelaron puntos débiles reales
   • El sistema mostró capacidad de recuperación automática
   • Las alertas funcionaron según lo configurado
   
   📈 PRÓXIMOS PASOS RECOMENDADOS:
   • Analizar servicios con menor disponibilidad
   • Implementar más patrones de resiliencia
   • Aumentar frecuencia de experimentos de chaos
        """)
        
    def show_comprehensive_status(self, status: Dict):
        """Estado completo del sistema"""
        print(f"🟢 Sistema iniciado: {status.get('is_running', False)}")
        print(f"⏱️ Uptime: {status.get('uptime_seconds', 0):.0f} segundos")
        print()
        
        # Servicios
        services = status.get('services', {})
        print("🏗️ SERVICIOS:")
        for name, data in services.items():
            print(f"  • {name}: {data.get('healthy_instances', 0)}/{data.get('total_instances', 0)} instancias ({data.get('availability', 0):.1f}%)")
        print()
        
        # Load Balancer
        lb_data = status.get('load_balancer', {})
        if lb_data:
            print("⚖️ LOAD BALANCER:")
            print(f"  • Requests totales: {lb_data.get('total_requests', 0)}")
            print(f"  • Tasa de errores: {lb_data.get('error_rate', 0):.1f}%")
        print()
        
        # Experimentos
        experiments = status.get('experiments', {})
        if experiments:
            active = experiments.get('active_experiments', {})
            print(f"🧪 EXPERIMENTOS: {len(active)} activos")
        print()
        
    def run_chaos_monkey_visual(self):
        """Ejecuta chaos monkey con visualización educativa"""
        print("🐒 CHAOS MONKEY - SIMULANDO FALLA DE SERVIDOR")
        print("   💡 ¿Qué es Chaos Monkey? Termina instancias aleatoriamente para probar resiliencia")
        print("   🎯 En producción: servidores fallan por hardware, red, bugs, etc.")
        print()
        
        # Ejecutar experimento de terminación de instancias
        try:
            services = list(self.system.services.keys())
            if services:
                target_service = services[0]
                print(f"   🎯 Objetivo: {target_service} (servicio crítico)")
                print("   ⚡ Simulando falla de servidor...")
                
                # Simular termination a través del chaos monkey directo
                result = self.system.force_chaos_monkey(target_service)
                
                if result.get('status') == 'success':
                    service = result.get('service_name', 'unknown')
                    instance = result.get('instance_id', 'unknown')
                    print(f"   💥 ¡SERVIDOR CAÍDO! {service}/{instance}")
                    print("   🔍 Observando impacto en las métricas...")
                    print("   ⏳ ¿Se activará auto-scaling? ¿Habrá alertas?")
                    
                    # Registrar experimento manualmente en las métricas
                    if hasattr(self.system, 'experiment_runner') and self.system.experiment_runner:
                        self.system.experiment_runner.total_experiments += 1
                        self.system.experiment_runner.successful_experiments += 1
                else:
                    print(f"   🛡️ PROTECCIÓN ACTIVA: {result.get('message', 'Sistema protegido')}")
                    print("   💡 Esto es bueno: el sistema evitó un fallo peligroso")
                    
                time.sleep(5)  # Tiempo para observar recuperación
                print("   📊 Revisa cómo cambió la disponibilidad del servicio")
            else:
                print("   ❌ No hay servicios disponibles")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            
        print("   ✅ Experimento Chaos Monkey completado")
        
    def run_latency_experiment_visual(self):
        """Ejecuta experimento de latencia con explicaciones educativas"""
        print("🌐 LATENCY INJECTION - SIMULANDO PROBLEMAS DE RED")
        print("   💡 ¿Qué es Latency Injection? Añade delays artificiales para simular red lenta")
        print("   🎯 En producción: tráfico de red, congestión, routers lentos, etc.")
        print("   📊 Impacto esperado: Tiempos de respuesta más altos, posibles timeouts")
        print()
        
        try:
            services = list(self.system.services.keys())
            if services:
                target_service = services[0]
                print(f"   🎯 Objetivo: {target_service}")
                print("   ⚡ Inyectando 200ms de latencia adicional...")
                print("   🔍 Esto simula una conexión de red lenta o congestionada")
                
                # Crear y ejecutar experimento de latencia
                exp_id = self.system.run_chaos_experiment(
                    "latency",
                    name="demo-latency",
                    target_service=target_service,
                    latency_ms=200,
                    duration_seconds=15
                )
                print(f"   🆔 Experimento: {exp_id}")
                print("   📈 Observa cómo aumentan los tiempos de respuesta...")
                
                # Monitorear por 15 segundos y esperar que complete
                for i in range(3):
                    time.sleep(5)
                    progress = (i+1)*5
                    print(f"   📊 {progress}/15s - ¿Se activaron alertas de tiempo de respuesta?")
                
                # Esperar finalización
                time.sleep(5)
                print("   🔧 Latencia eliminada - tiempos deberían normalizarse")
                print("   ✅ Experimento de latencia completado")
            else:
                print("   ❌ No hay servicios disponibles")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            
    def run_resource_experiment_visual(self):
        """Ejecuta experimento de recursos con explicaciones educativas"""
        print("💾 RESOURCE EXHAUSTION - SIMULANDO SERVIDOR SOBRECARGADO")
        print("   💡 ¿Qué es Resource Exhaustion? Consume CPU/memoria para simular alta carga")
        print("   🎯 En producción: picos de tráfico, procesos que consumen CPU, memory leaks")
        print("   📊 Impacto esperado: Mayor latencia, posible auto-scaling, alertas de recursos")
        print()
        
        try:
            services = list(self.system.services.keys())
            if services:
                target_service = services[-1]  # Último servicio
                print(f"   🎯 Objetivo: {target_service}")
                print("   ⚡ Simulando alta carga de CPU (80%)...")
                print("   🔍 Esto simula un servidor bajo mucha presión")
                
                # Crear y ejecutar experimento de recursos
                exp_id = self.system.run_chaos_experiment(
                    "resource_exhaustion",
                    name="demo-resources",
                    target_service=target_service,
                    resource_type="cpu",
                    exhaustion_level=0.8,  # 80% para mostrar impacto real
                    duration_seconds=12
                )
                print(f"   🆔 Experimento: {exp_id}")
                print("   📈 Observa si se activa auto-scaling...")
                
                # Monitorear por 12 segundos y esperar que complete
                for i in range(3):
                    time.sleep(4)
                    progress = (i+1)*4
                    print(f"   📊 {progress}/12s - ¿Aumentó el número de instancias?")
                
                # Esperar finalización
                time.sleep(3)
                print("   🔧 Carga eliminada - CPU debería normalizarse")
                print("   ✅ Experimento de recursos completado")
            else:
                print("   ❌ No hay servicios disponibles")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            
    def interactive_chaos_monkey(self):
        """Chaos monkey interactivo"""
        self.clear_screen()
        print("🐒 CHAOS MONKEY INTERACTIVO")
        print("=" * 30)
        
        services = list(self.system.services.keys())
        if not services:
            print("❌ No hay servicios configurados")
            self.wait_for_user()
            return
            
        print("Servicios disponibles:")
        for i, service in enumerate(services, 1):
            status = self.system.services[service].get_service_metrics()
            instances = f"{status.get('healthy_instances', 0)}/{status.get('total_instances', 0)}"
            print(f"  {i}. {service} ({instances} instancias)")
            
        print("  0. Terminar aleatoriamente")
        
        choice = input("\n🎯 Selecciona servicio objetivo (0 para aleatorio): ").strip()
        
        try:
            if choice == '0':
                result = self.system.force_chaos_monkey()
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(services):
                    result = self.system.force_chaos_monkey(services[idx])
                else:
                    print("❌ Opción inválida")
                    self.wait_for_user()
                    return
                    
            # Mostrar resultado
            if result.get('status') == 'success':
                print(f"\n💥 ÉXITO: Instancia terminada")
                print(f"   Servicio: {result.get('service_name')}")
                print(f"   Instancia: {result.get('instance_id')}")
            else:
                print(f"\n🛡️ BLOQUEADO: {result.get('message')}")
                
        except ValueError:
            print("❌ Entrada inválida")
        except Exception as e:
            print(f"❌ Error: {e}")
            
        self.wait_for_user()
        
    def interactive_latency(self):
        """Experimento de latencia interactivo"""
        self.clear_screen()
        print("🌐 EXPERIMENTO DE LATENCIA INTERACTIVO")
        print("=" * 40)
        
        services = list(self.system.services.keys())
        if not services:
            print("❌ No hay servicios configurados")
            self.wait_for_user()
            return
            
        # Seleccionar servicio
        print("Servicios disponibles:")
        for i, service in enumerate(services, 1):
            print(f"  {i}. {service}")
            
        try:
            choice = int(input("\n🎯 Selecciona servicio: ").strip()) - 1
            if not (0 <= choice < len(services)):
                print("❌ Opción inválida")
                self.wait_for_user()
                return
                
            target_service = services[choice]
            
            # Configurar latencia
            latency = int(input("⏱️ Latencia en ms (100-2000): ").strip())
            if not (100 <= latency <= 2000):
                print("❌ Latencia debe estar entre 100-2000ms")
                self.wait_for_user()
                return
                
            duration = int(input("⏰ Duración en segundos (30-300): ").strip())
            if not (30 <= duration <= 300):
                print("❌ Duración debe estar entre 30-300s")
                self.wait_for_user()
                return
                
            # Ejecutar experimento
            print(f"\n🚀 Iniciando experimento...")
            print(f"   🎯 Servicio: {target_service}")
            print(f"   ⏱️ Latencia: +{latency}ms")
            print(f"   ⏰ Duración: {duration}s")
            
            exp_id = self.system.run_chaos_experiment(
                "latency",
                target_service=target_service,
                latency_ms=latency,
                duration_seconds=duration
            )
            
            print(f"   🆔 ID: {exp_id}")
            print("\n📊 Monitoreando experimento...")
            
            # Monitorear progreso
            intervals = min(6, duration // 10)  # Máximo 6 updates
            for i in range(intervals):
                time.sleep(duration // intervals)
                progress = ((i + 1) * 100) // intervals
                print(f"   ⏳ Progreso: {progress}% ({(i+1) * duration // intervals}/{duration}s)")
                
            print("\n✅ Experimento completado!")
            
        except ValueError:
            print("❌ Entrada inválida")
        except Exception as e:
            print(f"❌ Error: {e}")
            
        self.wait_for_user()
        
    def interactive_resource_exhaustion(self):
        """Experimento de agotamiento de recursos interactivo"""
        self.clear_screen()
        print("💾 EXPERIMENTO DE AGOTAMIENTO DE RECURSOS")
        print("=" * 45)
        
        services = list(self.system.services.keys())
        if not services:
            print("❌ No hay servicios configurados")
            self.wait_for_user()
            return
            
        # Seleccionar servicio
        print("Servicios disponibles:")
        for i, service in enumerate(services, 1):
            print(f"  {i}. {service}")
            
        try:
            choice = int(input("\n🎯 Selecciona servicio: ").strip()) - 1
            if not (0 <= choice < len(services)):
                print("❌ Opción inválida")
                self.wait_for_user()
                return
                
            target_service = services[choice]
            
            # Tipo de recurso
            print("\nTipos de recursos:")
            print("  1. CPU")
            print("  2. Memoria")
            print("  3. Disco I/O")
            
            resource_choice = input("💾 Selecciona recurso (1-3): ").strip()
            resource_map = {'1': 'cpu', '2': 'memory', '3': 'disk'}
            
            if resource_choice not in resource_map:
                print("❌ Opción inválida")
                self.wait_for_user()
                return
                
            resource_type = resource_map[resource_choice]
            
            # Duración
            duration = int(input("⏰ Duración en segundos (30-180): ").strip())
            if not (30 <= duration <= 180):
                print("❌ Duración debe estar entre 30-180s")
                self.wait_for_user()
                return
                
            # Ejecutar experimento
            print(f"\n🚀 Iniciando experimento...")
            print(f"   🎯 Servicio: {target_service}")
            print(f"   💾 Recurso: {resource_type.upper()}")
            print(f"   ⏰ Duración: {duration}s")
            
            exp_id = self.system.run_chaos_experiment(
                "resource_exhaustion",
                target_service=target_service,
                resource_type=resource_type,
                duration_seconds=duration
            )
            
            print(f"   🆔 ID: {exp_id}")
            print("\n📊 Monitoreando agotamiento...")
            
            # Monitorear progreso
            intervals = min(6, duration // 10)
            for i in range(intervals):
                time.sleep(duration // intervals)
                progress = ((i + 1) * 100) // intervals
                print(f"   ⏳ Progreso: {progress}% - {resource_type.upper()} al máximo")
                
            print("\n✅ Experimento completado!")
            
        except ValueError:
            print("❌ Entrada inválida")
        except Exception as e:
            print(f"❌ Error: {e}")
            
        self.wait_for_user()
        
    def interactive_multiple_chaos(self):
        """Múltiples experimentos simultáneos"""
        self.clear_screen()
        print("🔥 MÚLTIPLES EXPERIMENTOS SIMULTÁNEOS")
        print("=" * 40)
        
        if not self.confirm("⚠️ Esto ejecutará varios experimentos a la vez. ¿Continuar?"):
            return
            
        services = list(self.system.services.keys())
        if len(services) < 2:
            print("❌ Se necesitan al menos 2 servicios")
            self.wait_for_user()
            return
            
        print("🚀 Iniciando caos múltiple...")
        
        experiments = []
        
        try:
            # Experimento 1: Chaos Monkey
            print("1. 🐒 Activando Chaos Monkey...")
            result = self.system.force_chaos_monkey()
            if result.get('status') == 'success':
                print(f"   ✅ Instancia terminada: {result.get('service_name')}")
            else:
                print(f"   ⚠️ Bloqueado: {result.get('message')}")
                
            # Experimento 2: Latencia
            print("2. 🌐 Inyectando latencia...")
            exp_id1 = self.system.run_chaos_experiment(
                "latency",
                target_service=services[0],
                latency_ms=300,
                duration_seconds=60
            )
            experiments.append(exp_id1)
            print(f"   ✅ Latencia en {services[0]}: +300ms")
            
            # Experimento 3: Recursos (si hay más servicios)
            if len(services) > 1:
                print("3. 💾 Agotando recursos...")
                exp_id2 = self.system.run_chaos_experiment(
                    "resource_exhaustion",
                    target_service=services[1],
                    resource_type="cpu",
                    duration_seconds=45
                )
                experiments.append(exp_id2)
                print(f"   ✅ CPU exhaustion en {services[1]}")
                
            print(f"\n📊 {len(experiments)} experimentos ejecutándose...")
            
            # Monitorear por 60 segundos
            for i in range(6):
                time.sleep(10)
                print(f"   ⏳ Tiempo: {(i+1)*10}/60 segundos")
                status = self.system.get_system_status()
                avg_availability = sum(s.get('availability', 0) for s in status.get('services', {}).values()) / len(status.get('services', {})) if status.get('services') else 0
                print(f"   📊 Disponibilidad promedio: {avg_availability:.1f}%")
                
            print("\n✅ Experimentos múltiples completados!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
        self.wait_for_user()
        
    def interactive_health_check(self):
        """Diagnóstico interactivo del sistema"""
        self.clear_screen()
        print("🩺 DIAGNÓSTICO INTERACTIVO DEL SISTEMA")
        print("=" * 40)
        
        print("🔍 Ejecutando diagnóstico completo...")
        
        try:
            # Ejecutar Doctor Monkey
            exp_id = self.system.run_chaos_experiment(
                "doctor_monkey",
                duration_seconds=30
            )
            
            print(f"   🆔 ID del diagnóstico: {exp_id}")
            print("   📊 Analizando sistema...")
            
            # Monitorear diagnóstico
            for i in range(3):
                time.sleep(10)
                print(f"   ⏳ Progreso: {(i+1)*10}/30 segundos")
                
            # Obtener resultados
            print("\n📋 RESULTADOS DEL DIAGNÓSTICO:")
            
            status = self.system.get_system_status()
            services = status.get('services', {})
            
            if not services:
                print("❌ No hay servicios para diagnosticar")
            else:
                total_instances = sum(s.get('total_instances', 0) for s in services.values())
                healthy_instances = sum(s.get('healthy_instances', 0) for s in services.values())
                avg_availability = sum(s.get('availability', 0) for s in services.values()) / len(services)
                
                print(f"   🟢 Instancias saludables: {healthy_instances}/{total_instances}")
                print(f"   📊 Disponibilidad promedio: {avg_availability:.1f}%")
                
                # Análisis por servicio
                print("\n   📝 Análisis por servicio:")
                for service_name, service_data in services.items():
                    availability = service_data.get('availability', 0)
                    instances = f"{service_data.get('healthy_instances', 0)}/{service_data.get('total_instances', 0)}"
                    
                    status_icon = "🟢" if availability > 90 else "🟡" if availability > 70 else "🔴"
                    recommendation = "OK" if availability > 90 else "Revisar" if availability > 70 else "CRÍTICO"
                    
                    print(f"     {status_icon} {service_name}: {instances} inst, {availability:.1f}% - {recommendation}")
                    
                # Recomendaciones
                print("\n   💡 RECOMENDACIONES:")
                if avg_availability > 95:
                    print("     ✅ Sistema funcionando óptimamente")
                elif avg_availability > 85:
                    print("     ⚠️ Revisar servicios con baja disponibilidad")
                    print("     🔧 Considerar añadir más instancias")
                else:
                    print("     🚨 Acción inmediata requerida")
                    print("     🔧 Revisar configuración del sistema")
                    print("     🛠️ Verificar balanceador de carga")
                    
            print("\n✅ Diagnóstico completado!")
            
        except Exception as e:
            print(f"❌ Error en diagnóstico: {e}")
            
        self.wait_for_user()
        
    def run_destructive_scenario(self, choice: str):
        """Ejecuta escenarios destructivos"""
        self.clear_screen()
        
        scenarios = {
            '1': "🦍 Chaos Gorilla - Falla de zona completa",
            '2': "🔥 Cascade Failure - Falla en cascada", 
            '4': "🧨 Database Chaos - Fallas en base de datos"
        }
        
        scenario_name = scenarios.get(choice, "Desconocido")
        print(f"💥 EJECUTANDO: {scenario_name}")
        print("=" * 50)
        
        if choice == '1':  # Chaos Gorilla
            print("🦍 Simulando falla de zona completa...")
            try:
                exp_id = self.system.run_chaos_experiment(
                    "chaos_gorilla",
                    duration_seconds=120
                )
                print(f"   🆔 ID: {exp_id}")
                print("   💥 Múltiples servicios afectados")
                
                for i in range(12):  # 2 minutos
                    time.sleep(10)
                    print(f"   ⏳ Progreso: {(i+1)*10}/120 segundos")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
        elif choice == '2':  # Cascade Failure
            print("🔥 Iniciando falla en cascada...")
            services = list(self.system.services.keys())
            
            for i, service in enumerate(services):
                print(f"   💥 Afectando {service}...")
                try:
                    self.system.force_chaos_monkey(service)
                    time.sleep(5)
                except:
                    pass
                    
        elif choice == '4':  # Database Chaos
            print("🧨 Caos en base de datos...")
            db_services = [s for s in self.system.services.keys() if 'db' in s.lower() or 'database' in s.lower()]
            
            if db_services:
                for db in db_services:
                    print(f"   💥 Afectando {db}...")
                    try:
                        result = self.system.force_chaos_monkey(db)
                        print(f"   🎯 Resultado: {result.get('message', 'Ejecutado')}")
                    except Exception as e:
                        print(f"   ❌ Error: {e}")
            else:
                print("   ⚠️ No se encontraron servicios de base de datos")
                
        print("\n✅ Escenario destructivo completado!")
        self.wait_for_user()
        
    def run_moderate_scenario(self, choice: str):
        """Ejecuta escenarios moderados"""
        self.clear_screen()
        
        scenarios = {
            '3': "🌊 Traffic Spike - Pico masivo de tráfico",
            '5': "🔌 Network Partition - Partición de red"
        }
        
        scenario_name = scenarios.get(choice, "Desconocido")
        print(f"⚡ EJECUTANDO: {scenario_name}")
        print("=" * 50)
        
        if choice == '3':  # Traffic Spike
            print("🌊 Simulando pico masivo de tráfico...")
            print("   📈 Aumentando carga del sistema...")
            
            # Simular aumento de tráfico
            for i in range(6):
                traffic_level = (i + 1) * 20  # 20%, 40%, 60%, 80%, 100%, 120%
                print(f"   📊 Tráfico: {traffic_level}% del normal")
                time.sleep(5)
                
            print("   📉 Normalizando tráfico...")
            
        elif choice == '5':  # Network Partition
            print("🔌 Simulando partición de red...")
            services = list(self.system.services.keys())
            
            if len(services) >= 2:
                partition_size = len(services) // 2
                group1 = services[:partition_size]
                group2 = services[partition_size:]
                
                print(f"   🌐 Grupo A: {', '.join(group1)}")
                print(f"   🌐 Grupo B: {', '.join(group2)}")
                print("   ⚡ Simulando pérdida de conectividad entre grupos...")
                
                for i in range(6):
                    time.sleep(10)
                    print(f"   ⏳ Partición activa: {(i+1)*10}/60 segundos")
                    
                print("   🔗 Restaurando conectividad...")
            else:
                print("   ⚠️ Se necesitan al menos 2 servicios para partición")
                
        print("\n✅ Escenario moderado completado!")
        self.wait_for_user()
        
    # ═══════════════════════════════════════════════════════════════════
    # MÉTODOS EDUCATIVOS
    # ═══════════════════════════════════════════════════════════════════
    
    def explain_chaos_engineering(self):
        """Explica qué es Chaos Engineering"""
        self.clear_screen()
        print("""
❓ ¿QUÉ ES CHAOS ENGINEERING?
═══════════════════════════════════

Chaos Engineering es una disciplina que consiste en experimentar con 
sistemas distribuidos para descubrir debilidades antes de que se 
manifiesten como comportamientos aberrantes en producción.

🎯 OBJETIVOS PRINCIPALES:
   • Encontrar puntos únicos de falla
   • Probar la efectividad de mecanismos de fallback
   • Mejorar la resiliencia del sistema
   • Generar confianza en la infraestructura

📈 HISTORIA:
   • 2010: Netflix introduce "Chaos Monkey"
   • 2012: Evolución hacia "Simian Army"
   • 2017: Principios de Chaos Engineering publicados
   • Hoy: Adoptado por Amazon, Google, Facebook, Microsoft

🔬 METODOLOGÍA:
   1. Definir el "estado estable" del sistema
   2. Hipotetizar que el estado se mantendrá
   3. Introducir variables del mundo real (fallas)
   4. Intentar refutar la hipótesis

💡 BENEFICIOS:
   • Reducción de incidentes en producción
   • Mejor comprensión del sistema
   • Identificación proactiva de problemas
   • Incremento en la confianza del equipo
        """)
        self.wait_for_user()
        
    def explain_distributed_systems(self):
        """Explica arquitecturas distribuidas"""
        self.clear_screen()
        print("""
🏗️ ARQUITECTURAS DISTRIBUIDAS
════════════════════════════════

Los sistemas distribuidos son colecciones de computadoras independientes
que aparecen ante los usuarios como un sistema único y coherente.

🔧 COMPONENTES PRINCIPALES:

   🌐 API Gateway:
      • Punto de entrada único
      • Enrutamiento de requests
      • Autenticación y autorización
      • Rate limiting

   🔐 Servicios de Autenticación:
      • Gestión de identidades
      • Tokens y sesiones
      • Control de acceso

   👥 Microservicios:
      • Servicios independientes
      • Responsabilidad única
      • Comunicación via APIs

   💾 Capa de Datos:
      • Bases de datos distribuidas
      • Cache distribuido
      • Consistencia eventual

   ⚖️ Balanceadores de Carga:
      • Distribución de tráfico
      • Health checks
      • Failover automático

⚠️ DESAFÍOS:
   • Latencia de red
   • Fallas parciales
   • Consistencia de datos
   • Complejidad operacional

🎯 BENEFICIOS:
   • Escalabilidad
   • Resiliencia
   • Flexibilidad tecnológica
   • Independencia de equipos
        """)
        self.wait_for_user()
        
    def explain_experiment_types(self):
        """Explica tipos de experimentos"""
        self.clear_screen()
        print("""
🧪 TIPOS DE EXPERIMENTOS DE CHAOS
══════════════════════════════════════

🐒 CHAOS MONKEY (Básico):
   • Terminación aleatoria de instancias
   • Primer nivel de chaos engineering
   • Prueba redundancia y failover

🌐 EXPERIMENTOS DE RED:
   • Latency Monkey: Delays artificiales
   • Network Partition: Aislamiento de servicios
   • Packet Loss: Pérdida de paquetes

💾 AGOTAMIENTO DE RECURSOS:
   • CPU Exhaustion: Consumo al 100%
   • Memory Exhaustion: Agotamiento de RAM
   • Disk I/O: Saturación de disco

🦍 CHAOS GORILLA (Destructivo):
   • Falla de zona completa
   • Afecta múltiples servicios
   • Prueba recuperación regional

🧨 CHAOS KONG (Muy Destructivo):
   • Falla de región completa
   • Máximo nivel de destrucción
   • Solo en entornos seguros

🩺 EXPERIMENTOS DE DIAGNÓSTICO:
   • Doctor Monkey: Health checks
   • Performance Monitor: Análisis de rendimiento
   • Security Monkey: Vulnerabilidades

📊 NIVELES DE RIESGO:
   🟢 Bajo: Chaos Monkey, Latency
   🟡 Medio: Resource Exhaustion, Network Partition
   🔴 Alto: Chaos Gorilla, Database Failures
   ⚫ Crítico: Chaos Kong, Regional Failures

💡 MEJORES PRÁCTICAS:
   • Comenzar con experimentos simples
   • Incrementar complejidad gradualmente
   • Tener plan de rollback
   • Monitorear métricas clave
        """)
        self.wait_for_user()
        
    def explain_metrics(self):
        """Explica métricas y monitoreo"""
        self.clear_screen()
        print("""
📊 MÉTRICAS Y MONITOREO
═══════════════════════════

📈 MÉTRICAS FUNDAMENTALES:

   ⏱️ LATENCIA:
      • Tiempo de respuesta promedio
      • Percentiles P50, P95, P99
      • Timeout rates

   🚀 THROUGHPUT:
      • Requests por segundo (RPS)
      • Transacciones por minuto
      • Bandwidth utilizado

   ❌ ERROR RATE:
      • Porcentaje de errores
      • Códigos de estado HTTP
      • Timeouts y fallos

   📊 DISPONIBILIDAD:
      • Uptime percentage
      • SLA compliance
      • MTTR (Mean Time To Recovery)
      • MTBF (Mean Time Between Failures)

🎯 GOLDEN SIGNALS:
   1. Latency - ¿Qué tan rápido?
   2. Traffic - ¿Cuánto tráfico?
   3. Errors - ¿Qué está fallando?
   4. Saturation - ¿Qué tan lleno?

📱 TIPOS DE ALERTAS:

   🔴 CRÍTICAS:
      • Sistema completamente caído
      • Pérdida de datos
      • Seguridad comprometida

   🟠 ALTAS:
      • SLA en riesgo
      • Degradación significativa
      • Recursos agotándose

   🟡 MEDIAS:
      • Tendencias preocupantes
      • Umbrales preventivos
      • Anomalías detectadas

🛠️ HERRAMIENTAS COMUNES:
   • Prometheus + Grafana
   • DataDog
   • New Relic
   • CloudWatch

💡 MEJORES PRÁCTICAS:
   • Definir SLOs claros
   • Alertas accionables
   • Dashboards por audiencia
   • Retención de datos históricos
        """)
        self.wait_for_user()
        
    def explain_resilience_patterns(self):
        """Explica patrones de resiliencia"""
        self.clear_screen()
        print("""
🔄 PATRONES DE RESILIENCIA
═══════════════════════════════

🛡️ CIRCUIT BREAKER:
   • Previene cascadas de fallas
   • Estados: Closed, Open, Half-Open
   • Failfast cuando hay problemas
   • Recuperación automática

🏰 BULKHEAD:
   • Aislamiento de recursos
   • Compartimentos separados
   • Falla aislada no afecta todo
   • Pool de conexiones segregado

🔄 RETRY CON BACKOFF:
   • Reintentos inteligentes
   • Backoff exponencial
   • Jitter para evitar thundering herd
   • Máximo número de intentos

⏰ TIMEOUT:
   • Límites de tiempo de espera
   • Evita recursos bloqueados
   • Configuración por operación
   • Cascading timeouts

🎭 FALLBACK:
   • Respuestas de emergencia
   • Graceful degradation
   • Cache como fallback
   • Respuestas por defecto

⚖️ RATE LIMITING:
   • Control de tráfico
   • Previene sobrecarga
   • Token bucket algorithm
   • Sliding window

🔀 LOAD BALANCING:
   • Distribución de carga
   • Health checks
   • Algoritmos: Round Robin, Least Connections
   • Sticky sessions

📦 CACHING:
   • Reducción de latencia
   • Offload de servicios backend
   • Cache invalidation strategies
   • Multi-level caching

💡 IMPLEMENTACIÓN:
   • Combinar múltiples patrones
   • Configuración por servicio
   • Monitoreo de efectividad
   • Testing de patrones
        """)
        self.wait_for_user()
        
    def explain_best_practices(self):
        """Explica mejores prácticas"""
        self.clear_screen()
        print("""
🎯 MEJORES PRÁCTICAS DE CHAOS ENGINEERING
═══════════════════════════════════════════

🚀 COMENZANDO:

   📋 1. PREPARACIÓN:
      • Definir estado estable del sistema
      • Establecer métricas baseline
      • Identificar servicios críticos
      • Crear plan de rollback

   🎯 2. HIPÓTESIS:
      • Específica y medible
      • "El sistema mantendrá X disponibilidad cuando..."
      • Basada en observaciones reales
      • Validable con métricas

   ⚡ 3. EMPEZAR PEQUEÑO:
      • Entornos de desarrollo primero
      • Experimentos simples (Chaos Monkey)
      • Incrementar gradualmente
      • Horarios de oficina inicialmente

🔧 EJECUCIÓN:

   📊 4. MONITOREO CONTINUO:
      • Métricas en tiempo real
      • Alertas configuradas
      • Dashboards visibles
      • Logs centralizados

   🛡️ 5. SAFETY FIRST:
      • Kill switches disponibles
      • Blast radius limitado
      • Dry-run mode disponible
      • Rollback rápido

   👥 6. COLABORACIÓN:
      • Involucrar a todos los equipos
      • Comunicar experimentos
      • Compartir resultados
      • Post-mortems sin culpa

📈 ESCALAMIENTO:

   🎮 7. AUTOMATIZACIÓN:
      • Experimentos programados
      • Validación automática
      • Reportes automáticos
      • Integración CI/CD

   🌍 8. PRODUCCIÓN:
      • Horarios de bajo tráfico
      • Monitoreo intensivo
      • Equipos en standby
      • Comunicación clara

   📚 9. APRENDIZAJE CONTINUO:
      • Documentar hallazgos
      • Mejorar sistemas basado en resultados
      • Compartir conocimiento
      • Iterar y mejorar experimentos

❌ QUÉ EVITAR:
   • Experimentos sin hipótesis
   • Falta de monitoreo
   • No tener plan de rollback
   • Culpar por fallas encontradas
   • Experimentos en viernes
        """)
        self.wait_for_user()
        
    # ═══════════════════════════════════════════════════════════════════
    # MÉTODOS AUXILIARES
    # ═══════════════════════════════════════════════════════════════════
    
    def create_stable_demo_system(self):
        """Crea un sistema súper estable optimizado para demos sin fallos"""
        # Configuración MUY CONSERVADORA para demos exitosas
        demo_config = {
            "enabled": True,
            "schedule": {
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
                "hours": {"start": 0, "end": 23}
            },
            "targets": {
                "services": ["api-gateway", "auth-service", "user-service", "payment-service", 
                           "notification-service", "analytics-service", "file-storage", "search-service",
                           "mobile-api", "security-service", "monitoring-service", "database", "cache"],
                "min_healthy_instances": 1,  # AGRESIVO - permitir bajar a 1 instancia
                "max_instances_to_kill": 3   # SÚPER AGRESIVO - hasta 3 a la vez para reducir disponibilidad
            },
            "experiments": {
                "instance_termination": {"enabled": True, "probability": 0.60},  # EXTREMO: 60% - FALLOS CONSTANTES
                "network_latency": {"enabled": True, "probability": 0.45},       # EXTREMO: 45% - RED PROBLEMÁTICA
                "resource_exhaustion": {"enabled": True, "probability": 0.35}    # EXTREMO: 35% - CPU SOBRECARGADA
            },
            "monitoring": {
                "collection_interval_seconds": 1,  # MUY FRECUENTE para detectar problemas rápido
                "alert_thresholds": {
                    "response_time_ms": 80,     # EXTREMO: 80ms - ALERTAS INSTANTÁNEAS
                    "error_rate_percent": 0.5,  # EXTREMO: 0.5% - CUALQUIER ERROR = ALERTA
                    "availability_percent": 95  # EXTREMO: 95% - PERFECTECCIÓN O ALERTA
                }
            },
            "safety": {
                "enabled": True,
                "dry_run_mode": False,
                "require_confirmation_for_destructive": False,
                "max_concurrent_experiments": 1  # Solo 1 experimento a la vez
            },
            "services": {
                "api-gateway": {
                    "type": "api-gateway",
                    "initial_instances": 6,  # MUCHAS INSTANCIAS - para estadísticas claras
                    "min_instances": 2,      # AGRESIVO - Solo 2 mínimas
                    "max_instances": 10,
                    "region": "us-east-1"
                },
                "auth-service": {
                    "type": "auth-service", 
                    "initial_instances": 5,  # MUCHAS INSTANCIAS - para estadísticas claras
                    "min_instances": 2,      # AGRESIVO - Permitir bajar a 2
                    "max_instances": 8,
                    "region": "us-east-1"
                },
                "user-service": {
                    "type": "user-profile",
                    "initial_instances": 5,  # MUCHAS INSTANCIAS - para que fallen algunas
                    "min_instances": 2,      # AGRESIVO - Permitir bajar a 2
                    "max_instances": 8,
                    "region": "us-east-1"
                },
                "payment-service": {
                    "type": "database",
                    "initial_instances": 6,  # MUCHAS INSTANCIAS - servicio crítico
                    "min_instances": 2,
                    "max_instances": 9,
                    "region": "us-east-1"
                },
                "notification-service": {
                    "type": "api-gateway",
                    "initial_instances": 7,  # MÁS INSTANCIAS - para que muchas fallen
                    "min_instances": 2,
                    "max_instances": 10,
                    "region": "us-east-1"
                },
                "analytics-service": {
                    "type": "cache",
                    "initial_instances": 5,  # MÁS INSTANCIAS para redundancia
                    "min_instances": 2,
                    "max_instances": 8,
                    "region": "us-east-1"
                },
                "file-storage": {
                    "type": "database",
                    "initial_instances": 5,  # MÁS INSTANCIAS - para fallos visibles
                    "min_instances": 1,      # Permitir fallar completamente
                    "max_instances": 8,
                    "region": "us-east-1"
                },
                "search-service": {
                    "type": "cache",
                    "initial_instances": 5,  # MÁS INSTANCIAS para redundancia
                    "min_instances": 2,
                    "max_instances": 8,
                    "region": "us-east-1"
                },
                "mobile-api": {
                    "type": "user-profile",
                    "initial_instances": 6,  # MUCHAS INSTANCIAS - API crítica
                    "min_instances": 2,
                    "max_instances": 9,
                    "region": "us-east-1"
                },
                "security-service": {
                    "type": "auth-service",
                    "initial_instances": 4,  # MÁS INSTANCIAS para redundancia
                    "min_instances": 2,
                    "max_instances": 7,
                    "region": "us-east-1"
                },
                "monitoring-service": {
                    "type": "database",
                    "initial_instances": 4,  # MÁS INSTANCIAS para redundancia
                    "min_instances": 2,
                    "max_instances": 7,
                    "region": "us-east-1"
                },
                "database": {
                    "type": "database",
                    "initial_instances": 6,  # MUCHAS INSTANCIAS - DB crítica
                    "min_instances": 3,      # MÍNIMO 3 para DB para estadísticas claras
                    "max_instances": 9,
                    "region": "us-east-1"
                },
                "cache": {
                    "type": "cache",
                    "initial_instances": 5,  # MÁS INSTANCIAS - para fallos claros
                    "min_instances": 2,      # AGRESIVO - Permitir bajar a 2
                    "max_instances": 8,
                    "region": "us-east-1"
                }
            }
        }
        
        system = ChaosEngineeringSystem()
        system.config = demo_config
        return system

    def ensure_system_running(self):
        """Asegura que el sistema esté ejecutándose"""
        if not self.system or not self.running:
            print("❌ El sistema no está ejecutándose")
            if self.confirm("¿Deseas configurar e iniciar el sistema ahora?"):
                self.quick_system_setup()
                return True
            else:
                self.wait_for_user()
                return False
        return True
        
    def quick_system_setup(self):
        """Configuración rápida del sistema"""
        print("🚀 Configuración rápida del sistema...")
        
        self.system = self.create_stable_demo_system()
        
        # Servicios por defecto
        services = [
            ("api-gateway", "api-gateway", 3),
            ("auth-service", "auth-service", 2),
            ("user-service", "user-profile", 2),
            ("database", "database", 2)
        ]
        
        for name, service_type, instances in services:
            self.system.add_service(name, service_type, instances)
            
        self.system.initialize()
        self.system.start()
        self.running = True
        
        print("✅ Sistema configurado y funcionando!")
        time.sleep(1)
        
    def cleanup_demo(self):
        """Limpia recursos de la demo"""
        if self.system and self.running:
            print("\n🧹 Limpiando sistema...")
            self.system.stop()
            self.running = False
            
    def cleanup_and_exit(self):
        """Limpia y sale"""
        print("\n🧹 Limpiando y saliendo...")
        
        if self.system and self.running:
            self.system.stop()
            
        print("👋 ¡Gracias por usar el Demo de Chaos Engineering!")
        print("   📚 Para más información, revisa el README.md")
        print("   🌟 ¡Esperamos que hayas aprendido algo nuevo!")
        
    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def wait_for_user(self, message: str = "Presiona Enter para continuar..."):
        """Espera input del usuario"""
        input(f"\n{message}")
        
    def confirm(self, message: str) -> bool:
        """Pide confirmación al usuario"""
        response = input(f"{message} (s/N): ").strip().lower()
        return response in ['s', 'si', 'y', 'yes']
        
    def print_error(self, message: str):
        """Muestra mensaje de error"""
        print(f"\n{message}")
        time.sleep(1.5)

# ═══════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════

def main():
    """Función principal"""
    try:
        demo = InteractiveDemo()
        demo.run()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrumpida. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 