from .interfaces import IDataLoader, IVisualizer
from .analyzers import AnalysisContext, PublicationTrendAnalyzer, AuthorsAnalyzer, LanguageDistributionAnalyzer, PublisherAnalyzer, MissingISBNAnalyzer, LanguageYearAnalyzer
from .visualizers import VisualizerFactory
from .data_loader import CSVDataLoader
import sys

# Clean Coding: High-level Orchestration
# The CLI class orchestrates the interaction between data loading, analysis, and visualization.
class CLI:
    def __init__(self, file_path: str):
        self.file_path = file_path
        # SOLID Principle: Dependency Injection (though simplified here)
        # The CLI relies on CSVDataLoader and AnalysisContext.
        self.loader = CSVDataLoader(limit=5000)
        self.analyzers = AnalysisContext()
        self.data = None
        self.viz_type = 'matplotlib' # Default

        # Register Analyzers
        self.analyzers.register_analyzer("1", PublicationTrendAnalyzer())
        self.analyzers.register_analyzer("2", AuthorsAnalyzer())
        self.analyzers.register_analyzer("3", LanguageDistributionAnalyzer())
        self.analyzers.register_analyzer("4", PublisherAnalyzer())
        self.analyzers.register_analyzer("5", MissingISBNAnalyzer())
        self.analyzers.register_analyzer("6", LanguageYearAnalyzer())

    def run(self):
        print("Loading data...")
        try:
            self.data = self.loader.load_data(self.file_path)
            print(f"Data loaded successfully. {len(self.data)} rows processed.")
        except Exception as e:
            print(f"Error loading data: {e}")
            return

        while True:
            # Programming Pattern: Factory Pattern usage
            # Re-create visualizer in case user switched types
            visualizer = VisualizerFactory.get_visualizer(self.viz_type)

            print(f"\n--- Dream Book Shop Data Analysis (Visualizer: {self.viz_type}) ---")
            print("v. Toggle Visualizer")
            print("1. Publication Trends Over Time")
            print("2. Top 5 Most Prolific Authors")
            print("3. Language Distribution")
            print("4. Number of books published by each publisher")
            print("5. Missing ISBN Analysis")
            print("6. Number of books published per year categorized by language")
            print("q. Quit")
            
            choice = input("Select an analysis (1-6, v, q): ")
            
            if choice.lower() == 'q':
                break
            
            if choice.lower() == 'v':
                if self.viz_type == 'matplotlib':
                    self.viz_type = 'plotly'
                else:
                    self.viz_type = 'matplotlib'
                continue
            
            analyzer = self.analyzers.get_analyzer(choice)
            if analyzer:
                print(f"\nPerforming: {analyzer.name}...")
                result = analyzer.analyze(self.data)
                
                # Textual Summary
                print("\n--- Textual Summary ---")
                if isinstance(result, dict) and "trend_line" in result:
                     print(result['counts'])
                     if result['trend_line']:
                         print(result['trend_line']['description'])
                elif choice == "4":
                    print(result.to_string())
                elif choice != "6":
                    print(result)
                
                # Visualization
                if choice == "1":
                    # Result is dict for trends now
                    visualizer.visualize(result, analyzer.name, chart_type='line')
                elif choice == "2":
                    visualizer.visualize(result, analyzer.name, chart_type='bar')
                elif choice == "3":
                    if len(result) > 10:
                        top_languages = result.head(10).copy()
                        other_count = result.iloc[10:].sum()
                        top_languages['Other'] = other_count
                    else:
                        top_languages = result
                    visualizer.visualize(top_languages, analyzer.name, chart_type='bar')
                elif choice == "4":
                    if len(result) > 10:
                        top_publishers = result.head(10).copy()
                        other_count = result.iloc[10:].sum()
                        top_publishers['Other'] = other_count
                    else:
                        top_publishers = result
                    visualizer.visualize(top_publishers, analyzer.name, chart_type='bar')
                elif choice == "5":
                    # Custom text summary for ISBN
                    total = result.sum()
                    missing = result['Missing ISBN']
                    print(f"Total Books: {total}")
                    print(f"Missing ISBN: {missing} ({(missing/total)*100:.2f}%)")
                    print(f"With ISBN: {result['With ISBN']} ({(result['With ISBN']/total)*100:.2f}%)")
                    
                    visualizer.visualize(result, analyzer.name, chart_type='pie') 
                elif choice == "6":
                    print(result.to_string())
                    visualizer.visualize(result, analyzer.name, chart_type='line')
            else:
                print("Invalid selection.")

if __name__ == "__main__":
    pass
