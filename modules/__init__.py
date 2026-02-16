"""
Mangrove Bibliography Dashboard

A modular Streamlit application for exploring
scientific literature on mangrove mapping
using remote sensing and AI.
"""

__author__ = "Your Name"
__version__ = "0.1.0"

# Public API of the package
from .config import *
from .data_loader import *
from .filters import *
from .metrics import *
from .visuals import *
from .sort_table import *