"""Compatibility package for embedded and standalone worker execution.

The worker image runs its source as the top-level ``src`` package,
while the backend imports it as ``ai_workers.src``. Registering the
embedded package under the standalone name keeps both entry points
using the same modules without requiring a custom PYTHONPATH.
"""

from importlib import import_module
import sys


worker_source = import_module("ai_workers.src")
sys.modules.setdefault("src", worker_source)
