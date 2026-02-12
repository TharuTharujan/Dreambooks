from typing import Any, Dict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from .interfaces import IVisualizer

# SOLID Principle: Liskov Substitution Principle (LSP)
# MatplotlibVisualizer and PlotlyVisualizer can both be used as IVisualizer without changing the client code.
class MatplotlibVisualizer(IVisualizer):
    def visualize(self, data: Any, title: str, chart_type: str = 'bar') -> None:
        """
        Visualizes the data using matplotlib in a new window.
        """
        # Handle dict from PublicationTrendAnalyzer
        if isinstance(data, dict) and "counts" in data:
            self._visualize_trend_with_matplotlib(data, title)
            return

        plt.figure(figsize=(10, 6))
        plt.title(title)
        
        if chart_type == 'bar':
            if isinstance(data, pd.Series):
                data.plot(kind='bar')
                xlabel = data.index.name.capitalize() if data.index.name else 'Category'
                plt.xlabel(xlabel)
                plt.ylabel('No. of Books')
            elif isinstance(data, pd.DataFrame):
                data.plot(kind='bar')
        
        elif chart_type == 'line':
            if isinstance(data, pd.Series):
                data.plot(kind='line', marker='o')
                plt.xlabel('Year')
                plt.ylabel('Count')
                plt.grid(True)
            elif isinstance(data, pd.DataFrame):
                data.plot(kind='line', marker='o')
                plt.xlabel('Year')
                plt.ylabel('Count')
                plt.legend(title='Language', bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.figtext(0.99, 0.01, f'Total Years: {len(data.index)}', horizontalalignment='right') 
                plt.xticks(data.index, rotation=90)
                plt.grid(True)
        
        elif chart_type == 'pie':
            if isinstance(data, pd.Series):
                data.plot(kind='pie', autopct='%1.1f%%')
                plt.ylabel('')
        
        plt.tight_layout()
        plt.show()

    def _visualize_trend_with_matplotlib(self, data: Dict, title: str):
        counts = data['counts']
        trend = data['trend_line']
        
        plt.figure(figsize=(10, 6))
        plt.title(title)
        
        # Plot actual data
        counts.plot(kind='line', marker='o', label='Actual Counts')
        
        # Plot trend line if exists
        if trend:
            x = counts.index.to_numpy()
            y_trend = trend['slope'] * x + trend['intercept']
            plt.plot(x, y_trend, color='red', linestyle='--', label='Trend Line')
            plt.title(f"{title}\n{trend['description']}")
            
        plt.xlabel('Year')
        plt.ylabel('Count')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

class PlotlyVisualizer(IVisualizer):
    def visualize(self, data: Any, title: str, chart_type: str = 'bar') -> None:
        """
        Visualizes the data using Plotly.
        """
        fig = None
        
        # Handle dict from PublicationTrendAnalyzer
        if isinstance(data, dict) and "counts" in data:
            self._visualize_trend_with_plotly(data, title)
            return

        if chart_type == 'bar':
            if isinstance(data, pd.Series):
                xlabel = data.index.name.capitalize() if data.index.name else 'Category'
                fig = px.bar(x=data.index, y=data.values, labels={'x': xlabel, 'y': 'No. of Books'}, title=title)
            elif isinstance(data, pd.DataFrame):
                # For stacked or grouped bars
                fig = px.bar(data, title=title)
        
        elif chart_type == 'line':
            if isinstance(data, pd.Series):
                fig = px.line(x=data.index, y=data.values, labels={'x': 'Year', 'y': 'Count'}, title=title)
            elif isinstance(data, pd.DataFrame):
                fig = px.line(data, markers=True, title=title)
        
        elif chart_type == 'pie':
            if isinstance(data, pd.Series):
                fig = px.pie(values=data.values, names=data.index, title=title)

        if fig:
            fig.show()

    def _visualize_trend_with_plotly(self, data: Dict, title: str):
        counts = data['counts']
        trend = data['trend_line']
        
        fig = go.Figure()
        
        # Actual Data
        fig.add_trace(go.Scatter(x=counts.index, y=counts.values, mode='lines+markers', name='Actual Counts'))
        
        # Trend Line
        if trend:
            x = counts.index.to_numpy()
            y_trend = trend['slope'] * x + trend['intercept']
            fig.add_trace(go.Scatter(x=x, y=y_trend, mode='lines', name='Trend Line', line=dict(dash='dash', color='red')))
            title = f"{title}<br>{trend['description']}"
            
        fig.update_layout(title=title, xaxis_title='Year', yaxis_title='Count')
        fig.show()

# Programming Pattern: Factory Method Pattern
# VisualizerFactory abstracts the instantiation logic of visualizers.
class VisualizerFactory:
    @staticmethod
    def get_visualizer(viz_type: str) -> IVisualizer:
        if viz_type == 'plotly':
            return PlotlyVisualizer()
        return MatplotlibVisualizer()
