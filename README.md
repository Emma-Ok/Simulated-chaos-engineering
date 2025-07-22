# 🔥 Demo Interactivo de Chaos Engineering

**La forma más fácil y visual de aprender Chaos Engineering**

Un simulador completo e interactivo que te enseña los principios de Chaos Engineering a través de experimentos prácticos con arquitecturas distribuidas simuladas.

## 🚀 ¡Ejecutar es súper fácil!

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. ¡Ejecutar el demo!
python demo.py
```

**¡Eso es todo!** 🎉

### 🔧 **¿Problemas? Opciones alternativas:**
- **`python demo.py`** ← Versión súper estable (RECOMENDADA)
- **`python run_demo.py`** ← Versión interactiva completa

## ✨ ¿Qué verás?

### 🎯 Demo Rápida (5 minutos) - ¡RECOMENDADO!
- 🏗️ **Configuración automática** de arquitectura distribuida
- 🌐 **Tráfico simulado** con métricas en tiempo real  
- 💥 **Experimentos de caos** automáticos y visuales
- 📊 **Reportes HTML** interactivos con gráficos

### 🧪 Experimentos Interactivos
- **🐒 Chaos Monkey**: Termina instancias paso a paso
- **🌐 Network Latency**: Configura delays personalizados
- **💾 Resource Exhaustion**: Agota CPU/memoria selectivamente
- **🔥 Multiple Chaos**: Experimentos simultáneos

### 📊 Monitoreo Visual
- **Métricas en tiempo real** actualizadas cada 3 segundos
- **Estado de servicios** con indicadores visuales
- **Alertas automáticas** cuando algo va mal
- **Dashboards interactivos** con gráficos

### 💥 Escenarios Avanzados
- **🦍 Chaos Gorilla**: Falla de zona completa
- **🌊 Traffic Spike**: Picos masivos de tráfico  
- **🔌 Network Partition**: Partición de red
- **🧨 Database Chaos**: Fallas en base de datos

### 📚 Modo Educativo
- **Explicaciones interactivas** de cada concepto
- **Guías paso a paso** para entender experimentos
- **Mejores prácticas** de la industria
- **Patrones de resiliencia** explicados visualmente

## 🏗️ Arquitectura Simulada

```
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
```

## 🎮 Cómo Funciona

### 1. **Menú Principal Super Simple**
```
┌─────────────────── DEMO INTERACTIVO ───────────────────┐
│                                                        │
│  Estado: 🟢 ACTIVO    Servicios: 05                    │
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
```

### 2. **Experiencias Interactivas**

**🚀 Demo Rápida**: Todo automatizado, solo siéntate y disfruta
- ✅ Configuración automática
- ✅ Métricas en tiempo real
- ✅ Experimentos visuales
- ✅ Reportes automáticos

**🧪 Experimentos**: Tú controlas cada paso
- 🎯 Selecciona servicios objetivo
- ⚙️ Configura parámetros  
- 📊 Ve el impacto en tiempo real
- 📈 Analiza los resultados

**📊 Monitoreo**: Dashboard live actualizado cada 3 segundos
```
📊 MÉTRICAS DEL SISTEMA - TIEMPO REAL
==================================================
⏱️ Uptime: 245s | 🟢 Sistema: FUNCIONANDO

