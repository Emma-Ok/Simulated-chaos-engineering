# 🔥 Simulador de Chaos Engineering

Un simulador completo de Chaos Engineering en Python que demuestra los principios y prácticas de esta disciplina en sistemas distribuidos. Este proyecto educativo implementa arquitecturas distribuidas realistas y experimentos de falla controlados.

## ✨ Características Principales

- 🏗️ **Arquitectura Distribuida**: Simulación de múltiples servicios (API Gateway, Auth, Database, Cache)
- ⚖️ **Balanceador de Carga**: Distribución inteligente de tráfico con múltiples estrategias
- 📊 **Monitoreo en Tiempo Real**: Métricas, alertas y dashboards visuales
- 🐒 **Chaos Monkey**: Terminación controlada de instancias
- 🧪 **Experimentos Avanzados**: Latencia, agotamiento de recursos, particiones de red
- 🔄 **Patrones de Resiliencia**: Circuit Breaker, Bulkhead, Retry, Timeout
- 📈 **Reportes Detallados**: Análisis de impacto y recomendaciones de mejora
- ⚙️ **Configuración YAML**: Configuración externa flexible

## 🚀 Inicio Rápido

### Instalación

1. **Clona o descarga el proyecto**
2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Verifica la instalación:**
   ```bash
   python setup.py
   ```

### Ejecución

**🎮 Interfaz de Menús (RECOMENDADO)**
```bash
python main.py
```

**⚡ Demo Rápida (4 minutos)**
```bash
python main.py --demo
```

**🚀 Ejemplos de Uso**
```bash
# Inicio básico
python examples/quick_start.py

# Simulación completa
python examples/basic_simulation.py

# Experimentos avanzados
python examples/advanced_experiments.py
```

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │    │   Auth Service  │    │  User Service   │
│   (3 instancias)│    │   (2 instancias)│    │   (2 instancias)│
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴─────────────┐
                    │     Load Balancer         │
                    │   (Health-based routing)  │
                    └─────────────┬─────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
    ┌─────────┴───────┐ ┌─────────┴───────┐ ┌─────────┴───────┐
    │  Database       │ │   Cache Layer   │ │   Monitoring    │
    │  (2 instancias) │ │  (2 instancias) │ │     System      │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
```

## 🧪 Tipos de Experimentos

### 🐒 Chaos Monkey (Básico)
- Terminación aleatoria de instancias
- Configuración de horarios y probabilidades
- Reglas de seguridad (mínimo de instancias saludables)

### 🌐 Experimentos de Red
- **Latency Monkey**: Introducir delays de red (100-2000ms)
- **Network Partition**: Aislamiento temporal de servicios
- **Packet Loss**: Simulación de pérdida de paquetes

### 💾 Agotamiento de Recursos
- **CPU Exhaustion**: Consumo intensivo de CPU (hasta 90%)
- **Memory Exhaustion**: Agotamiento de memoria disponible
- **Disk I/O**: Saturación de operaciones de disco

### 🦍 Experimentos Destructivos
- **Chaos Gorilla**: Falla de zona completa (múltiples servicios)
- **Chaos Kong**: Falla regional (toda una región)
- **Database Failure**: Simulación de caída de base de datos

### 🩺 Experimentos de Diagnóstico
- **Doctor Monkey**: Detección de instancias no saludables
- **Health Checker**: Verificación continua de estado
- **Performance Monitor**: Análisis de degradación

## 📊 Métricas y Monitoreo

### Métricas Clave
- **Latencia**: Tiempo de respuesta promedio (ms)
- **Throughput**: Requests por segundo (RPS)
- **Error Rate**: Porcentaje de errores (%)
- **Disponibilidad**: Tiempo de actividad (uptime)
- **MTTR**: Mean Time To Recovery (tiempo de recuperación)
- **MTBF**: Mean Time Between Failures

### Dashboards
- 📈 **Gráficos en Tiempo Real**: Métricas live con Plotly
- 🎯 **Alertas Automáticas**: Detección de umbrales críticos
- 📋 **Reportes HTML**: Análisis completo con recomendaciones
- 📊 **Exportación de Datos**: JSON, CSV para análisis externo

## ⚙️ Configuración

### Configuración Básica (YAML)
```yaml
# config/chaos_config.yaml
enabled: true

schedule:
  days: ["monday", "tuesday", "wednesday", "thursday", "friday"]
  hours:
    start: 9
    end: 17

targets:
  services: ["api-service", "auth-service", "db-service"]
  min_healthy_instances: 1
  max_instances_to_kill: 1

experiments:
  instance_termination:
    probability: 0.1
  network_latency:
    probability: 0.05
    delay_ms: 500
```

### Configuración Programática
```python
from chaos_system import ChaosEngineeringSystem

