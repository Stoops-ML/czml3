from importlib.metadata import version

from .core import CZML_VERSION, Document, Packet

__version__ = version("czml3")
__all__ = ["CZML_VERSION", "Document", "Packet", "__version__"]
