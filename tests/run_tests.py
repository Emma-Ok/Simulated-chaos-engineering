#!/usr/bin/env python3
"""
Script para ejecutar todos los tests del simulador de Chaos Engineering
"""

import unittest
import sys
import os

# Agregar el directorio del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def run_all_tests():
    """Ejecuta todos los tests disponibles"""
    
    print("="*70)
    print("🧪 EJECUTANDO TESTS DEL SIMULADOR DE CHAOS ENGINEERING")
    print("="*70)
    
    # Configurar logging para tests (reducir verbosidad)
    import logging
    logging.basicConfig(level=logging.ERROR)
    
    # Descubrir y cargar todos los tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cargar todos los tests que comienzan con 'test_'
    test_suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Configurar el runner con verbosidad
    runner = unittest.TextTestRunner(
        verbosity=2,
        descriptions=True,
        failfast=False  # Continuar ejecutando tests aunque algunos fallen
    )
    
    print(f"📁 Buscando tests en: {start_dir}")
    print(f"🔍 Tests encontrados: {test_suite.countTestCases()}")
    print()
    
    # Ejecutar los tests
    result = runner.run(test_suite)
    
    # Mostrar resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*70)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    passed = total_tests - failures - errors - skipped
    
    print(f"✅ Tests ejecutados: {total_tests}")
    print(f"🟢 Exitosos: {passed}")
    print(f"🔴 Fallidos: {failures}")
    print(f"⚠️  Errores: {errors}")
    print(f"⏭️  Omitidos: {skipped}")
    
    if failures > 0:
        print(f"\n❌ TESTS FALLIDOS ({failures}):")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"  {i}. {test}")
    
    if errors > 0:
        print(f"\n💥 TESTS CON ERRORES ({errors}):")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"  {i}. {test}")
    
    # Calcular porcentaje de éxito
    if total_tests > 0:
        success_rate = (passed / total_tests) * 100
        print(f"\n📈 Tasa de éxito: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 ¡Excelente! Los tests están pasando correctamente.")
        elif success_rate >= 70:
            print("👍 Bien, pero hay algunos tests que necesitan atención.")
        else:
            print("⚠️  Atención: Muchos tests están fallando. Revisar implementación.")
    
    print("="*70)
    
    # Retornar código de salida apropiado
    return 0 if (failures == 0 and errors == 0) else 1

def run_specific_test_module(module_name):
    """Ejecuta tests de un módulo específico"""
    
    print(f"🧪 Ejecutando tests del módulo: {module_name}")
    print("-" * 50)
    
    # Configurar logging
    import logging
    logging.basicConfig(level=logging.ERROR)
    
    # Cargar el módulo específico
    loader = unittest.TestLoader()
    
    try:
        test_suite = loader.loadTestsFromName(module_name)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(test_suite)
        
        # Mostrar resultado
        if result.wasSuccessful():
            print(f"✅ Todos los tests de {module_name} pasaron exitosamente!")
            return 0
        else:
            print(f"❌ Algunos tests de {module_name} fallaron.")
            return 1
            
    except Exception as e:
        print(f"💥 Error al ejecutar tests de {module_name}: {e}")
        return 1

def show_available_tests():
    """Muestra los tests disponibles"""
    
    print("📋 TESTS DISPONIBLES:")
    print("="*50)
    
    test_files = [
        ("test_service.py", "Tests para servicios e instancias"),
        ("test_chaos_monkey.py", "Tests para Chaos Monkey"),
        ("test_integration.py", "Tests de integración del sistema")
    ]
    
    for filename, description in test_files:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        status = "✅" if os.path.exists(filepath) else "❌"
        print(f"  {status} {filename:<20} - {description}")
    
    print("\nUso:")
    print("  python run_tests.py                    # Ejecutar todos los tests")
    print("  python run_tests.py test_service       # Ejecutar tests específicos")
    print("  python run_tests.py --list             # Mostrar tests disponibles")

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg in ["--list", "-l", "list"]:
            show_available_tests()
            sys.exit(0)
        else:
            # Ejecutar módulo específico
            exit_code = run_specific_test_module(arg)
            sys.exit(exit_code)
    else:
        # Ejecutar todos los tests
        exit_code = run_all_tests()
        sys.exit(exit_code)
