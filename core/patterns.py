"""
Patrones de resiliencia para el simulador de Chaos Engineering.
Implementa Circuit Breaker, Bulkhead, Retry y otros patrones.
"""

import time
import threading
import random
from typing import Dict, Optional, Callable, Any
from enum import Enum
from dataclasses import dataclass
import logging
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class CircuitBreakerState(Enum):
    """Estados del Circuit Breaker"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Blocking requests  
    HALF_OPEN = "half_open"  # Testing recovery

@dataclass
class CircuitBreakerConfig:
    """Configuración del Circuit Breaker"""
    failure_threshold: int = 5          # Número de fallas para abrir
    success_threshold: int = 3          # Éxitos consecutivos para cerrar
    timeout_seconds: int = 60           # Tiempo antes de pasar a half-open
    expected_exception: type = Exception # Tipo de excepción a considerar

class CircuitBreaker:
    """
    Implementación del patrón Circuit Breaker.
    Previene cascadas de fallas cortando automáticamente servicios defectuosos.
    """
    
    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state_change_time = time.time()
        
        # Métricas
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.blocked_requests = 0
        
        # Threading
        self.lock = threading.RLock()
        
        logger.info(f"Circuit Breaker '{name}' inicializado en estado CLOSED")
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Ejecuta una función protegida por el circuit breaker.
        """
        with self.lock:
            self.total_requests += 1
            
            # Verificar si debemos cambiar de estado
            self._check_state_transition()
            
            if self.state == CircuitBreakerState.OPEN:
                self.blocked_requests += 1
                raise CircuitBreakerOpenException(
                    f"Circuit breaker '{self.name}' está ABIERTO"
                )
            
            try:
                # Ejecutar la función
                result = func(*args, **kwargs)
                self._record_success()
                return result
                
            except self.config.expected_exception:
                self._record_failure()
                raise
    
    def _record_success(self):
        """Registra una ejecución exitosa"""
        self.successful_requests += 1
        self.failure_count = 0
        
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self._transition_to_closed()
    
    def _record_failure(self):
        """Registra una falla"""
        self.failed_requests += 1
        self.failure_count += 1
        self.success_count = 0
        self.last_failure_time = time.time()
        
        if (
            (self.state == CircuitBreakerState.CLOSED and self.failure_count >= self.config.failure_threshold)
            or self.state == CircuitBreakerState.HALF_OPEN
        ):
            self._transition_to_open()
    
    def _check_state_transition(self):
        """Verifica si es necesario cambiar de estado"""
        if self.state == CircuitBreakerState.OPEN:
            if (self.last_failure_time and 
                time.time() - self.last_failure_time >= self.config.timeout_seconds):
                self._transition_to_half_open()
    
    def _transition_to_open(self):
        """Transición a estado OPEN"""
        self.state = CircuitBreakerState.OPEN
        self.state_change_time = time.time()
        logger.warning(f"🔴 Circuit Breaker '{self.name}' ABIERTO - bloqueando requests")
    
    def _transition_to_half_open(self):
        """Transición a estado HALF_OPEN"""
        self.state = CircuitBreakerState.HALF_OPEN
        self.state_change_time = time.time()
        self.success_count = 0
        logger.info(f"🟡 Circuit Breaker '{self.name}' SEMI-ABIERTO - probando recuperación")
    
    def _transition_to_closed(self):
        """Transición a estado CLOSED"""
        self.state = CircuitBreakerState.CLOSED
        self.state_change_time = time.time()
        self.failure_count = 0
        self.success_count = 0
        logger.info(f"🟢 Circuit Breaker '{self.name}' CERRADO - operación normal")
    
    def get_metrics(self) -> Dict:
        """Retorna métricas del circuit breaker"""
        with self.lock:
            uptime = time.time() - self.state_change_time
            success_rate = (self.successful_requests / max(1, self.total_requests)) * 100
            
            return {
                "name": self.name,
                "state": self.state.value,
                "uptime_seconds": uptime,
                "total_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "blocked_requests": self.blocked_requests,
                "success_rate": success_rate,
                "failure_count": self.failure_count,
                "last_failure_time": self.last_failure_time
            }
    
    def reset(self):
        """Resetea el circuit breaker al estado inicial"""
        with self.lock:
            self.state = CircuitBreakerState.CLOSED
            self.failure_count = 0
            self.success_count = 0
            self.last_failure_time = None
            self.state_change_time = time.time()
            logger.info(f"Circuit Breaker '{self.name}' reseteado")