🟢 api-gateway      | 04/04 inst | 100.0% | 0067ms | 0.0% err
🟡 auth-service     | 02/03 inst |  66.7% | 0142ms | 2.1% err  
🟢 user-service     | 03/03 inst | 100.0% | 0089ms | 0.5% err
🟢 database         | 02/02 inst | 100.0% | 0234ms | 0.0% err
🟢 cache            | 03/03 inst | 100.0% | 0023ms | 0.1% err
```

### 3. **Reportes Automáticos**
- 📊 **Gráficos interactivos** con Plotly
- 📈 **Análisis de tendencias** durante experimentos
- 💡 **Recomendaciones** automáticas de mejora
- 📋 **Resumen ejecutivo** con métricas clave

## 🧪 Tipos de Experimentos

| Experimento | Descripción | Nivel | Duración |
|-------------|-------------|-------|----------|
| 🐒 **Chaos Monkey** | Termina instancias aleatoriamente | 🟢 Básico | 30s |
| 🌐 **Network Latency** | Introduce delays de red (100-2000ms) | 🟡 Medio | 60s |
| 💾 **Resource Exhaustion** | Agota CPU/memoria (configurable) | 🟡 Medio | 45s |
| 🦍 **Chaos Gorilla** | Falla de zona completa | 🔴 Alto | 120s |
| 🌊 **Traffic Spike** | Pico masivo de tráfico | 🟡 Medio | 60s |
| 🔌 **Network Partition** | Aislamiento de servicios | 🟡 Medio | 60s |
| 🧨 **Database Chaos** | Fallas en BD | 🔴 Alto | 90s |

## 📚 Modo Educativo

### Aprende Interactivamente:
- **❓ ¿Qué es Chaos Engineering?** - Historia y principios
- **🏗️ Arquitecturas Distribuidas** - Componentes y desafíos  
- **🧪 Tipos de Experimentos** - Desde básicos hasta destructivos
- **📊 Métricas y Monitoreo** - Golden signals y alertas
- **🔄 Patrones de Resiliencia** - Circuit breaker, bulkhead, retry
- **🎯 Mejores Prácticas** - Cómo implementar en la vida real

## 🎯 ¿Para Quién Es?

### 🎓 **Estudiantes**
- Aprende sistemas distribuidos de forma práctica
- Ve conceptos teóricos en acción
- Experimenta sin riesgos

### 🏢 **Equipos de Desarrollo**  
- Entiende el impacto de fallas
- Diseña sistemas más resilientes
- Practica incident response

### 🔧 **SREs e Ingenieros**
- Explora herramientas de chaos engineering
- Valida estrategias de resiliencia  
- Mejora observabilidad

### 👥 **Managers y Arquitectos**
- Visualiza riesgos del sistema
- Justifica inversión en resiliencia
- Entiende trade-offs técnicos

## 🔧 Estructura del Proyecto (Limpia y Organizada)

```
ChaosEngineering/
├── 🎮 demo.py                  # ← ¡PUNTO DE ENTRADA PRINCIPAL!
├── 🔥 run_demo.py              # Demo interactivo completo  
├── 🏗️ chaos_system.py          # Sistema principal
├── 📋 requirements.txt         # Dependencias
├── 📋 README.md                # Esta documentación
├── 🚫 .gitignore               # Archivos a ignorar
├── 
├── 📂 core/                    # Componentes fundamentales
│   ├── service.py              # Servicios distribuidos
│   ├── load_balancer.py        # Balanceador de carga
│   ├── monitoring.py           # Sistema de monitoreo
│   └── patterns.py             # Patrones de resiliencia
├── 
├── 📂 chaos/                   # Motor de experimentos
│   ├── chaos_monkey.py         # Chaos Monkey principal
│   ├── experiments.py          # Experimentos avanzados
│   └── runner.py               # Orquestador de experimentos
├── 
├── 📂 utils/                   # Utilidades
│   ├── helpers.py              # Funciones comunes
│   ├── reports.py              # Generador de reportes HTML
│   └── menu_interface.py       # Interfaces de usuario
├── 
├── 📂 config/                  # Configuración
│   └── chaos_config.yaml       # Configuración del sistema
├── 
├── 📂 examples/                # Ejemplos y tutoriales
│   ├── quick_start.py          # Ejemplo básico
│   ├── basic_simulation.py     # Simulación completa
│   └── advanced_experiments.py # Experimentos complejos
├── 
├── 📂 tests/                   # Tests automatizados
│   └── run_tests.py            # Ejecutor de tests
└── 
└── 📂 reports/                 # Reportes HTML generados
    └── *.html                  # Reportes con gráficos interactivos
```

## 🛠️ Instalación Detallada

### Requisitos:
- **Python 3.8+**
- **10 MB de espacio** 
- **Terminal/Command Prompt**

### Paso a Paso:

```bash
# 1. Clonar o descargar el proyecto
git clone <repository-url>
cd ChaosEngineering

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Verificar instalación (opcional)
python tests/run_tests.py

