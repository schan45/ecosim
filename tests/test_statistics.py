import pytest
import os
import numpy as np
from statistic_tools.population import export_population_chart, display_population_chart
from statistic_tools.heatmap import export_heatmaps, display_heatmap


def test_export_population_chart(tmp_path):
    output_dir = tmp_path / "statistics_plots"
    data = {
        "rabbit": [5, 10, 15, 12],
        "fox": [2, 3, 1, 0]
    }
    export_population_chart(data, output_dir=output_dir)
    assert (output_dir / "population_chart.png").exists()


def test_export_heatmaps(tmp_path):
    output_dir = tmp_path / "statistics_plots"
    heatmaps = {
        "rabbit": np.random.rand(50, 50),
        "fox": np.random.rand(50, 50)
    }
    export_heatmaps(heatmaps, output_dir=output_dir)
    assert (output_dir / "heatmap_rabbit.png").exists()
    assert (output_dir / "heatmap_fox.png").exists()


def test_display_population_chart_does_not_crash(tmp_path):
    output_dir = tmp_path / "statistics_plots"
    output_dir.mkdir()
    dummy_path = output_dir / "population_chart.png"
    dummy_path.write_bytes(b"fake image")
    try:
        display_population_chart(str(dummy_path))
    except Exception:
        pytest.fail("display_population_chart crashed unexpectedly")


def test_display_heatmap_does_not_crash(tmp_path):
    output_dir = tmp_path / "statistics_plots"
    output_dir.mkdir()
    dummy_path = output_dir / "heatmap_rabbit.png"
    dummy_path.write_bytes(b"fake image")
    try:
        display_heatmap("rabbit", path=str(output_dir))
    except Exception:
        pytest.fail("display_heatmap crashed unexpectedly")
