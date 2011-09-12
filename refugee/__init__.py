__import__('pkg_resources').declare_namespace(__name__)

from refugee.migration import Migration
from refugee.manager import migration_manager, register

__all__ = ['Migration', 'migration_manager', 'register']
__doc__ = """\
Namespace for refugee
"""
