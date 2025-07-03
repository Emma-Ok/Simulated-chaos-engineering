# Ejemplos de Uso - Simulador de Chaos Engineering

Esta carpeta contiene ejemplos prácticos para demostrar diferentes aspectos del simulador de Chaos Engineering.

## Ejemplos Disponibles

### 1. `quick_start.py`
**Ejemplo básico de inicio rápido**
- Configuración simple de servicios
- Ejecución básica de experimentos de chaos
- Generación de reportes

```bash
python examples/quick_start.py
```

### 2. `basic_simulation.py`
**Simulación básica con fallas controladas**
- Configuración de múltiples servicios
- Introducción de diferentes tipos de fallas
- Monitoreo del impacto y recuperación

```bash
python examples/basic_simulation.py
```

### 3. `advanced_experiments.py`
**Experimentos avanzados de Chaos Engineering**
- Latency Monkey - Introducción de latencia de red
- Resource Exhaustion Monkey - Agotamiento de recursos
- Chaos Gorilla - Falla de zona completa
- Monitoreo detallado del impacto

```bash
python examples/advanced_experiments.py
```

### 4. `configuration_example.py`
**Configuración mediante archivos YAML**
- Uso de configuración externa
- Personalización de comportamientos
- Configuración de patrones de resiliencia
- Configuración de horarios y probabilidades

```bash
python examples/configuration_example.py
```

### 5. `monitoring_dashboard.py`
**Monitoreo y dashboards en tiempo real**
- Dashboard de consola en tiempo real
- Configuración de alertas personalizadas
- Análisis de tendencias
- Recomendaciones automáticas

```bash
python examples/monitoring_dashboard.py
```

## Conceptos Demostrados

### Principios de Chaos Engineering
- **Hipótesis**: Definir el estado estable del sistema
- **Variaciones**: Introducir variables que reflejen eventos del mundo real
- **Impacto**: Medir el impacto en el estado estable
- **Automatización**: Automatizar experimentos para ejecutar continuamente

### Tipos de Experimentos
- **Instance Termination**: Terminación de instancias de servicios
- **Network Latency**: Introducción de latencia de red
- **Resource Exhaustion**: Agotamiento de CPU/memoria
- **Zone Failures**: Falla de zonas de disponibilidad completas
- **Dependency Failures**: Falla de servicios dependientes

### Patrones de Resiliencia
- **Circuit Breaker**: Prevención de cascadas de fallas
- **Bulkhead**: Aislamiento de recursos
- **Retry**: Reintentos con backoff exponencial
- **Rate Limiting**: Limitación de velocidad de requests
- **Timeout**: Timeouts configurables
- **Fallback**: Mecanismos de respaldo

### Métricas y Observabilidad
- **Latencia**: Tiempo de respuesta de servicios
- **Throughput**: Requests por segundo
- **Disponibilidad**: Porcentaje de uptime
- **Error Rate**: Tasa de errores
- **Resource Usage**: Uso de CPU y memoria

## Ejecutar Todos los Ejemplos

Para ejecutar todos los ejemplos en secuencia:

```bash
# Ejemplo básico (recomendado para empezar)
python examples/quick_start.py

# Simulación con más fallas
python examples/basic_simulation.py

# Experimentos avanzados
python examples/advanced_experiments.py

# Configuración personalizada
python examples/configuration_example.py

# Monitoreo en tiempo real
python examples/monitoring_dashboard.py
```

## Notas de Uso

1. **Prerequisitos**: Asegúrate de tener todas las dependencias instaladas (`pip install -r requirements.txt`)

2. **Duración**: Los ejemplos tienen diferentes duraciones:
   - Quick Start: ~1 minuto
   - Basic Simulation: ~2-3 minutos  
   - Advanced Experiments: ~5-7 minutos
   - Configuration Example: ~3-4 minutos
   - Monitoring Dashboard: ~8-10 minutos

3. **Reportes**: Todos los ejemplos generan reportes en la carpeta `reports/`

4. **Logs**: Los logs detallados se muestran en consola y se pueden redirigir a archivos

5. **Personalización**: Modifica los parámetros en cada ejemplo para experimentar con diferentes configuraciones

## Interpretación de Resultados

### Métricas Clave a Observar
- **Tiempo de Recuperación**: Qué tan rápido el sistema se recupera después de una falla
- **Degradación Gradual**: Si el sistema falla de manera gradual o abrupta
- **Efectividad de Patrones**: Si circuit breakers, retries, etc. funcionan correctamente
- **Impacto en Cascada**: Si las fallas se propagan a otros servicios

### Indicadores de Resiliencia
✅ **Buena Resiliencia**:
- Recuperación automática rápida (< 30 segundos)
- Degradación gradual sin colapso total
- Circuit breakers funcionando correctamente
- Métricas estables después de la recuperación

❌ **Problemas de Resiliencia**:
- Fallas en cascada
- Tiempos de recuperación largos (> 2 minutos)
- Colapso total del sistema
- Métricas inestables después de fallas

## Siguiente Paso

Después de ejecutar los ejemplos, revisa el archivo principal `main.py` para experimentos interactivos y el `README.md` del proyecto para documentación completa.
