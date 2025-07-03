#!/usr/bin/env python3
"""
Ejemplo de monitoreo y dashboards en tiempo real.
Demuestra las capacidades de observabilidad del sistema
durante experimentos de chaos engineering.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chaos_system import ChaosEngineeringSystem
import time
import threading

def configure_services(system):
    print("1. Configurando servicios con diferentes cargas...")
    system.add_service("frontend", "web", instances=4)
    system.add_service("api-users", "api", instances=3)
    system.add_service("api-orders", "api", instances=3)
    system.add_service("cache-redis", "cache", instances=2)
    system.add_service("db-primary", "database", instances=1)
    system.add_service("db-replica", "database", instances=2)
    system.initialize_components()

def configure_alerts(monitoring):
    if monitoring:
        monitoring.add_alert_rule(
            name="high_latency",
            metric="response_time",
            threshold=2000,
            condition="greater_than",
            action="log_warning"
        )
        monitoring.add_alert_rule(
            name="low_availability",
            metric="availability",
            threshold=0.95,
            condition="less_than",
            action="log_critical"
        )
        print("   ✓ Alertas configuradas (latencia alta, disponibilidad baja)")

def show_dashboard(system):
    if not system.monitoring:
        return
    print("\n" + "="*80)
    print("📊 DASHBOARD DE MONITOREO EN TIEMPO REAL")
    print("="*80)
    system_metrics = system.monitoring.get_system_metrics()
    print(f"🏥 Estado del Sistema: {'🟢 SALUDABLE' if system_metrics.get('healthy', True) else '🔴 CRÍTICO'}")
    print(f"⚡ Throughput Total: {system_metrics.get('total_throughput', 0):.1f} req/s")
    print(f"⏱️  Latencia Promedio: {system_metrics.get('avg_response_time', 0):.1f}ms")
    print(f"✅ Disponibilidad: {system_metrics.get('availability', 0)*100:.1f}%")
    print("\n📈 MÉTRICAS POR SERVICIO:")
    print("-" * 80)
    for service_name, service in system.services.items():
        metrics = service.get_metrics()
        health = service.health_check()
        if health['status'] == 'healthy':
            status_icon = "🟢"
        elif health['status'] == 'unhealthy':
            status_icon = "🔴"
        else:
            status_icon = "🟡"
        print(f"{status_icon} {service_name:<15} | "
              f"Instancias: {metrics.get('healthy_instances', 0)}/{metrics.get('total_instances', 0)} | "
              f"CPU: {metrics.get('cpu_usage', 0):.1f}% | "
              f"Memoria: {metrics.get('memory_usage', 0):.1f}% | "
              f"Latencia: {metrics.get('avg_response_time', 0):.1f}ms | "
              f"Requests: {metrics.get('requests_per_minute', 0):.0f}/min")
    active_alerts = system.monitoring.get_active_alerts()
    if active_alerts:
        print(f"\n🚨 ALERTAS ACTIVAS ({len(active_alerts)}):")
        print("-" * 50)
        for alert in active_alerts[-5:]:
            timestamp = time.strftime("%H:%M:%S", time.localtime(alert.get('timestamp', time.time())))
            print(f"[{timestamp}] {alert.get('level', 'INFO').upper()}: {alert.get('message', 'N/A')}")
    print("="*80)

def generate_variable_traffic(system):
    patterns = [
        {"duration": 30, "rps": 50},
        {"duration": 20, "rps": 150},
        {"duration": 25, "rps": 30},
        {"duration": 15, "rps": 200},
    ]
    for pattern in patterns:
        print(f"\n🌊 Cambiando patrón de tráfico: {pattern['rps']} req/s por {pattern['duration']}s")
        system.simulate_traffic(duration=pattern['duration'], requests_per_second=pattern['rps'])

def introduce_chaos(system, cycle):
    if cycle == 2:
        print("\n💥 INTRODUCIENDO CHAOS: Terminando instancia de api-users...")
        result = system.chaos_monkey.force_chaos("api-users")
        print(f"   Resultado: {result.get('message', 'N/A')}")
    elif cycle == 4:
        print("\n💥 INTRODUCIENDO CHAOS: Simulando outage en cache-redis...")
        result = system.chaos_monkey.simulate_outage("cache-redis", instance_count=1)
        print(f"   Resultado: {result.get('message', 'N/A')}")
    elif cycle == 6:
        print("\n💥 INTRODUCIENDO CHAOS: Experimento de latencia en frontend...")
        if "frontend" in system.services:
            system.services["frontend"].chaos_introduce_latency(1500)
            print("   Latencia de 1500ms aplicada al frontend")

def analyze_trends(system):
    print("\n5. Análisis de tendencias...")
    if system.monitoring:
        trends = system.monitoring.analyze_trends(hours=1)
        print("   📊 Tendencias detectadas:")
        for metric, trend in trends.items():
            if trend > 0:
                direction = "📈 Subiendo"
            elif trend < 0:
                direction = "📉 Bajando"
            else:
                direction = "➡️ Estable"
            print(f"      {metric}: {direction} ({trend:+.2f})")

def show_recommendations(system):
    print("\n6. Recomendaciones del sistema...")
    recommendations = system.monitoring.get_recommendations()
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"   {i}. {rec}")

def generate_report(system):
    print("\n7. Generando reporte de monitoreo...")
    report_path = system.generate_report()
    print(f"   Reporte completo disponible en: {report_path}")

def monitoring_dashboard_example():
    print("=== Ejemplo de Monitoreo y Dashboard en Tiempo Real ===\n")
    system = ChaosEngineeringSystem()
    configure_services(system)
    print("2. Iniciando sistema de monitoreo...")
    system.start()
    configure_alerts(system.monitoring)
    print("3. Iniciando simulación de tráfico variable...")
    traffic_thread = threading.Thread(target=generate_variable_traffic, args=(system,), daemon=True)
    traffic_thread.start()
    print("4. Iniciando monitoreo en tiempo real...")
    print("   (El dashboard se actualizará cada 15 segundos)")
    show_dashboard(system)
    monitor_cycles = 8
    for cycle in range(monitor_cycles):
        time.sleep(15)
        print(f"\n🔄 Actualización {cycle + 1}/{monitor_cycles}")
        show_dashboard(system)
        introduce_chaos(system, cycle)
    analyze_trends(system)
    show_recommendations(system)
    generate_report(system)
    system.stop()
    print("\n=== Monitoreo Completado ===")
    print("\nCapacidades demostradas:")
    print("✓ Dashboard en tiempo real con métricas clave")
    print("✓ Alertas automáticas basadas en umbrales")
    print("✓ Monitoreo por servicio e instancia")
    print("✓ Análisis de tendencias y patrones")
    print("✓ Recomendaciones automáticas")
    print("✓ Respuesta del sistema ante fallas")

if __name__ == "__main__":
    monitoring_dashboard_example()