# Crear sistema
system = ChaosEngineeringSystem()

# Agregar servicios
system.add_service("api-gateway", "api-gateway", instances=3)
system.add_service("database", "database", instances=2)

# Configurar experimentos
system.run_chaos_experiment("latency", 
                           target_service="api-gateway",
                           latency_ms=500,
                           duration_seconds=300)
```

## 🔧 Patrones de Resiliencia

### Circuit Breaker
```python
# Prevención de cascadas de fallas
circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=30,
    expected_exception=ServiceException
)
```

### Bulkhead Pattern
```python
# Aislamiento de recursos
bulkhead = BulkheadPattern("api-bulkhead", max_concurrent=20)
```

### Retry con Backoff Exponencial
```python
# Reintentos inteligentes
retry = RetryPattern("db-retry", max_attempts=3, base_delay=1.0)
```

## 📁 Estructura del Proyecto

```
ChaosEngineering/
├── 🔥 chaos_system.py          # Sistema principal integrado
├── 🖥️ main.py                  # CLI y puntos de entrada
├── ⚙️ setup.py                 # Script de instalación y verificación
├── 📋 requirements.txt         # Dependencias del proyecto
├── 
├── 📂 core/                    # Componentes principales
│   ├── service.py              # Servicios e instancias distribuidas
│   ├── load_balancer.py        # Balanceador de carga inteligente
│   ├── monitoring.py           # Sistema de monitoreo y métricas
│   └── patterns.py             # Patrones de resiliencia
├── 
├── 📂 chaos/                   # Motor de Chaos Engineering
│   ├── chaos_monkey.py         # Chaos Monkey principal
│   ├── experiments.py          # Experimentos avanzados
│   └── runner.py               # Orquestador de experimentos
├── 
├── 📂 config/                  # Configuración
│   └── chaos_config.yaml       # Configuración completa del sistema
├── 
├── 📂 utils/                   # Utilidades del sistema
│   ├── helpers.py              # Helpers comunes y logging
│   ├── reports.py              # Generador de reportes HTML/JSON
│   └── menu_interface.py       # Interfaz de menús navegable
├── 
├── 📂 examples/                # Ejemplos de uso
│   ├── quick_start.py          # Inicio rápido básico
│   ├── basic_simulation.py     # Simulación con fallas controladas
│   ├── advanced_experiments.py # Experimentos complejos
│   ├── configuration_example.py# Uso de configuración YAML
│   └── monitoring_dashboard.py # Dashboard de monitoreo
├── 
├── 📂 tests/                   # Tests unitarios e integración
│   ├── test_service.py         # Tests de servicios
│   ├── test_chaos_monkey.py    # Tests de Chaos Monkey
│   ├── test_integration.py     # Tests del sistema completo
│   └── run_tests.py            # Ejecutor de tests
└── 
└── 📂 reports/                 # Reportes generados automáticamente
```

## 🎮 Guía de la Interfaz de Menús

### Navegación Básica
- **Números (1-9)**: Seleccionar opciones
- **0**: Volver al menú anterior o salir
- **Enter**: Confirmar selección
- **Ctrl+C**: Interrupción segura

### Menús Principales

#### 🚀 1. Inicio Rápido
- **Demo de 5 minutos**: Demostración automática completa
- **Simulación interactiva**: Proceso guiado paso a paso
- **Experimento básico**: Chaos Monkey simple

#### 🔧 2. Gestión del Sistema
- **Iniciar/Reiniciar Sistema**: Control del sistema distribuido
- **Agregar/Remover Servicios**: Gestión de arquitectura
- **Ver Estado**: Dashboard del sistema
- **Métricas en Tiempo Real**: Monitor actualizable

#### 🧪 3. Experimentos de Chaos
- **🐒 Chaos Monkey**: Terminación aleatoria de instancias
- **🌐 Experimento de Latencia**: Delays de red
- **💾 Agotamiento de Recursos**: CPU/memoria alta
- **🦍 Chaos Gorilla**: Falla de zona (DESTRUCTIVO)

#### 📊 4. Monitoreo y Métricas
- **Dashboard en Tiempo Real**: Métricas live
- **Generar Reporte HTML**: Reporte completo
- **Exportar Métricas**: Datos en JSON
- **Historial de Métricas**: Análisis temporal

## 🧪 Ejemplos de Uso

### Ejemplo 1: Inicio Básico
```python
# examples/quick_start.py
from chaos_system import ChaosEngineeringSystem

system = ChaosEngineeringSystem()
system.add_service("api-gateway", "api-gateway", instances=3)
system.add_service("database", "database", instances=2)

system.initialize()
system.start()

# Ejecutar experimento
result = system.force_chaos_monkey()
print(f"Resultado: {result}")

