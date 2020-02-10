try:
    from .models import EsiClient  # noqa
    from .security import EsiSecurity  # noqa
    from .app import EsiApp  # noqa
    from pyswagger import App  # noqa
except ImportError:  # pragma: no cover
    # Not installed or in install (not yet installed) so ignore
    pass

__version__ = '1.1.0'