import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib.ticker import MaxNLocator
from IPython.display import Image, display


def export_population_chart(population_history, output_dir="statistics_plots"):
    """
    Kirajzolja fajonként az egyedszám időbeli alakulását.
    :param population_history: dict[str, list[int]] — fajonként az időbeli populációméret
    :param output_dir: hová mentse a képet
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(6, 6))
    
    for species, counts in population_history.items():
        x = np.arange(len(counts))
        if len(x) >= 4:  # spline legalább 4 pontból működik jól
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
    Megjeleníti a korábban mentett population_chart.png képet, ha létezik.
    """
    if os.path.exists(path):
        display(Image(filename=path))
    else:
        print(f"⚠️ Population chart not found at {path}")