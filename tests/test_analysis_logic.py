import pytest
import pandas as pd
import numpy as np
import os
import sys
from scipy import stats

# Ensure src can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.analyzers import (
    PublicationTrendAnalyzer, 
    AuthorsAnalyzer, 
    LanguageDistributionAnalyzer, 
    PublisherAnalyzer, 
    MissingISBNAnalyzer, 
    LanguageYearAnalyzer
)
@pytest.fixture(scope="module")
def sample_data():
    """
    Fixture to provide a small, predictable sample dataset for scripted testing.
    """
    data = {
        'publication date': ['2020', '2021', '2020', 'Invalid', None, '2022', '1900', '2150'],
        'author': ['Author A', 'Author B', 'Author A', 'Author C', 'Author A', 'Author B', 'Author D', 'Author E'],
        'language': ['English', 'Tamil', 'English', 'French', 'English', 'Tamil', 'Spanish', 'German'],
        'book publisher': ['Pub 1', 'Pub 2', 'Pub 1', 'Pub 3', 'Pub 1', 'Pub 2', 'Pub 4', 'Pub 5'],
        'ISBN': ['123', '456', None, '789', None, '012', '345', '678']
    }
    return pd.DataFrame(data)

def test_publication_trends_logic(sample_data):
    """
    Validates Option 1: Publication Trends Over Time
    """
    analyzer = PublicationTrendAnalyzer()
    result = analyzer.analyze(sample_data)
    
    # Replicate Logic for sample_data
    # 2020 (2), 2021 (1), 2022 (1). 1900 and 2150 might be filtered if range is tight, 
    # but the logic uses (1000 < year < 2100).
    # So: 2020, 2021, 2022, 1900 should be valid.
    expected_counts = pd.Series([1, 2, 1, 1], index=[1900, 2020, 2021, 2022]).sort_index()
    expected_counts.index.name = 'publication date'
    
    # 1. Validate Counts
    pd.testing.assert_series_equal(result['counts'], expected_counts, obj="Trend Counts", check_names=False)
    
    # 2. Validate Trend Line Logic
    if not expected_counts.empty:
        x = expected_counts.index.to_numpy()
        y = expected_counts.values
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        trend_res = result['trend_line']
        assert trend_res is not None
        assert trend_res['slope'] == pytest.approx(slope)
        assert trend_res['intercept'] == pytest.approx(intercept)
        assert trend_res['r_value'] == pytest.approx(r_value)

def test_top_authors_logic(sample_data):
    """
    Validates Option 2: Top 5 Most Prolific Authors
    """
    analyzer = AuthorsAnalyzer()
    result = analyzer.analyze(sample_data)
    
    # Author A: 3, Author B: 2, Others: 1
    expected = pd.Series([3, 2, 1, 1, 1], 
                        index=['Author A', 'Author B', 'Author C', 'Author D', 'Author E'], 
                        name='count')
    # The analyzer output might have different index name or order for ties, let's be careful
    # But usually value_counts() handles this.
    pd.testing.assert_series_equal(result, expected, obj="Top 5 Authors", check_names=False)

def test_language_distribution_logic(sample_data):
    """
    Validates Option 3: Language Distribution
    """
    analyzer = LanguageDistributionAnalyzer()
    result = analyzer.analyze(sample_data)
    
    expected = sample_data['language'].value_counts()
    pd.testing.assert_series_equal(result, expected, obj="Language Distribution", check_names=False)

def test_publisher_counts_logic(sample_data):
    """
    Validates Option 4: Number of books published by each publisher
    """
    analyzer = PublisherAnalyzer()
    result = analyzer.analyze(sample_data)
    
    expected = sample_data['book publisher'].value_counts()
    pd.testing.assert_series_equal(result, expected, obj="Publisher Counts", check_names=False)

def test_missing_isbn_logic(sample_data):
    """
    Validates Option 5: Missing ISBN Analysis
    """
    analyzer = MissingISBNAnalyzer()
    result = analyzer.analyze(sample_data)
    
    # Total 8, Missing: index 2, 4 (2 total), Present: 6
    expected = pd.Series([2, 6], index=['Missing ISBN', 'With ISBN'])
    pd.testing.assert_series_equal(result, expected, obj="Missing ISBN Stats", check_names=False)

def test_language_year_logic(sample_data):
    """
    Validates Option 6: Number of books published per year categorized by language
    """
    analyzer = LanguageYearAnalyzer()
    result = analyzer.analyze(sample_data)
    
    expected = sample_data.groupby(['publication date', 'language']).size().unstack(fill_value=0)
    pd.testing.assert_frame_equal(result, expected, obj="Language Per Year Grid")

if __name__ == "__main__":
    # Allows running this file directly with Python (e.g. via Play button)
    # This invokes pytest on this file
    sys.exit(pytest.main(["-v", __file__]))
