
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Avoid backend conflicts
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from PyQt6.QtWidgets import QWidget, QHBoxLayout


class TrendChartWidget(QWidget):
    """
    A PyQt6 widget embedding a Matplotlib chart for trend visualization.
    Supports adding/removing lines by name from pandas DataFrames.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create Matplotlib Figure and Canvas
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.figure.tight_layout(rect=[0, 0, 0.78, 1])

        # Track lines by name
        self._lines = {}

        self.init_axes_()

        # Layout
        layout = QHBoxLayout(self)
        layout.addWidget(self.canvas)

    def init_axes_(self, x_label: str = "Año", y_label: str = "S HV [MVA]"):
        """Initialize axis labels and clear existing content."""
        self.ax.clear()
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.grid(True)
        self._lines.clear()
        self.canvas.draw()

    def add_line(
        self,
        name: str,
        df: pd.DataFrame,
        color = None
    ):
        """Add a line from a DataFrame."""
        ## If the years fix range time when a data with less years is called first, remake the line chart deleting everything and then redrawing (the next if would be removed)
        if name in self._lines: ## It can improve because data already used is still brought in (The good part is that data is not being rep)
            raise ValueError(f"Line '{name}' already exists.")

        df = df.set_index('Año')

        # Plot line
        line, = self.ax.plot(df, label=name, color=color) ## Include color restriction
        self._lines[name] = line

        # Force integer ticks on the x-axis
        self.ax.xaxis.set_major_locator(MaxNLocator(integer=True)) 

        # Update legend and redraw
        self.ax.legend(loc='center left', fontsize = 10, bbox_to_anchor=(1.005, 0.5))
        self.canvas.draw()

        self.autoscale_triggered()

    def remove_line(self, name: str):
        """Remove a line by name."""
        if name not in self._lines:
            return
        line = self._lines.pop(name)
        line.remove()
        self.ax.legend(loc='center left', fontsize = 10, bbox_to_anchor=(1.005, 0.5))
        self.canvas.draw()

        self.autoscale_triggered()

    def autoscale_triggered(self, padding_ratio: float = 0.05):
        """
        Auto-rescale x-axis to fit only the currently plotted lines.

        Parameters
        ----------
        padding_ratio : float
            Extra margin added to min/max values (default 5%).
        """
        if not self._lines:
            # No lines → reset to default autoscale
            self.ax.relim()
            self.ax.autoscale()
            self.canvas.draw()
            return

        y_min, y_max = float("inf"), float("-inf")

        for line in self._lines.values():
            ydata = line.get_ydata(orig=False)

            if len(ydata) == 0:
                continue

            y_min = min(y_min, ydata.min())
            y_max = max(y_max, ydata.max())

        # Avoid zero-range axes
        if y_min == y_max:
            y_min -= 1
            y_max += 1

        # Add padding
        y_pad = (y_max - y_min) * padding_ratio

        self.ax.set_ylim(y_min - y_pad, y_max + y_pad)

        self.canvas.draw_idle()
