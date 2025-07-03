# Tests - Simulador de Chaos Engineering

Esta carpeta contiene los tests unitarios e integración para validar el funcionamiento del simulador de Chaos Engineering.

## Estructura de Tests

```
tests/
├── test_service.py         # Tests para servicios e instancias
├── test_chaos_monkey.py    # Tests para Chaos Monkey
├── test_integration.py     # Tests de integración del sistema
├── run_tests.py           # Script para ejecutar todos los tests
└── README.md              # Esta documentación
```

## Tipos de Tests

### 1. Tests Unitarios

#### `test_service.py`
- **TestServiceInstance**: Tests para instancias individuales de servicios
  - Creación y configuración de instancias
  - Health checks y métricas
  - Procesamiento de requests
  - Operaciones de chaos (terminación, latencia, agotamiento de recursos)
  - Auto-restart y recuperación

- **TestService**: Tests para servicios completos
  - Gestión de múltiples instancias
  - Balanceo de carga entre instancias
  - Auto-scaling basado en métricas
  - Operaciones de chaos a nivel servicio
  - Recolección de métricas agregadas

#### `test_chaos_monkey.py`
- **TestChaosMonkey**: Tests para el motor de Chaos Engineering
  - Configuración y reglas de seguridad
  - Selección de objetivos
  - Ejecución de experimentos
  - Bloqueo por reglas de seguridad
  - Simulación de outages
  - Recolección de estadísticas
  - Exclusión temporal de servicios
  - Sistema de callbacks

### 2. Tests de Integración

#### `test_integration.py`
- **TestChaosEngineeringSystemIntegration**: Tests del sistema completo
  - Inicialización de todos los componentes
  - Integración entre módulos
  - Simulación de tráfico
  - Experimentos de chaos end-to-end
  - Generación de reportes
  - Resiliencia ante múltiples fallas
  - Configuración desde archivos

## Ejecutar Tests

### Todos los tests
```bash
python tests/run_tests.py
```

### Tests específicos
```bash
# Tests de servicios
python tests/run_tests.py test_service

# Tests de Chaos Monkey
python tests/run_tests.py test_chaos_monkey

# Tests de integración
python tests/run_tests.py test_integration
```

### Tests individuales
```bash
# Ejecutar archivo específico
python -m unittest tests.test_service -v

# Ejecutar clase específica
python -m unittest tests.test_service.TestService -v

# Ejecutar test específico
python -m unittest tests.test_service.TestService.test_service_creation -v
```

### Listar tests disponibles
```bash
python tests/run_tests.py --list
```

## Cobertura de Tests

Los tests cubren los siguientes aspectos:

### ✅ Funcionalidad Core
- [x] Creación y gestión de servicios
- [x] Instancias de servicios y health checks
- [x] Balanceo de carga
- [x] Métricas y monitoreo
- [x] Auto-scaling

### ✅ Chaos Engineering
- [x] Configuración de Chaos Monkey
- [x] Terminación de instancias
- [x] Reglas de seguridad
- [x] Simulación de outages
- [x] Estadísticas y historial

### ✅ Integración del Sistema
- [x] Inicialización completa
- [x] Comunicación entre componentes
- [x] Simulación de tráfico
- [x] Experimentos end-to-end
- [x] Generación de reportes

### ✅ Resiliencia
- [x] Recuperación automática
- [x] Múltiples fallas simultáneas
- [x] Degradación gradual
- [x] Mantenimiento de servicios críticos

## Interpretación de Resultados

### Resultados Exitosos
```
======================================================================
📊 RESUMEN DE RESULTADOS
======================================================================
✅ Tests ejecutados: 45
🟢 Exitosos: 43
🔴 Fallidos: 2
⚠️  Errores: 0
⏭️  Omitidos: 0

📈 Tasa de éxito: 95.6%
🎉 ¡Excelente! Los tests están pasando correctamente.
```

### Interpretación de Métricas
- **Tasa de éxito >= 90%**: Sistema funcionando correctamente
- **Tasa de éxito 70-89%**: Algunas funcionalidades necesitan revisión
- **Tasa de éxito < 70%**: Problemas serios que requieren atención inmediata

### Tipos de Fallas Comunes

#### 1. Fallas de Configuración
```python
AssertionError: Expected service to be registered
```
- **Causa**: Componentes no inicializados correctamente
- **Solución**: Verificar orden de inicialización

#### 2. Fallas de Timing
```python
AssertionError: Expected recovery within timeout
```
- **Causa**: Operaciones asíncronas no completadas
- **Solución**: Ajustar timeouts o usar polling

#### 3. Fallas de Estado
```python
AssertionError: Expected 2 healthy instances, got 3
```
- **Causa**: Estado no actualizado después de operación
- **Solución**: Verificar sincronización de estado

## Configuración para CI/CD

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python tests/run_tests.py
```

### Requisitos Mínimos
- Python 3.7+
- Todas las dependencias de `requirements.txt`
- Acceso a sistema de archivos (para reportes temporales)

## Debugging Tests

### Habilitar Logs Detallados
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Usar pdb para Debugging
```python
import pdb; pdb.set_trace()
```

### Tests con Datos Mock
```python
from unittest.mock import Mock, patch

# Mock de servicios externos
with patch('external_service.call') as mock_call:
    mock_call.return_value = {"status": "success"}
    # ... ejecutar test
```

## Mejores Prácticas

### 1. Aislamiento de Tests
- Cada test debe ser independiente
- Usar `setUp()` y `tearDown()` para estado limpio
- No depender del orden de ejecución

### 2. Datos de Test
- Usar datos determinísticos cuando sea posible
- Evitar dependencias externas
- Mockear servicios externos

### 3. Assertions Claras
```python
# ✅ Bueno
self.assertEqual(actual_count, expected_count, 
                f"Expected {expected_count} instances, got {actual_count}")

# ❌ Malo
self.assertTrue(actual_count == expected_count)
```

### 4. Performance
- Tests rápidos (< 1 segundo por test)
- Usar timeouts cortos para tests
- Mockear operaciones lentas

## Agregar Nuevos Tests

### 1. Crear nuevo archivo de test
```python
# tests/test_nuevo_modulo.py
import unittest
from nuevo_modulo import NuevaClase

class TestNuevaClase(unittest.TestCase):
    def setUp(self):
        self.instance = NuevaClase()
    
    def test_nueva_funcionalidad(self):
        result = self.instance.nueva_funcionalidad()
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
```

### 2. Actualizar run_tests.py si es necesario

### 3. Documentar el nuevo test en este README

## Troubleshooting

### Problemas Comunes

1. **ImportError**: Verificar que el path del proyecto esté configurado
2. **TimeoutError**: Ajustar timeouts en tests lentos  
3. **ResourceError**: Asegurar que recursos se liberen en tearDown()
4. **StateError**: Verificar que el estado se resetee entre tests

### Logs Útiles
```bash
# Ejecutar con logs detallados
python -m unittest tests.test_service -v --buffer

# Capturar output completo
python tests/run_tests.py > test_output.log 2>&1
```