# 4. ¡Ejecutar el demo!
python run_demo.py
```

### ¿Problemas? 🔧

**❌ Error de dependencias:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**❌ Error de permisos:**
```bash
# Linux/Mac
chmod +x run_demo.py

# Windows
python run_demo.py
```

**❌ Python no encontrado:**
- Instala Python desde [python.org](https://python.org)
- Asegúrate que esté en el PATH

## 🎉 Empezar Ahora

### Opción 1: Demo Rápida (Recomendada)
```bash
python run_demo.py
# Selecciona "1" para demo de 5 minutos
```

### Opción 2: Exploración Libre
```bash
python run_demo.py  
# Explora el menú interactivo
```

### Opción 3: Ejemplos Específicos  
```bash
# Ejemplo básico
python examples/quick_start.py

# Simulación completa
python examples/basic_simulation.py
```

## 💡 Consejos Pro

### 🚀 **Para Principiantes**
1. Comienza con la **Demo Rápida** (opción 1)
2. Luego explora **Experimentos Interactivos** (opción 2) 
3. Usa el **Modo Educativo** (opción 6) para aprender conceptos
4. Experimenta con **Chaos Monkey** antes de experimentos avanzados

### 🧪 **Para Experimentadores**
1. Prueba **múltiples experimentos simultáneos**
2. Configura **parámetros personalizados** en experimentos
3. Observa el **monitoreo en tiempo real** durante experimentos
4. Revisa los **reportes HTML** generados automáticamente

### 📊 **Para Analistas**
1. Ejecuta experimentos durante **períodos extendidos**
2. Compara **métricas antes/después** de experimentos
3. Analiza **patrones de degradación** en los reportes
4. Documenta **hallazgos y recomendaciones**

## 🌟 ¿Qué Hace Especial Este Demo?

### ✅ **Súper Fácil de Usar**
- Un solo comando para ejecutar
- Interfaz visual e intuitiva
- Navegación con números simples
- Explicaciones paso a paso

### ✅ **Educativo y Práctico**  
- Conceptos explicados de forma simple
- Experimentos con resultados inmediatos
- Análisis automático de impacto
- Recomendaciones de mejora

### ✅ **Realista pero Seguro**
- Simula arquitecturas reales
- Experimentos basados en casos reales
- Métricas y alertas realistas
- Completamente seguro (solo simulación)

### ✅ **Visualmente Atractivo**
- Interfaz con emojis y colores
- Métricas actualizadas en tiempo real
- Reportes HTML con gráficos interactivos
- Diagramas de arquitectura ASCII

## 📞 Soporte

### 🐛 **¿Encontraste un bug?**
- Revisa la sección "¿Problemas? 🔧" arriba
- Ejecuta con `--log-level DEBUG` para más información
- Verifica que tengas Python 3.8+

### 💡 **¿Quieres más características?**
- Este es un proyecto educativo
- Para uso en producción, considera herramientas como:
  - **Chaos Monkey** (Netflix)
  - **Gremlin** (Plataforma comercial)
  - **Litmus** (Para Kubernetes)

### 🎓 **¿Quieres aprender más?**

**📚 Libros Recomendados:**
- "Chaos Engineering" por Casey Rosenthal
- "Building Microservices" por Sam Newman
- "Site Reliability Engineering" por Google

**🌐 Recursos Online:**
- [Principles of Chaos Engineering](https://principlesofchaos.org)
- [Netflix Tech Blog](https://netflixtechblog.com)
- [Chaos Engineering Community](https://www.chaoseng.io)

---

## 🎉 ¡Disfruta el Demo!

**🔥 Aprende Chaos Engineering de la forma más divertida e interactiva**

```bash
python run_demo.py
```

**¡Eso es todo lo que necesitas hacer!** 🚀

---

*Este es un proyecto educativo diseñado para enseñar conceptos de Chaos Engineering de forma segura y práctica. No usar en sistemas de producción.*
