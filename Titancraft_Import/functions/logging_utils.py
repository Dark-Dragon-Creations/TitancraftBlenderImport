"""
Logging utilities for Titancraft Import add-on.
Provides proper error reporting and logging functionality.
"""

import bpy  # type: ignore
import logging
from typing import Optional, Union

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TitancraftLogger:
    """Custom logger for Titancraft Import add-on."""
    
    def __init__(self, operator_instance: Optional[bpy.types.Operator] = None):
        self.operator = operator_instance
    
    def info(self, message: str) -> None:
        """Log info message and report to Blender if operator available."""
        logger.info(message)
        if self.operator:
            self.operator.report({'INFO'}, message)
    
    def warning(self, message: str) -> None:
        """Log warning message and report to Blender if operator available."""
        logger.warning(message)
        if self.operator:
            self.operator.report({'WARNING'}, message)
    
    def error(self, message: str) -> None:
        """Log error message and report to Blender if operator available."""
        logger.error(message)
        if self.operator:
            self.operator.report({'ERROR'}, message)
    
    def debug(self, message: str) -> None:
        """Log debug message (only to console, not Blender UI)."""
        logger.debug(message)
    
    def success(self, message: str) -> None:
        """Log success message and report to Blender if operator available."""
        logger.info(f"SUCCESS: {message}")
        if self.operator:
            self.operator.report({'INFO'}, f"✓ {message}")

def get_logger(operator_instance: Optional[bpy.types.Operator] = None) -> TitancraftLogger:
    """Get a logger instance, optionally with operator for Blender reporting."""
    return TitancraftLogger(operator_instance)

def log_operation_start(operation_name: str, logger: TitancraftLogger) -> None:
    """Log the start of an operation."""
    logger.info(f"Starting {operation_name}...")

def log_operation_success(operation_name: str, logger: TitancraftLogger) -> None:
    """Log successful completion of an operation."""
    logger.success(f"{operation_name} completed successfully")

def log_operation_error(operation_name: str, error: Union[str, Exception], logger: TitancraftLogger) -> None:
    """Log an operation error."""
    error_msg = str(error) if isinstance(error, Exception) else error
    logger.error(f"{operation_name} failed: {error_msg}")

def log_file_operation(operation: str, file_path: str, logger: TitancraftLogger) -> None:
    """Log file operations with path information."""
    logger.debug(f"{operation}: {file_path}")

def log_node_operation(node_name: str, operation: str, logger: TitancraftLogger) -> None:
    """Log node operations in material editor."""
    logger.debug(f"Node '{node_name}': {operation}")

def log_progress(current: int, total: int, operation: str, logger: TitancraftLogger) -> None:
    """Log progress for long operations."""
    percentage = (current / total) * 100
    logger.debug(f"{operation}: {current}/{total} ({percentage:.1f}%)")