class Bulkhead:
    """
    Implementación del patrón Bulkhead.
    Aísla recursos para prevenir que las fallas se propaguen.
    """
    
    def __init__(self, name: str, max_concurrent_calls: int = 10):
        self.name = name
        self.max_concurrent_calls = max_concurrent_calls
        self.current_calls = 0
        self.total_calls = 0
        self.rejected_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        
        # Threading
        self.semaphore = threading.Semaphore(max_concurrent_calls)
        self.lock = threading.RLock()
        
        logger.info(f"Bulkhead '{name}' inicializado con límite de {max_concurrent_calls} llamadas")
    
    def execute(self, func: Callable, timeout: float = None, *args, **kwargs) -> Any:
        """
        Ejecuta una función con aislamiento de recursos.
        """
        with self.lock:
            self.total_calls += 1
        
        # Intentar adquirir el semáforo
        acquired = self.semaphore.acquire(blocking=False)
        
        if not acquired:
            with self.lock:
                self.rejected_calls += 1
            raise BulkheadFullException(
                f"Bulkhead '{self.name}' está saturado ({self.max_concurrent_calls} llamadas)"
            )
        
        try:
            with self.lock:
                self.current_calls += 1
            
            start_time = time.time()
            
            # Ejecutar la función con timeout opcional
            if timeout:
                result = self._execute_with_timeout(func, timeout, *args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            execution_time = time.time() - start_time
            
            with self.lock:
                self.successful_calls += 1
                
            logger.debug(f"Bulkhead '{self.name}': ejecución exitosa en {execution_time:.2f}s")
            return result
            
        except Exception as e:
            with self.lock:
                self.failed_calls += 1
            logger.error(f"Bulkhead '{self.name}': ejecución falló - {e}")
            raise
            
        finally:
            with self.lock:
                self.current_calls -= 1
            self.semaphore.release()
    
    def _execute_with_timeout(self, func: Callable, timeout: float, *args, **kwargs):
        """Ejecuta una función con timeout"""
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                raise BulkheadTimeoutException(
                    f"Función excedió timeout de {timeout}s en bulkhead '{self.name}'"
                )
    
    def get_metrics(self) -> Dict:
        """Retorna métricas del bulkhead"""
        with self.lock:
            utilization = (self.current_calls / self.max_concurrent_calls) * 100
            success_rate = (self.successful_calls / max(1, self.total_calls)) * 100
            rejection_rate = (self.rejected_calls / max(1, self.total_calls)) * 100
            
            return {
                "name": self.name,
                "max_concurrent_calls": self.max_concurrent_calls,
                "current_calls": self.current_calls,
                "utilization": utilization,
                "total_calls": self.total_calls,
                "successful_calls": self.successful_calls,
                "failed_calls": self.failed_calls,
                "rejected_calls": self.rejected_calls,
                "success_rate": success_rate,
                "rejection_rate": rejection_rate
            }

class RetryPolicy:
    """
    Implementación de políticas de retry con backoff exponencial.
    """
    
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0, 
                 max_delay: float = 60.0, backoff_factor: float = 2.0,
                 jitter: bool = True):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter
        
        # Métricas
        self.total_attempts = 0
        self.successful_retries = 0
        self.failed_retries = 0
        
        logger.info(f"RetryPolicy inicializada: {max_attempts} intentos, delay base {base_delay}s")
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Ejecuta una función con política de retry.
        """
        last_exception = None
        
        for attempt in range(self.max_attempts):
            self.total_attempts += 1
            
            try:
                result = func(*args, **kwargs)
                
                if attempt > 0:
                    self.successful_retries += 1
                    logger.info(f"Retry exitoso en intento {attempt + 1}")
                
                return result
                
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_attempts - 1:
                    delay = self._calculate_delay(attempt)
                    logger.warning(f"Intento {attempt + 1} falló: {e}. Reintentando en {delay:.2f}s")
                    time.sleep(delay)
                else:
                    self.failed_retries += 1
                    logger.error(f"Todos los intentos fallaron. Último error: {e}")
        
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calcula el delay para el siguiente intento"""
        delay = self.base_delay * (self.backoff_factor ** attempt)
        delay = min(delay, self.max_delay)
        
        if self.jitter:
            # Añadir jitter para evitar thundering herd
            jitter_range = delay * 0.1
            delay += random.uniform(-jitter_range, jitter_range)
        
        return max(0, delay)
    
    def get_metrics(self) -> Dict:
        """Retorna métricas de retry"""
        return {
            "max_attempts": self.max_attempts,
            "total_attempts": self.total_attempts,
            "successful_retries": self.successful_retries,
            "failed_retries": self.failed_retries,
            "retry_success_rate": (self.successful_retries / max(1, self.total_attempts)) * 100
        }

