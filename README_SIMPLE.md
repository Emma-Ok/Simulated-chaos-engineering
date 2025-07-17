# 🔥 Simulador de Chaos Engineering - VERSIÓN SIMPLIFICADA

Sistema unificado y centralizado para demostraciones rápidas de Chaos Engineering.

## 🚀 Inicio Rápido

### Demostración Automática (Recomendado)
```bash
# Demo rápida de 3 minutos
python demo_chaos.py

# Demo personalizada
python demo_chaos.py --duration 2

# Con logs detallados
python demo_chaos.py --verbose
```

### Modo Interactivo
```bash
# Control manual de experimentos
python demo_chaos.py --interactive
```

## ✨ Características Principales

### 🎯 **Sistema Centralizado**
- **Una sola interfaz** para todos los experimentos
- **Configuración simplificada** sin archivos complejos
- **Gestión automática** de servicios y recursos

### 🧪 **Experimentos Unificados**
- **Latencia**: Simula delays de red en servicios
- **Terminación**: Mata instancias de forma controlada
- **Recursos**: Agota CPU/memoria temporalmente
- **Diagnóstico**: Evalúa la salud del sistema

### 📊 **Monitoreo Integrado**
- **Métricas en tiempo real** de todos los servicios
- **Alertas automáticas** cuando hay problemas
- **Reportes HTML** con gráficos y análisis

### ⚡ **Optimizado para Demos**
- **Tiempos cortos**: 1-4 minutos por demostración
- **Resultados visibles**: Cambios inmediatos observables
- **Seguridad integrada**: Protección contra fallas catastróficas

## 🎮 Uso del Sistema

### Demostración Automática

El sistema ejecuta automáticamente una secuencia de experimentos:

```bash
python demo_chaos.py --duration 3
```

**Secuencia típica (3 minutos):**
1. **Minuto 1**: Configuración y diagnóstico inicial
2. **Minuto 2**: Experimento de latencia en API
3. **Minuto 3**: Terminación de instancia + recuperación

### Modo Interactivo

Control manual completo del sistema:

```bash
python demo_chaos.py --interactive
```

**Comandos disponibles:**
- `1` - Ver estado del sistema
- `2` - Experimento de latencia
- `3` - Experimento de terminación  
- `4` - Experimento de recursos
- `5` - Diagnóstico del sistema
- `6` - Generar reporte
- `0` - Salir

## 🏗️ Arquitectura Simplificada

```
demo_chaos.py                 # → Interfaz principal
├── simple_chaos_system.py    # → Sistema principal
├── chaos_experiments_core.py # → Experimentos centralizados
├── core/                     # → Componentes base
│   ├── service.py           # → Servicios y instancias
│   ├── load_balancer.py     # → Distribución de tráfico
│   └── monitoring.py        # → Métricas y alertas
└── utils/                    # → Utilidades
    ├── helpers.py           # → Funciones comunes
    └── reports.py           # → Generación de reportes
```

## 🧪 Tipos de Experimentos

### 🌐 Latencia
Añade delays de red a servicios específicos:
```python
# En modo interactivo: opción 2
# Parámetros: servicio, latencia_ms, duración
```

### 💀 Terminación de Instancias
Mata instancias de forma controlada:
```python
# En modo interactivo: opción 3
# Respeta mínimos de instancias para evitar outages completos
```

### 💾 Agotamiento de Recursos
Simula alta utilización de CPU/memoria:
```python
# En modo interactivo: opción 4
# Parámetros: servicio, tipo_recurso, nivel_agotamiento
```

### 🩺 Diagnóstico del Sistema
Evalúa la salud general del sistema:
```python
# En modo interactivo: opción 5
# Analiza disponibilidad, latencia, recursos
```

## 📊 Métricas y Reportes

### Métricas en Tiempo Real
- **Disponibilidad** por servicio
- **Tiempo de respuesta** promedio
- **Utilización de recursos** (CPU/memoria)
- **Tasa de errores** por servicio

### Reportes Automáticos
- **HTML interactivo** con gráficos
- **Análisis de impacto** de experimentos
- **Recomendaciones** de mejora
- **Historial completo** de eventos

## ⚙️ Configuración

### Configuración por Defecto
El sistema viene preconfigurado con:
- **4 servicios**: API, Auth, Database, Cache
- **2-3 instancias** por servicio
- **Monitoreo cada 5 segundos**
- **Máximo 3 experimentos** concurrentes

### Personalización
```python
from simple_chaos_system import SimpleChaosSystem, SystemConfig

config = SystemConfig(
    services={
        "mi-api": {"type": "api-gateway", "instances": 5},
        "mi-db": {"type": "database", "instances": 3}
    },
    monitoring_interval_seconds=3,
    max_concurrent_experiments=2
)

system = SimpleChaosSystem(config)
```

## 🛡️ Seguridad

### Verificaciones Automáticas
- **Mínimo de instancias**: No permite terminaciones que causen outages
- **Límites de concurrencia**: Máximo 3 experimentos simultáneos
- **Validación de objetivos**: Verifica que los servicios existan
- **Timeouts automáticos**: Los experimentos se auto-detienen

### Modo Seguro
Por defecto, todas las verificaciones están habilitadas:
```python
system.experiment_manager.safety_checks_enabled = True
```

## 📁 Archivos Eliminados/Simplificados

### ❌ Archivos Eliminados
- `main.py` (reemplazado por `demo_chaos.py`)
- `chaos_system.py` (reemplazado por `simple_chaos_system.py`)
- `chaos/experiments.py` (reemplazado por `chaos_experiments_core.py`)
- `chaos/runner.py` (integrado en el core)
- `chaos/chaos_monkey.py` (simplificado en experimentos)
- `examples/` (funcionalidad integrada en demo)

### ♻️ Archivos Simplificados
- `utils/helpers.py` (reducido 70% eliminando funciones duplicadas)
- `README.md` (enfoque en uso práctico)

## 🎯 Beneficios de la Refactorización

### ✅ **Menos Complejidad**
- **70% menos código** manteniendo funcionalidad core
- **Una sola interfaz** vs múltiples archivos de ejemplo
- **Configuración unificada** vs dispersa en múltiples archivos

### ✅ **Mejor Estructura**
- **Separación clara** de responsabilidades
- **Experimentos centralizados** con interfaz común
- **Factory pattern** para creación de experimentos

### ✅ **Más Mantenible**
- **Menos duplicación** de código
- **Funciones enfocadas** en una sola responsabilidad
- **Testing más simple** con componentes aislados

### ✅ **Mejor UX**
- **Demos más rápidas** (1-4 minutos vs 30+ minutos)
- **Interfaz más clara** con opciones obvias
- **Resultados inmediatos** y visibles

## 🚀 Próximos Pasos

1. **Ejecuta la demo**: `python demo_chaos.py`
2. **Prueba modo interactivo**: `python demo_chaos.py --interactive`
3. **Revisa reportes**: Abre `./reports/chaos_report_*.html`
4. **Personaliza**: Modifica `SystemConfig` según tus necesidades

---

**¡Disfruta experimentando con Chaos Engineering! 🔥**
