import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from collections import defaultdict
import os

def plot_organisms(step, organisms, grid_size=20, output_dir="frames", foodweb=None, terrain=None):
    """Kirajzolja az adott lépés állapotát, a tereptípusokkal együtt"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    scale = 0.3  # 1 rácsmezőhöz ennyi inch jusson
    figsize = (grid_size * scale, grid_size * scale)
    plt.figure(figsize=figsize)
    ax = plt.gca()
    ax.set_facecolor("#ccffcc")         # háttér halványzöld
    ax.grid(True, color="#ccffcc")      # rácsvonalak halványzöld
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_xticks(range(0, grid_size + 1))
    ax.set_yticks(range(0, grid_size + 1))
    ax.grid(True)

    # Háttérszínek terrain típusokhoz
    terrain_colors = {
        "tree": "#2e8b57",     # sötétzöld
        "water": "#add8e6",    # világoskék
        "hill": "#deb887",     # barnás
        "shelter": "#d3d3d3",  # világosszürke
        "plain": "#ccffcc"     # fehérvilágoszöld (alap)
    }

    # Terep kirajzolása háttérként
    if terrain:
        for x in range(grid_size):
            for y in range(grid_size):
                ttype = terrain.get_type(x, y)
                rect = plt.Rectangle((x, y), 1, 1, color=terrain_colors.get(ttype, "#ffffff"), zorder=0)
                ax.add_patch(rect)

    # Színek fajonként
    color_map = get_species_colors(organisms, foodweb=foodweb)
    position_counts = defaultdict(int)

    # Élőlények kirajzolása
    for org in organisms:
        pos = (org.x, org.y)
        i = position_counts[pos]
        position_counts[pos] += 1

        offset = 0.1 * i
        if not org.alive:
            marker = "x"
            color = "gray"
        else:
            marker = "o"
            color = color_map.get(org.species, "black")
            ax.plot(org.x + 0.5 + offset, org.y + 0.5 + offset, marker, color=color, markersize=10, zorder=1)

    plt.title(f"Step {step}")
    plt.savefig(f"{output_dir}/step_{step:03d}.png")
    plt.close()

def get_species_colors(organisms, foodweb=None):
    if foodweb:
        return {org.species: foodweb.get_color(org.species) for org in organisms}
    else:
        species = list({org.species for org in organisms})
        cmap = cm.get_cmap('tab10', len(species))
        return {sp: mcolors.to_hex(cmap(i)) for i, sp in enumerate(species)}
    

