import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from collections import defaultdict
import os
import imageio
import numpy as np
from IPython.display import Image

def plot_organisms(step, organisms, grid_size=20, output_dir="frames", foodweb=None, terrain=None):
    """Kirajzolja az adott lépés állapotát, a tereptípusokkal együtt"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    scale = 0.3  # 1 rácsmezőhöz ennyi inch jusson
    figsize = (grid_size * scale, grid_size * scale)
    plt.figure(figsize=figsize)
    ax = plt.gca()
    ax.set_facecolor("#a1cca3")         # halványzöld
    ax.grid(True, color="#a1cca3")      # rácsvonalak halványzöld
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_xticks(range(0, grid_size + 1))
    ax.set_yticks(range(0, grid_size + 1))
    ax.grid(True)

    # Háttérszínek terrain típusokhoz
    terrain_colors = {
        "tree": "#2e8b57",     # sötétzöld
        "water": "#add8e6",    # világoskék
        "hill": "#7d705c",     # barnás
        "shelter": "#d3d3d3",  # világosszürke
        "plain": "#a1cca3"     # halványzöld
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
    

def create_animation(frame_folder: str = "frames", output_path: str = "statistics_plots/animation.gif", fps: int = 4, frame_range: tuple[int, int] = None) -> None:
    """
    Creates an animated GIF from PNG frame images in the given folder.

    Parameters:
        frame_folder: Directory containing .png frames
        output_path: Where to save the animation
        fps: Frames per second
        frame_range: Tuple (start, end) to limit frames, or None for all
    """
    images = []
    frame_files = sorted([f for f in os.listdir(frame_folder) if f.endswith(".png")])

    if frame_range:
        start, end = frame_range
        frame_files = frame_files[start:end]

    for filename in frame_files:
        img_path = os.path.join(frame_folder, filename)
        images.append(imageio.imread(img_path))

    if not images:
        print("No frames found to create animation.")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    imageio.mimsave(output_path, images, fps=fps)
    print(f"✅ Animation saved to {output_path}")
    return Image(output_path)

def compose_frames_side_by_side(frame_indices: list[int], frame_folder: str = "frames", output_path: str = "statistics_plots/frames_side_by_side.png") -> None:
    """
    Composes selected PNG frames side-by-side into a single image.
    
    Parameters:
        frame_indices: List of frame numbers (e.g. [0, 5, 10])
        frame_folder: Directory containing frame PNGs
        output_path: Output PNG file path
    """
    images = []
    for i in frame_indices:
        filename = f"step_{i:03d}.png"
        path = os.path.join(frame_folder, filename)
        if os.path.exists(path):
            images.append(imageio.imread(path))
        else:
            print(f"⚠️ Frame not found: {filename}")

    if not images:
        print("No valid frames to compose.")
        return

    combined_image = np.hstack(images)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    imageio.imwrite(output_path, combined_image)
    print(f"✅ Composed image saved to {output_path}")
    return Image(output_path)