# Generar reporte
reports = system.generate_report()
system.stop()
```

### Ejemplo 2: Configuración YAML
```python
# examples/configuration_example.py
system = ChaosEngineeringSystem("config/chaos_config.yaml")
system.run_simulation(duration_minutes=4)
```

### Ejemplo 3: Experimentos Avanzados
```python
# examples/advanced_experiments.py
system = ChaosEngineeringSystem()

# Experimento de latencia
exp_id = system.run_chaos_experiment(
    "latency",
    target_service="api-service",
    latency_ms=500,
    duration_seconds=300
)

# Agotamiento de recursos  
exp_id = system.run_chaos_experiment(
    "resource_exhaustion",
    target_service="database",
    resource_type="cpu",
    exhaustion_level=0.9
)
```

## 🧪 Tests y Validación

```bash
# Ejecutar todos los tests
python tests/run_tests.py

# Tests específicos
python tests/run_tests.py test_service
python tests/run_tests.py test_chaos_monkey
python tests/run_tests.py test_integration

# Verificar instalación
python setup.py
```

### Cobertura de Tests
- ✅ **Tests Unitarios**: Servicios, instancias, Chaos Monkey
- ✅ **Tests de Integración**: Sistema completo end-to-end
- ✅ **Tests de Configuración**: Carga y validación de YAML
- ✅ **Tests de Resiliencia**: Patrones y recuperación

## 📊 Conceptos de Chaos Engineering

### Principios Fundamentales
1. **Construir hipótesis** sobre el comportamiento del sistema
2. **Variar eventos del mundo real** de forma controlada
3. **Ejecutar experimentos** en un entorno seguro
4. **Automatizar** la ejecución continua
5. **Minimizar el radio de explosión** de las fallas

### Métricas Clave de Resiliencia
- **MTTR**: Mean Time To Recovery (tiempo de recuperación)
- **MTBF**: Mean Time Between Failures (tiempo entre fallas)
- **SLA**: Service Level Agreement compliance
- **Error Budget**: Margen de error permitido

### Patrones de Diseño Implementados
- **Circuit Breaker**: Prevenir cascadas de fallas
- **Bulkhead**: Aislar recursos y fallas
- **Retry**: Reintentos con backoff exponencial
- **Timeout**: Evitar esperas indefinidas
- **Fallback**: Respuestas de emergencia

## 🛠️ Solución de Problemas

### Problemas Comunes

**❌ Sistema no inicia:**
- Verifica dependencias: `pip install -r requirements.txt`
- Ejecuta: `python setup.py`
- Revisa permisos de archivos

**❌ Experimentos fallan:**
- Asegúrate que el sistema esté iniciado
- Verifica que haya servicios configurados
- Revisa logs en modo DEBUG: `python main.py --log-level DEBUG`

**❌ Reportes no se generan:**
- Verifica permisos de escritura en `./reports/`
- Asegúrate que el sistema tenga datos de métricas

**❌ Performance lenta:**
- Reduce número de instancias
- Ajusta intervalos de monitoreo
- Usa duración de simulación más corta

### Debug y Logs
```bash
# Logs detallados
python main.py --log-level DEBUG

# Modo dry-run (solo simulación)
python main.py --config config/chaos_config.yaml --dry-run

# Verificación de sistema
python setup.py
```

## 📚 Recursos de Aprendizaje

### Libros Recomendados
- **"Chaos Engineering"** por Casey Rosenthal y Nora Jones
- **"Building Microservices"** por Sam Newman  
- **"Site Reliability Engineering"** por Google SRE Team

### Herramientas Reales
- **Chaos Monkey** (Netflix) - Inspiración para este proyecto
- **Gremlin** - Plataforma comercial de Chaos Engineering
- **Litmus** - Chaos Engineering para Kubernetes

### Conceptos Relacionados
- **Site Reliability Engineering (SRE)**
- **Observability** y **Monitoring**
- **Distributed Systems** y **Microservices**
- **Fault Tolerance** y **Resilience Patterns**

---

## 🎉 Proyecto Educativo

Este simulador es un proyecto educativo que demuestra los principios fundamentales de Chaos Engineering de manera práctica y segura. Perfecto para:

- 🎓 **Estudiantes** aprendiendo sobre sistemas distribuidos
- 🏢 **Equipos** explorando conceptos de resiliencia
- 🔧 **Ingenieros** practicando experimentos de falla
- 📊 **Analistas** entendiendo métricas de sistema

**⚠️ Nota**: Este es un simulador educativo. Para entornos de producción, utiliza herramientas especializadas como Chaos Monkey de Netflix o Gremlin.

---

**¡Gracias por usar el Simulador de Chaos Engineering! 🔥**

*Aprende, experimenta y construye sistemas más resilientes.*