class RateLimiter:
    """
    Implementación de rate limiting con token bucket.
    """
    
    def __init__(self, name: str, rate: float, burst_size: int = None):
        self.name = name
        self.rate = rate  # tokens per second
        self.burst_size = burst_size or int(rate * 2)  # bucket size
        self.tokens = self.burst_size
        self.last_refill = time.time()
        
        # Métricas
        self.total_requests = 0
        self.allowed_requests = 0
        self.denied_requests = 0
        
        # Threading
        self.lock = threading.RLock()
        
        logger.info(f"RateLimiter '{name}' inicializado: {rate} RPS, burst {self.burst_size}")
    
    def acquire(self, tokens_needed: int = 1) -> bool:
        """
        Intenta adquirir tokens del bucket.
        Retorna True si se pueden adquirir, False si no.
        """
        with self.lock:
            self.total_requests += 1
            self._refill_tokens()
            
            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                self.allowed_requests += 1
                return True
            else:
                self.denied_requests += 1
                return False
    
    def _refill_tokens(self):
        """Rellena el bucket con tokens basándose en el tiempo transcurrido"""
        now = time.time()
        time_passed = now - self.last_refill
        tokens_to_add = time_passed * self.rate
        
        self.tokens = min(self.burst_size, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def get_metrics(self) -> Dict:
        """Retorna métricas del rate limiter"""
        with self.lock:
            denial_rate = (self.denied_requests / max(1, self.total_requests)) * 100
            
            return {
                "name": self.name,
                "rate": self.rate,
                "burst_size": self.burst_size,
                "current_tokens": self.tokens,
                "total_requests": self.total_requests,
                "allowed_requests": self.allowed_requests,
                "denied_requests": self.denied_requests,
                "denial_rate": denial_rate
            }

class TimeoutPattern:
    """
    Implementación del patrón Timeout.
    """
    
    def __init__(self, name: str, default_timeout: float = 30.0):
        self.name = name
        self.default_timeout = default_timeout
        
        # Métricas
        self.total_calls = 0
        self.successful_calls = 0
        self.timeout_calls = 0
        self.failed_calls = 0
        
        logger.info(f"TimeoutPattern '{name}' inicializado con timeout por defecto {default_timeout}s")
    
    def execute(self, func: Callable, timeout: float = None, *args, **kwargs) -> Any:
        """
        Ejecuta una función con timeout.
        """
        import concurrent.futures
        
        timeout = timeout or self.default_timeout
        self.total_calls += 1
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            
            try:
                result = future.result(timeout=timeout)
                self.successful_calls += 1
                return result
                
            except concurrent.futures.TimeoutError:
                self.timeout_calls += 1
                raise TimeoutException(f"Función excedió timeout de {timeout}s")
                
            except Exception:
                self.failed_calls += 1
                raise
    
    def get_metrics(self) -> Dict:
        """Retorna métricas del timeout pattern"""
        success_rate = (self.successful_calls / max(1, self.total_calls)) * 100
        timeout_rate = (self.timeout_calls / max(1, self.total_calls)) * 100
        
        return {
            "name": self.name,
            "default_timeout": self.default_timeout,
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "timeout_calls": self.timeout_calls,
            "failed_calls": self.failed_calls,
            "success_rate": success_rate,
            "timeout_rate": timeout_rate
        }

class FallbackPattern:
    """
    Implementación del patrón Fallback.
    Proporciona respuestas alternativas cuando el servicio principal falla.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.fallback_strategies = []
        
        # Métricas
        self.primary_calls = 0
        self.primary_successes = 0
        self.fallback_calls = 0
        self.fallback_successes = 0
        
        logger.info(f"FallbackPattern '{name}' inicializado")
    
    def add_fallback(self, fallback_func: Callable, condition: Callable = None):
        """
        Añade una estrategia de fallback.
        condition: función que determina si usar este fallback
        """
        self.fallback_strategies.append({
            "function": fallback_func,
            "condition": condition or (lambda e: True)  # Usar por defecto si no hay condición
        })
    
    def execute(self, primary_func: Callable, *args, **kwargs) -> Any:
        """
        Ejecuta la función principal, y en caso de falla, intenta fallbacks.
        """
        self.primary_calls += 1
        
        try:
            result = primary_func(*args, **kwargs)
            self.primary_successes += 1
            return result
            
        except Exception as e:
            logger.warning(f"Función principal falló en '{self.name}': {e}")
            
            # Intentar fallbacks
            for i, strategy in enumerate(self.fallback_strategies):
                if strategy["condition"](e):
                    try:
                        self.fallback_calls += 1
                        logger.info(f"Ejecutando fallback {i+1} en '{self.name}'")
                        
                        result = strategy["function"](*args, **kwargs)
                        self.fallback_successes += 1
                        return result
                        
                    except Exception as fallback_error:
                        logger.error(f"Fallback {i+1} falló en '{self.name}': {fallback_error}")
                        continue
            
            # Si todos los fallbacks fallan, lanzar la excepción original
            raise e
    
    def get_metrics(self) -> Dict:
        """Retorna métricas del fallback pattern"""
        primary_success_rate = (self.primary_successes / max(1, self.primary_calls)) * 100
        fallback_success_rate = (self.fallback_successes / max(1, self.fallback_calls)) * 100
        
        return {
            "name": self.name,
            "fallback_strategies": len(self.fallback_strategies),
            "primary_calls": self.primary_calls,
            "primary_successes": self.primary_successes,
            "primary_success_rate": primary_success_rate,
            "fallback_calls": self.fallback_calls,
            "fallback_successes": self.fallback_successes,
            "fallback_success_rate": fallback_success_rate
        }

# Excepciones personalizadas
class CircuitBreakerOpenException(Exception):
    """Excepción lanzada cuando el circuit breaker está abierto"""
    pass

class BulkheadFullException(Exception):
    """Excepción lanzada cuando el bulkhead está saturado"""
    pass

class BulkheadTimeoutException(Exception):
    """Excepción lanzada cuando se excede el timeout en bulkhead"""
    pass

class TimeoutException(Exception):
    """Excepción lanzada cuando se excede un timeout"""
    pass

class RateLimitExceededException(Exception):
    """Excepción lanzada cuando se excede el límite de rate limiting"""
    pass

# Clase helper para combinar patrones
class ResiliencePatterns:
    """
    Clase que combina múltiples patrones de resiliencia.
    Facilita la aplicación de varios patrones a la vez.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.circuit_breaker = None
        self.bulkhead = None
        self.retry_policy = None
        self.rate_limiter = None
        self.timeout_pattern = None
        self.fallback_pattern = None
        
        logger.info(f"ResiliencePatterns '{name}' inicializado")
    
    def with_circuit_breaker(self, config: CircuitBreakerConfig = None):
        """Añade circuit breaker"""
        self.circuit_breaker = CircuitBreaker(f"{self.name}-cb", config)
        return self
    
    def with_bulkhead(self, max_concurrent: int = 10):
        """Añade bulkhead"""
        self.bulkhead = Bulkhead(f"{self.name}-bh", max_concurrent)
        return self
    
    def with_retry(self, max_attempts: int = 3, base_delay: float = 1.0):
        """Añade retry policy"""
        self.retry_policy = RetryPolicy(max_attempts, base_delay)
        return self
    
    def with_rate_limiter(self, rate: float, burst_size: int = None):
        """Añade rate limiter"""
        self.rate_limiter = RateLimiter(f"{self.name}-rl", rate, burst_size)
        return self
    
    def with_timeout(self, default_timeout: float = 30.0):
        """Añade timeout pattern"""
        self.timeout_pattern = TimeoutPattern(f"{self.name}-to", default_timeout)
        return self
    
    def with_fallback(self):
        """Añade fallback pattern"""
        self.fallback_pattern = FallbackPattern(f"{self.name}-fb")
        return self
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Ejecuta una función aplicando todos los patrones configurados.
        """
        def _wrapped_func(*args, **kwargs):
            return self._apply_rate_limiter_and_bulkhead(func, *args, **kwargs)

        def _timeout_wrapped_func(*args, **kwargs):
            if self.timeout_pattern:
                return self.timeout_pattern.execute(_wrapped_func, None, *args, **kwargs)
            else:
                return _wrapped_func(*args, **kwargs)

        def _circuit_breaker_wrapped_func(*args, **kwargs):
            if self.circuit_breaker:
                return self.circuit_breaker.call(_timeout_wrapped_func, *args, **kwargs)
            else:
                return _timeout_wrapped_func(*args, **kwargs)

        def _retry_wrapped_func(*args, **kwargs):
            if self.retry_policy:
                return self.retry_policy.execute(_circuit_breaker_wrapped_func, *args, **kwargs)
            else:
                return _circuit_breaker_wrapped_func(*args, **kwargs)

        # Aplicar fallback como capa externa
        if self.fallback_pattern:
            return self.fallback_pattern.execute(_retry_wrapped_func, *args, **kwargs)
        else:
            return _retry_wrapped_func(*args, **kwargs)
    def _apply_rate_limiter_and_bulkhead(self, func: Callable, *args, **kwargs):
        # Aplicar rate limiting
        if self.rate_limiter and not self.rate_limiter.acquire():
            raise RateLimitExceededException("Rate limit exceeded")

        # Aplicar bulkhead
        if self.bulkhead:
            return self.bulkhead.execute(func, None, *args, **kwargs)
        else:
            return func(*args, **kwargs)
    
    def get_all_metrics(self) -> Dict:
        """Retorna métricas de todos los patrones configurados"""
        metrics = {"name": self.name}
        
        if self.circuit_breaker:
            metrics["circuit_breaker"] = self.circuit_breaker.get_metrics()
        if self.bulkhead:
            metrics["bulkhead"] = self.bulkhead.get_metrics()
        if self.retry_policy:
            metrics["retry_policy"] = self.retry_policy.get_metrics()
        if self.rate_limiter:
            metrics["rate_limiter"] = self.rate_limiter.get_metrics()
        if self.timeout_pattern:
            metrics["timeout_pattern"] = self.timeout_pattern.get_metrics()
        if self.fallback_pattern:
            metrics["fallback_pattern"] = self.fallback_pattern.get_metrics()
        
        return metrics
