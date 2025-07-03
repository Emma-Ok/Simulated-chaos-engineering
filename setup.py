#!/usr/bin/env python3
"""
Script de setup y verificación para el Simulador de Chaos Engineering
"""

import sys
import subprocess
import os
import importlib

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    print("🐍 Verificando versión de Python...")
    
    if sys.version_info < (3, 7):
        print("❌ ERROR: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def install_requirements():
    """Instala las dependencias requeridas"""
    print("\n📦 Instalando dependencias...")
    
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ ERROR: No se encontró {requirements_file}")
        return False
    
    try:
        # Instalar dependencias
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ], capture_output=True, text=True, check=True)
        
        print("✅ Dependencias instaladas exitosamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR instalando dependencias: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False

def verify_imports():
    """Verifica que todos los módulos se puedan importar"""
    print("\n🔍 Verificando importaciones...")
    
    required_modules = [
        ("matplotlib", "Visualización de gráficos"),
        ("plotly", "Gráficos interactivos"),
        ("yaml", "Configuración YAML"),
        ("psutil", "Métricas del sistema"),
        ("colorama", "Colores en terminal"),
        ("tabulate", "Tablas en terminal")
    ]
    
    all_good = True
    
    for module_name, description in required_modules:
        try:
            importlib.import_module(module_name)
            print(f"  ✅ {module_name:<12} - {description}")
        except ImportError:
            print(f"  ❌ {module_name:<12} - {description} (FALTANTE)")
            all_good = False
    
    return all_good

def verify_project_structure():
    """Verifica que la estructura del proyecto esté completa"""
    print("\n📁 Verificando estructura del proyecto...")
    
    required_dirs = [
        ("core/", "Módulos principales"),
        ("chaos/", "Módulos de chaos engineering"),
        ("config/", "Archivos de configuración"),
        ("utils/", "Utilidades"),
        ("examples/", "Ejemplos de uso"),
        ("tests/", "Tests unitarios"),
        ("reports/", "Reportes generados")
    ]
    
    required_files = [
        ("main.py", "Script principal"),
        ("chaos_system.py", "Sistema principal"),
        ("requirements.txt", "Dependencias"),
        ("README.md", "Documentación")
    ]
    
    all_good = True
    
    # Verificar directorios
    for dir_path, description in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"  ✅ {dir_path:<15} - {description}")
        else:
            print(f"  ❌ {dir_path:<15} - {description} (FALTANTE)")
            all_good = False
    
    # Verificar archivos
    for file_path, description in required_files:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            print(f"  ✅ {file_path:<15} - {description}")
        else:
            print(f"  ❌ {file_path:<15} - {description} (FALTANTE)")
            all_good = False
    
    return all_good

def test_basic_functionality():
    """Ejecuta un test básico del sistema"""
    print("\n🧪 Ejecutando test básico...")
    
    try:
        # Importar y probar el sistema principal
        from chaos_system import ChaosEngineeringSystem
        
        # Crear instancia del sistema
        system = ChaosEngineeringSystem()
        
        # Agregar un servicio de prueba
        success = system.add_service("test-service", "database", instances=2)
        
        if success:
            print("  ✅ Sistema se inicializa correctamente")
            print("  ✅ Servicios se pueden agregar")
            
            # Inicializar componentes
            system.initialize_components()
            print("  ✅ Componentes se inicializan correctamente")
            
            return True
        else:
            print("  ❌ Error agregando servicio de prueba")
            return False
            
    except Exception as e:
        print(f"  ❌ ERROR en test básico: {e}")
        return False

def create_reports_directory():
    """Crea el directorio de reportes si no existe"""
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        print(f"📁 Directorio {reports_dir}/ creado")

def show_next_steps():
    """Muestra los próximos pasos para el usuario"""
    print("\n" + "="*60)
    print("🎉 ¡SETUP COMPLETADO EXITOSAMENTE!")
    print("="*60)
    
    print("\n📚 PRÓXIMOS PASOS:")
    print()
    print("1️⃣  Ejecutar ejemplo básico:")
    print("    python examples/quick_start.py")
    print()
    print("2️⃣  Ejecutar simulación completa:")
    print("    python examples/basic_simulation.py")
    print()
    print("3️⃣  Explorar experimentos avanzados:")
    print("    python examples/advanced_experiments.py")
    print()
    print("4️⃣  Ejecutar modo interactivo:")
    print("    python main.py")
    print()
    print("5️⃣  Ejecutar tests:")
    print("    python tests/run_tests.py")
    print()
    print("📖 DOCUMENTACIÓN:")
    print("    - README.md (documentación principal)")
    print("    - examples/README.md (guía de ejemplos)")
    print("    - tests/README.md (guía de tests)")
    print()
    print("🆘 SOPORTE:")
    print("    - Si encuentras problemas, revisa los logs")
    print("    - Ejecuta tests para verificar funcionalidad")
    print("    - Consulta la documentación en README.md")
    print()

def main():
    """Función principal del setup"""
    print("="*60)
    print("🔧 SETUP - SIMULADOR DE CHAOS ENGINEERING")
    print("="*60)
    
    # Lista de verificaciones
    checks = [
        ("Versión de Python", check_python_version),
        ("Instalación de dependencias", install_requirements),
        ("Verificación de imports", verify_imports),
        ("Estructura del proyecto", verify_project_structure),
        ("Test básico", test_basic_functionality)
    ]
    
    # Ejecutar verificaciones
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
                print(f"\n⚠️  {check_name} falló")
        except Exception as e:
            print(f"\n💥 Error en {check_name}: {e}")
            all_passed = False
    
    # Crear directorio de reportes
    create_reports_directory()
    
    if all_passed:
        show_next_steps()
        return 0
    else:
        print("\n" + "="*60)
        print("❌ SETUP INCOMPLETO")
        print("="*60)
        print("\nAlgunos checks fallaron. Por favor:")
        print("1. Revisa los errores mostrados arriba")
        print("2. Instala las dependencias faltantes")
        print("3. Ejecuta el setup nuevamente")
        print()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
