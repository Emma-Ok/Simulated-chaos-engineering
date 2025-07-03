# Simulador de Chaos Engineering

Un simulador completo de Chaos Engineering en Python que demuestra los principios y prácticas de esta disciplina en sistemas distribuidos.

## Características

- ✅ Arquitectura distribuida simulada con múltiples servicios
- ✅ Balanceador de carga con distribución de tráfico
- ✅ Sistema de monitoreo en tiempo real
- ✅ Múltiples tipos de experimentos de chaos
- ✅ Circuit Breaker y Bulkhead patterns
- ✅ Visualización de métricas y reportes
- ✅ Configuración flexible via YAML/JSON

## Arquitectura del Sistema

```
API Gateway → Load Balancer → [Service A, Service B, Service C]
                          ↓
                      Database Cluster
                          ↓
                      Cache Layer
                          ↓
                      Monitoring System
```

## Instalación

1. Clona o descarga el proyecto
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso Rápido

### Inicio Rápido
```python
# Ejecutar ejemplo básico
python examples/quick_start.py

# Ejecutar simulación con configuración
python examples/basic_simulation.py

# Ejecutar experimentos avanzados
python examples/advanced_experiments.py
```

### Usando el CLI Principal
```python
# Ejecutar simulación interactiva
python main.py

# Ejecutar con configuración personalizada
python main.py --config config/chaos_config.yaml

# Ejecutar modo demo
python main.py --demo
```

### Ejemplos Disponibles

Consulta la carpeta `examples/` para ejemplos detallados:

- **`quick_start.py`**: Introducción básica al sistema
- **`basic_simulation.py`**: Simulación con fallas controladas  
- **`advanced_experiments.py`**: Experimentos complejos de chaos
- **`configuration_example.py`**: Configuración mediante YAML
- **`monitoring_dashboard.py`**: Monitoreo en tiempo real

```bash
# Ver todos los ejemplos
ls examples/
python examples/README.md  # Documentación detallada
```

## Tipos de Experimentos

### 1. Chaos Monkey
- Terminación aleatoria de instancias
- Respeta reglas de seguridad
- Configurable por horarios

### 2. Fallas de Red
- Latencia alta
- Pérdida de paquetes
- Desconexiones

### 3. Fallas de Recursos
- Alto consumo de CPU
- Agotamiento de memoria
- Saturación de disco

### 4. Experimentos Avanzados
- **Chaos Gorilla**: Falla de centro de datos completo
- **Chaos Kong**: Falla regional
- **Latency Monkey**: Latencia variable
- **Doctor Monkey**: Detección de instancias no saludables

## Configuración

Modifica `config/chaos_config.yaml` para personalizar:

```yaml
enabled: true
schedule:
  days: ["monday", "tuesday", "wednesday", "thursday", "friday"]
  hours:
    start: 9
    end: 17
targets:
  services: ["api-service", "auth-service", "db-service"]
  max_instances_to_kill: 1
  min_healthy_instances: 2
experiments:
  instance_termination:
    probability: 0.1
  network_latency:
    probability: 0.05
    delay_ms: 500
  resource_exhaustion:
    probability: 0.03
```

## Estructura del Proyecto

```
chaos_engineering/
├── core/                 # Componentes principales
│   ├── service.py       # Servicios y instancias
│   ├── load_balancer.py # Balanceador de carga
│   ├── monitoring.py    # Sistema de monitoreo
│   └── patterns.py      # Circuit Breaker, Bulkhead
├── chaos/               # Motores de chaos
│   ├── chaos_monkey.py  # Chaos Monkey
│   ├── experiments.py   # Tipos de experimentos
│   └── runner.py        # Ejecutor de experimentos
├── config/              # Configuraciones
├── utils/               # Utilidades
├── examples/            # Ejemplos de uso
└── reports/             # Reportes generados
```

## Métricas y Monitoreo

El sistema genera métricas en tiempo real:

- **Latencia**: Tiempo de respuesta promedio
- **Throughput**: Requests por segundo
- **Error Rate**: Porcentaje de errores
- **Disponibilidad**: Tiempo de actividad del servicio
- **Tiempo de Recuperación**: MTTR después de fallas

## Visualización

- Dashboards en tiempo real con Plotly
- Gráficos de métricas históricas
- Alertas automáticas
- Reportes detallados en HTML

## Patrones Implementados

### Circuit Breaker
```python
# Detecta fallas y previene cascadas
circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=30,
    expected_exception=ServiceException
)
```

### Bulkhead
```python
# Aislamiento de recursos
bulkhead = Bulkhead(
    name="database_pool",
    max_concurrent_calls=10
)
```

## Ejemplos de Resultados

### Antes del Chaos Engineering
- Tiempo de recuperación: 15 minutos
- Cascada de fallas: 3 servicios afectados
- Error rate durante falla: 100%

### Después de implementar mejoras
- Tiempo de recuperación: 2 minutos
- Servicios afectados: 1 (aislado)
- Error rate durante falla: 15%

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

MIT License - ver LICENSE para detalles

## Conceptos de Chaos Engineering

Este simulador implementa los principios fundamentales:

1. **Build a Hypothesis**: Define el estado estable del sistema
2. **Vary Real-world Events**: Simula fallas reales
3. **Run Experiments in Production**: Ejecuta en condiciones reales
4. **Automate Continuously**: Automatiza los experimentos
5. **Minimize Blast Radius**: Limita el impacto de las fallas

## Tests y Validación

### Ejecutar Tests
```bash
# Ejecutar todos los tests
python tests/run_tests.py

# Tests específicos
python tests/run_tests.py test_service
python tests/run_tests.py test_chaos_monkey
python tests/run_tests.py test_integration

# Listar tests disponibles
python tests/run_tests.py --list
```

### Cobertura de Tests

El sistema incluye tests comprehensivos:

- ✅ **Tests Unitarios**: Servicios, instancias, Chaos Monkey
- ✅ **Tests de Integración**: Sistema completo end-to-end
- ✅ **Tests de Resiliencia**: Múltiples fallas simultáneas
- ✅ **Tests de Configuración**: Carga desde archivos YAML

```bash
# Ejemplo de output de tests
======================================================================
📊 RESUMEN DE RESULTADOS
======================================================================
✅ Tests ejecutados: 45
🟢 Exitosos: 43
🔴 Fallidos: 2
⚠️  Errores: 0
📈 Tasa de éxito: 95.6%
🎉 ¡Excelente! Los tests están pasando correctamente.
```

Para más detalles, consulta `tests/README.md`.
