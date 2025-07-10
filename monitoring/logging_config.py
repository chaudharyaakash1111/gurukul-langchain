#!/usr/bin/env python3
"""
🔍 Akash Gurukul - Enterprise Logging and Monitoring System
Comprehensive logging, metrics, and monitoring for production deployment
"""

import logging
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import uuid
from functools import wraps

class GurukulLogger:
    """Enterprise-grade logging system for Akash Gurukul"""
    
    def __init__(self, log_level: str = "INFO"):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # Configure main logger
        self.logger = logging.getLogger("akash_gurukul")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colors
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler for all logs
        file_handler = logging.FileHandler(
            self.log_dir / f"gurukul_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # JSON handler for structured logs
        json_handler = logging.FileHandler(
            self.log_dir / f"gurukul_structured_{datetime.now().strftime('%Y%m%d')}.json"
        )
        json_handler.setFormatter(self.JSONFormatter())
        self.logger.addHandler(json_handler)
        
        self.logger.info("Akash Gurukul logging system initialized")
    
    class JSONFormatter(logging.Formatter):
        """JSON formatter for structured logging"""
        
        def format(self, record):
            log_entry = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "function": record.funcName,
                "line": record.lineno,
                "message": record.getMessage(),
                "module": record.module
            }
            
            # Add extra fields if present
            if hasattr(record, 'student_id'):
                log_entry['student_id'] = record.student_id
            if hasattr(record, 'agent_type'):
                log_entry['agent_type'] = record.agent_type
            if hasattr(record, 'conversation_id'):
                log_entry['conversation_id'] = record.conversation_id
            if hasattr(record, 'response_time'):
                log_entry['response_time'] = record.response_time
            if hasattr(record, 'confidence_score'):
                log_entry['confidence_score'] = record.confidence_score
                
            return json.dumps(log_entry)
    
    def log_agent_interaction(self, agent_type: str, student_id: str, 
                            message: str, response: str, 
                            conversation_id: str, response_time: float,
                            confidence_score: float):
        """Log agent interaction with structured data"""
        extra = {
            'student_id': student_id,
            'agent_type': agent_type,
            'conversation_id': conversation_id,
            'response_time': response_time,
            'confidence_score': confidence_score
        }
        
        self.logger.info(
            f"Agent interaction: {agent_type} responded to student {student_id} "
            f"(confidence: {confidence_score:.2f}, time: {response_time:.2f}s)",
            extra=extra
        )
    
    def log_memory_operation(self, operation: str, agent_type: str, 
                           student_id: str, success: bool, details: str = ""):
        """Log memory operations"""
        extra = {
            'student_id': student_id,
            'agent_type': agent_type
        }
        
        level = logging.INFO if success else logging.ERROR
        status = "SUCCESS" if success else "FAILED"
        
        self.logger.log(
            level,
            f"Memory {operation}: {status} for {agent_type} agent, student {student_id}. {details}",
            extra=extra
        )
    
    def log_api_request(self, endpoint: str, method: str, status_code: int, 
                       response_time: float, student_id: str = None):
        """Log API requests"""
        extra = {
            'response_time': response_time
        }
        if student_id:
            extra['student_id'] = student_id
            
        self.logger.info(
            f"API {method} {endpoint} -> {status_code} ({response_time:.2f}s)",
            extra=extra
        )
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log errors with context"""
        extra = context or {}
        
        self.logger.error(
            f"Error occurred: {type(error).__name__}: {str(error)}",
            extra=extra,
            exc_info=True
        )

class MetricsCollector:
    """Collect and track system metrics"""
    
    def __init__(self):
        self.metrics = {
            'agent_interactions': 0,
            'successful_responses': 0,
            'failed_responses': 0,
            'memory_operations': 0,
            'api_requests': 0,
            'average_response_time': 0.0,
            'agent_usage': {'seed': 0, 'tree': 0, 'sky': 0},
            'confidence_scores': [],
            'active_students': set(),
            'total_conversations': 0
        }
        self.start_time = time.time()
        
    def record_agent_interaction(self, agent_type: str, student_id: str, 
                               response_time: float, confidence_score: float, 
                               success: bool):
        """Record agent interaction metrics"""
        self.metrics['agent_interactions'] += 1
        self.metrics['agent_usage'][agent_type] += 1
        self.metrics['active_students'].add(student_id)
        
        if success:
            self.metrics['successful_responses'] += 1
        else:
            self.metrics['failed_responses'] += 1
            
        # Update average response time
        current_avg = self.metrics['average_response_time']
        total_interactions = self.metrics['agent_interactions']
        self.metrics['average_response_time'] = (
            (current_avg * (total_interactions - 1) + response_time) / total_interactions
        )
        
        # Track confidence scores
        self.metrics['confidence_scores'].append(confidence_score)
        if len(self.metrics['confidence_scores']) > 1000:  # Keep last 1000
            self.metrics['confidence_scores'] = self.metrics['confidence_scores'][-1000:]
    
    def record_memory_operation(self, success: bool):
        """Record memory operation metrics"""
        self.metrics['memory_operations'] += 1
    
    def record_api_request(self):
        """Record API request metrics"""
        self.metrics['api_requests'] += 1
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        uptime = time.time() - self.start_time
        
        avg_confidence = (
            sum(self.metrics['confidence_scores']) / len(self.metrics['confidence_scores'])
            if self.metrics['confidence_scores'] else 0.0
        )
        
        success_rate = (
            self.metrics['successful_responses'] / max(self.metrics['agent_interactions'], 1)
        ) * 100
        
        return {
            'system_uptime_seconds': uptime,
            'total_agent_interactions': self.metrics['agent_interactions'],
            'success_rate_percentage': success_rate,
            'average_response_time_seconds': self.metrics['average_response_time'],
            'average_confidence_score': avg_confidence,
            'agent_usage_distribution': self.metrics['agent_usage'],
            'active_students_count': len(self.metrics['active_students']),
            'total_api_requests': self.metrics['api_requests'],
            'memory_operations': self.metrics['memory_operations'],
            'timestamp': datetime.now().isoformat()
        }

def log_performance(func):
    """Decorator to log function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function_id = str(uuid.uuid4())[:8]
        
        logger = logging.getLogger("akash_gurukul.performance")
        logger.info(f"Starting {func.__name__} (ID: {function_id})")
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger.info(
                f"Completed {func.__name__} (ID: {function_id}) in {execution_time:.2f}s"
            )
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Failed {func.__name__} (ID: {function_id}) after {execution_time:.2f}s: {e}"
            )
            raise
            
    return wrapper

def log_agent_call(func):
    """Decorator specifically for agent function calls"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        
        # Extract context
        student_id = getattr(self, 'student_id', 'unknown')
        agent_type = getattr(self, 'agent_type', 'unknown')
        
        logger = logging.getLogger("akash_gurukul.agents")
        
        try:
            result = func(self, *args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log successful agent call
            extra = {
                'student_id': student_id,
                'agent_type': agent_type,
                'response_time': execution_time
            }
            
            logger.info(
                f"Agent {agent_type} successfully processed request for student {student_id}",
                extra=extra
            )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            extra = {
                'student_id': student_id,
                'agent_type': agent_type,
                'response_time': execution_time
            }
            
            logger.error(
                f"Agent {agent_type} failed to process request for student {student_id}: {e}",
                extra=extra
            )
            raise
            
    return wrapper

# Global instances
gurukul_logger = GurukulLogger()
metrics_collector = MetricsCollector()

# Export for easy import
__all__ = [
    'GurukulLogger', 
    'MetricsCollector', 
    'log_performance', 
    'log_agent_call',
    'gurukul_logger',
    'metrics_collector'
]
