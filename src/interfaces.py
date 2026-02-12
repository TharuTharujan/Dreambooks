from abc import ABC, abstractmethod
from typing import Any, List
import pandas as pd

import sys
import os

# Ensure the src directory is in the path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# OOP Concept: Abstraction
# IDataLoader is an interface (Abstract Base Class) that defines the contract for loading data.
# SOLID Principle: Interface Segregation Principle (ISP) - Specific interfaces for specific tasks.
class IDataLoader(ABC):
    """Interface for loading data."""
    @abstractmethod
    def load_data(self, file_path: str) -> pd.DataFrame:
        pass

# SOLID Principle: Dependency Inversion Principle (DIP)
# High-level modules depend on abstractions (IAnalyzer), not low-level implementations.
class IAnalyzer(ABC):
    """Interface for analyzing data."""
    @abstractmethod
    def analyze(self, data: pd.DataFrame) -> Any:
        pass
        
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the analysis."""
        pass

# OOP Concept: Polymorphism
# IVisualizer allows different visualization implementations (Matplotlib, Plotly) to be used interchangeably.
class IVisualizer(ABC):
    """Interface for visualizing data."""
    @abstractmethod
    def visualize(self, data: Any, title: str, chart_type: str = 'bar') -> None:
        pass
