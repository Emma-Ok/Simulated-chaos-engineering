#!/usr/bin/env python3
"""
🔥 DEMO SÚPER SIMPLE - CHAOS ENGINEERING

EJECUTAR ESTE ARCHIVO:
    python demo.py

¡La forma más fácil de ver Chaos Engineering en acción!
"""

import sys
import time

def main():
    print("\n" + "=" * 60)
    print("🔥 DEMO SÚPER SIMPLE DE CHAOS ENGINEERING")
    print("=" * 60)
    print("🚀 Iniciando automáticamente...")
    print("📊 Duración: ~5-6 minutos")
    print("🎯 Todo automático - solo observa y aprende")
    print("🔥 Configuración AGRESIVA para máximo aprendizaje")
    print("=" * 60 + "\n")
    
    print("💡 Lo que verás (SÚPER EDUCATIVO CON MÁXIMA REDUNDANCIA):")
    print("   🏗️ Sistema de 13 SERVICIOS con 70+ INSTANCIAS total")
    print("   📊 ESTADÍSTICAS CLARAS: 4/6, 3/7, 2/5 instancias activas")
    print("   💥 SERVICIOS FALLANDO con disponibilidades: 60%-95%")
    print("   🚨 ALERTAS CRÍTICAS constantes (configuración estricta)")
    print("   ⚡ Experimentos EXTREMOS que causan caos masivo")
    print("   🔄 Auto-scaling VISIBLE luchando por recuperar servicios")
    print("   📈 Gráficas mostrando TENDENCIAS claras de fallos/recuperación")
    print("   🎯 ¡NUNCA más 100% disponibilidad - solo estadísticas REALES!")
    print("\n" + "⏳ Comenzando en 3 segundos..." + "\n")
    time.sleep(3)
    
    try:
        # Importar y ejecutar demo directamente
        from run_demo import InteractiveDemo
        
        demo = InteractiveDemo()
        
        # Configurar sistema automáticamente
        print("🏗️ Configurando sistema súper estable...")
        demo.system = demo.create_stable_demo_system()
        
        # Ejecutar demo rápida directamente
        demo.quick_demo()
        
        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("📊 Revisa el reporte HTML en la carpeta 'reports/'")
        print("🔥 Para más opciones usa: python run_demo.py")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrumpida. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Soluciones:")
        print("   1. python run_demo.py  (versión alternativa)")
        print("   2. pip install -r requirements.txt  (dependencias)")
        print("   3. Ver SOLUCION_PROBLEMAS.md")

if __name__ == "__main__":
    main() 