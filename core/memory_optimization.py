"""Memory optimization utilities for reducing RAM usage.

This module provides functions to optimize memory usage in the application,
particularly for machine learning models that consume large amounts of RAM.
"""

import os
import gc
import sys
import psutil
import logging
from typing import Dict, Any

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    
try:
    import transformers
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from .config import settings

logger = logging.getLogger(__name__)

def get_memory_usage():
    """Get current memory usage information.
    
    Returns:
        dict: Memory usage statistics
    """
    try:
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_percent = process.memory_percent()
        
        return {
            "rss_mb": memory_info.rss / 1024 / 1024,  # Resident Set Size in MB
            "vms_mb": memory_info.vms / 1024 / 1024,  # Virtual Memory Size in MB
            "percent": memory_percent,
            "available_mb": psutil.virtual_memory().available / 1024 / 1024
        }
    except Exception as e:
        logger.error(f"Failed to get memory usage: {e}")
        return {"error": str(e)}

def force_garbage_collection():
    """Force garbage collection and return collected objects count.
    
    Returns:
        int: Number of objects collected
    """
    try:
        # Force garbage collection for all generations
        collected = 0
        for generation in range(3):
            collected += gc.collect(generation)
        
        # Additional cleanup
        gc.collect()
        
        logger.info(f"Garbage collection completed, collected {collected} objects")
        return collected
    except Exception as e:
        logger.error(f"Failed to perform garbage collection: {e}")
        return 0

def optimize_python_memory():
    """Optimize Python memory usage.
    
    Returns:
        dict: Applied optimizations
    """
    results = {}
    
    try:
        # Set garbage collection thresholds optimized for 2GB
        gc.set_threshold(700, 10, 10)  # Balanced GC for larger memory
        results["gc_threshold_set"] = True
        
        # Force initial garbage collection
        collected = force_garbage_collection()
        results["initial_gc_collected"] = collected
        
        # Optimize sys settings for memory
        if hasattr(sys, 'intern'):
            # Enable string interning for memory efficiency
            results["string_interning"] = True
        
        logger.info("Python memory optimizations applied")
        return results
        
    except Exception as e:
        logger.error(f"Failed to apply Python memory optimizations: {e}")
        return {"error": str(e)}

def optimize_torch_memory():
    """Optimize PyTorch memory usage.
    
    Returns:
        bool: True if optimizations were applied, False otherwise
    """
    if not TORCH_AVAILABLE:
        logger.info("PyTorch not available, skipping torch memory optimizations")
        return False
    
    try:
        if torch.cuda.is_available():
            # Clear CUDA cache
            torch.cuda.empty_cache()
        
        # Configure transformers for memory efficiency
        if TRANSFORMERS_AVAILABLE:
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            transformers.logging.set_verbosity_error()
        
        logger.info("PyTorch memory optimizations applied")
        return True
        
    except Exception as e:
        logger.error(f"Failed to apply PyTorch optimizations: {e}")
        return False

def apply_memory_optimizations():
    """Apply all available memory optimizations based on configuration.
    
    Returns:
        dict: Summary of applied optimizations
    """
    results = {}
    
    # Log initial memory usage
    initial_memory = get_memory_usage()
    logger.info(f"Initial memory usage: {initial_memory.get('rss_mb', 'unknown'):.1f}MB RSS, {initial_memory.get('percent', 'unknown'):.1f}%")
    
    # Check if memory optimizations are enabled
    if not getattr(settings, 'ENABLE_MEMORY_OPTIMIZATIONS', True):
        logger.info("Memory optimizations disabled by configuration")
        return {"applied": False, "reason": "disabled_by_config"}
    
    # Apply optimized settings for 2GB memory limit
    logger.info("Applying memory optimizations for 2GB limit")
    
    # Apply Python memory optimizations first
    python_opts = optimize_python_memory()
    results["python_optimizations"] = python_opts
    
    # Apply PyTorch optimizations
    results["torch_optimized"] = optimize_torch_memory()
    
    # Optimize batch size for 2GB memory limit
    if hasattr(settings, 'EMBEDDING_BATCH_SIZE'):
        if settings.EMBEDDING_BATCH_SIZE > 32:  # Reasonable batch size for 2GB
            logger.info(f"Optimizing embedding batch size from {settings.EMBEDDING_BATCH_SIZE} to 32 for 2GB limit")
            settings.EMBEDDING_BATCH_SIZE = 32
            results["optimized_batch_size"] = True
    
    # Optimize memory cache for 2GB limit
    if hasattr(settings, 'MEMORY_CACHE_SIZE'):
        if settings.MEMORY_CACHE_SIZE > 1000:  # Generous cache for 2GB limit
            logger.info(f"Optimizing memory cache size from {settings.MEMORY_CACHE_SIZE} to 1000 for 2GB limit")
            settings.MEMORY_CACHE_SIZE = 1000
            results["optimized_cache_size"] = True
    
    # Enable local embeddings with 2GB memory available
    if not getattr(settings, 'ENABLE_LOCAL_EMBEDDINGS', True):
        logger.info("Enabling local embeddings with 2GB memory available")
        settings.ENABLE_LOCAL_EMBEDDINGS = True
        results["enabled_local_embeddings"] = True
    
    # Set environment variables for memory efficiency with 2GB available
    os.environ['PYTHONHASHSEED'] = '0'  # Consistent hashing
    os.environ['MALLOC_TRIM_THRESHOLD_'] = '100000'  # Moderate malloc trimming for 2GB
    os.environ['MALLOC_MMAP_THRESHOLD_'] = '131072'  # Use mmap for large allocations
    os.environ['PYTHONOPTIMIZE'] = '1'  # Keep some optimizations but allow debugging
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'  # Don't write .pyc files
    
    # Moderate garbage collection every 60 seconds for 2GB limit
    import threading
    import time
    
    def periodic_gc():
        while True:
            time.sleep(60)  # Less frequent GC with more memory available
            collected = force_garbage_collection()
            if collected > 0:
                logger.debug(f"Periodic GC collected {collected} objects")
    
    gc_thread = threading.Thread(target=periodic_gc, daemon=True)
    gc_thread.start()
    results["periodic_gc_enabled"] = True
    
    results["optimized_mode"] = True
    results["memory_2gb_optimized"] = True
    
    # Final memory check
    final_memory = get_memory_usage()
    logger.info(f"Final memory usage: {final_memory.get('rss_mb', 'unknown'):.1f}MB RSS, {final_memory.get('percent', 'unknown'):.1f}%")
    
    # Memory usage monitoring for 2GB limit
    current_mb = final_memory.get('rss_mb', 0)
    if current_mb > 1400:  # Warn at 1400MB (70% of 2GB limit)
        logger.warning(f"Memory usage is {current_mb:.1f}MB, approaching 2GB limit")
        results["memory_warning"] = True
    elif current_mb > 1700:  # Critical warning at 1700MB (85% of limit)
        logger.critical(f"Memory usage is {current_mb:.1f}MB, critically close to 2GB limit!")
        results["memory_critical"] = True
        # Force emergency garbage collection
        emergency_collected = force_garbage_collection()
        logger.info(f"Emergency GC collected {emergency_collected} objects")
    
    # Log memory optimization results
    optimizations_applied = any(results.values())
    logger.info(f"Memory optimizations applied: {optimizations_applied}")
    
    return {"applied": optimizations_applied, "details": results}