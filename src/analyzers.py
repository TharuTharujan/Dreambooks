from typing import Any, List, Dict
import pandas as pd
import numpy as np
from scipy import stats
from .interfaces import IAnalyzer

# Programming Pattern: Strategy Pattern
# Each analyzer class (PublicationTrendAnalyzer, AuthorsAnalyzer, etc.) implements a specific strategy for data analysis.
# SOLID Principle: Open/Closed Principle (OCP)
# The system is open for extension (adding new analyzers) but closed for modification.
class PublicationTrendAnalyzer(IAnalyzer):
    @property
    def name(self) -> str:
        return "Publication Trends Over Time"

    def analyze(self, data: pd.DataFrame) -> pd.Series:
        # Filter valid years (numeric)
        data = data.dropna(subset=['publication date'])
        # Convert to numeric, errors='coerce' turns non-numeric to NaN
        years = pd.to_numeric(data['publication date'], errors='coerce').dropna().astype(int)
        
        # Filter for reasonable years (e.g., 1000 to current year + small buffer)
        years = years[(years > 1000) & (years < 2100)]
        
        trends = years.value_counts().sort_index()
        
        # Calculate trend line using scipy
        if not trends.empty:
            x = trends.index.to_numpy() # usage of numpy
            y = trends.values
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # Return both actual counts and the trend info
            # We'll return a dict to hold both, visualizer will need to adapt
            return {
                "counts": trends,
                "trend_line": {
                    "slope": slope,
                    "intercept": intercept,
                    "r_value": r_value,
                    "description": f"Linear Trend: y = {slope:.2f}x + {intercept:.2f} (R2={r_value**2:.2f})"
                }
            }
        
        return {"counts": trends, "trend_line": None}

class AuthorsAnalyzer(IAnalyzer):
    @property
    def name(self) -> str:
        return "Top 5 Most Prolific Authors"

    def analyze(self, data: pd.DataFrame) -> pd.Series:
        authors = data['author'].value_counts().head(5)
        return authors

class LanguageDistributionAnalyzer(IAnalyzer):
    @property
    def name(self) -> str:
        return "Language Distribution"

    def analyze(self, data: pd.DataFrame) -> pd.Series:
        languages = data['language'].value_counts()
        return languages

class PublisherAnalyzer(IAnalyzer):
    @property
    def name(self) -> str:
        return "Number of books published by each publisher"

    def analyze(self, data: pd.DataFrame) -> pd.Series:
        publishers = data['book publisher'].value_counts()
        return publishers

class MissingISBNAnalyzer(IAnalyzer):
    @property
    def name(self) -> str:
        return "Missing ISBN Analysis"

    def analyze(self, data: pd.DataFrame) -> pd.Series:
        total = len(data)
        missing_count = data['ISBN'].isna().sum()
        present_count = total - missing_count
        
        return pd.Series(
            [missing_count, present_count], 
            index=['Missing ISBN', 'With ISBN']
        )

class LanguageYearAnalyzer(IAnalyzer):
    @property
    def name(self) -> str:
        return "Number of books published per year categorized by language"

    def analyze(self, data: pd.DataFrame) -> pd.DataFrame:
        # Group by year and language
        # Pivot or simple group size
        grouped = data.groupby(['publication date', 'language']).size().unstack(fill_value=0)
        return grouped

# OOP Concept: Encapsulation
# AnalysisContext encapsulates the registration and retrieval of analyzers.
class AnalysisContext:
    def __init__(self):
        self._analyzers: Dict[str, IAnalyzer] = {}

    def register_analyzer(self, key: str, analyzer: IAnalyzer):
        self._analyzers[key] = analyzer

    def get_analyzer(self, key: str) -> IAnalyzer:
        return self._analyzers.get(key)
    
    def get_available_analyses(self) -> List[str]:
        return list(self._analyzers.keys())
