from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import column

class BaseVisualizer:
    """
    Base class for visualizing data using Bokeh.
    """
    def __init__(self, train_df, ideal_df, test_results_df):
        self.train_df = train_df
        self.ideal_df = ideal_df
        self.test_results_df = test_results_df

class Visualizer(BaseVisualizer):
    """
    Visualizer class for creating plots of the training data, ideal functions, and test results.

    Methods:
        visualize: Create and display the plots.
    """
    def __init__(self, train_df, ideal_df, test_results_df):
        super().__init__(train_df, ideal_df, test_results_df)

    def visualize(self):
        """
        Create and display plots for training data, ideal functions, and test results using Bokeh.
        """
        try:
            plots = []
            if 'Train Function' not in self.test_results_df.columns:
                raise KeyError("'Train Function' not found in test_results_df columns")

            for ideal_func in self.test_results_df['Ideal Function'].unique():
                if ideal_func not in self.ideal_df.columns:
                    print(f"Skipping visualization for {ideal_func} as it is not present in ideal_df columns.")
                    continue
                
                print(f"Visualizing {ideal_func}...")

                if self.ideal_df[ideal_func].isnull().all():
                    print(f"Skipping visualization for {ideal_func} in ideal_df as it contains only NaN values.")
                    continue

                p = figure(title=f'Function: {ideal_func}', x_axis_label='x', y_axis_label='y')

                train_func = self.test_results_df[self.test_results_df['Ideal Function'] == ideal_func]['Train Function'].iloc[0]
                if train_func not in self.train_df.columns:
                    print(f"Skipping visualization for {ideal_func} as {train_func} is not present in train_df columns.")
                    continue

                source_train = ColumnDataSource(data={
                    'x': self.train_df['x'], 
                    'y': self.train_df[train_func]
                })
                p.line('x', 'y', source=source_train, legend_label=f'Train: {train_func}', line_color='blue')

                source_ideal = ColumnDataSource(data={
                    'x': self.ideal_df['x'], 
                    'y': self.ideal_df[ideal_func]
                })
                p.line('x', 'y', source=source_ideal, legend_label=f'Ideal: {ideal_func}', line_color='green')

                test_data = self.test_results_df[self.test_results_df['Ideal Function'] == ideal_func]
                source_test = ColumnDataSource(data={
                    'x': test_data['x'], 
                    'y': test_data['y']
                })
                p.circle('x', 'y', source=source_test, legend_label='Test Data', fill_color='red', size=8)

                p.legend.title = 'Legend'
                plots.append(p)

            if plots:
                show(column(*plots))
            else:
                print("No valid plots to display.")

        except KeyError as e:
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise
