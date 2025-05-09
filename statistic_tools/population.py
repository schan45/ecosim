import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib.ticker import MaxNLocator
from IPython.display import Image, display


def export_population_chart(population_history, output_dir="statistics_plots"):
    """
    This function is designed to visualize how the population size of each species changed over time during the simulation. Each species is associated with a list that tracks the number of living individuals at every simulation step. Using this data, the function generates a line chart: each species is represented by a distinct colored line showing how its population increased, decreased, or remained stable over time.
    The parameter population_history is a dictionary where the keys are species names (e.g., "Fox", "Rabbit"), and the values are lists of integers representing the population size at each step.
    The output_dir parameter specifies the folder where the generated chart (typically in PNG format) should be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(6, 6))
    
    for species, counts in population_history.items():
        x = np.arange(len(counts))
        if len(x) >= 4:  
            spline = make_interp_spline(x, counts, k=3)  # cubic spline
            x_smooth = np.linspace(x.min(), x.max(), 300)
            y_smooth = spline(x_smooth)
            plt.plot(x_smooth, y_smooth, label=species, linewidth=2)
        else:
            plt.plot(x, counts, label=species, linewidth=2)
   

    plt.title("Population")
    plt.xlabel("Time")
    plt.ylabel("Species number")
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "population_chart.png"))
    plt.close()

def display_population_chart(path: str = "statistics_plots/population_chart.png") -> None:
    """
    This function is intended to display the population chart image (population_chart.png) that was saved after the simulation — if the file actually exists in the specified folder (typically statistics_plots/). The chart visually represents how the population of each species changed over time during the simulation — showing the number of living individuals per species at each simulation step.
    The program first checks whether the file is present in the folder. If it exists, the image is loaded and displayed on screen, allowing the user to review the results without rerunning the simulation. If the file doesn't exist, the program may display a warning or error message.
    """
    if os.path.exists(path):
        display(Image(filename=path))
    else:
        print(f"⚠️ Population chart not found at {path}")
