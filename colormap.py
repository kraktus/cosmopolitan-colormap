#!/usr/local/bin/python3
# coding: utf-8
# Licence: GNU AGPLv3

"""A simple colormap for matplotlib that renders well on both black and white backgrounds"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
from PIL import Image
from typing import Optional, List, Union, Tuple

#############
# Constants #
#############

#############
# Functions #
#############


def cutstom1_cmap():
    colors = [
        mpl.colors.to_rgba(x)
        for x in [
            "#1c90d4",
            "#ad0026",
            "#530fff",
            "#429900",
            "#d55e00",
            "#ff47ac",
            "#42baff",
            "#009e73",
            "#fff133",
            "#0072b2",
        ]
    ]
    return mpl.colors.ListedColormap(colors)


# based on https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
def plot_colored_lines(ax, cmap):
    """Plot lines with colors following the style color cycle."""
    ax.set_prop_cycle(color=cmap.colors)
    t = np.linspace(-10, 10, 100)

    def sigmoid(t, t0):
        return 1 / (1 + np.exp(-(t - t0)))

    nb_colors = len(cmap.colors)
    shifts = np.linspace(-5, 5, nb_colors)
    amplitudes = np.linspace(1, 1.5, nb_colors)
    for t0, a in zip(shifts, amplitudes):
        ax.plot(t, a * sigmoid(t, t0), "-")
    ax.set_xlim(-10, 10)
    return ax


# based on https://matplotlib.org/stable/tutorials/colors/colormaps.html
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))


def plot_color_gradients(name, cmap, ax):
    ax.imshow(gradient, aspect="auto", cmap=cmap)
    # ax.text(-0.01, 0.5, name, va='center', ha='right', fontsize=10,
    #         transform=ax.transAxes)
    ax.set_ylabel(name, fontsize=10, rotation=0, va="center", ha="right")


def plot(style: str, cmap, name) -> None:
    figh = 0.962
    with plt.style.context(style):
        fig, axs = plt.subplots(nrows=2, gridspec_kw={"height_ratios": [10, 1]})
    plot_colored_lines(axs[0], cmap)
    plot_color_gradients(name, cmap, axs[1])
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])


def combine(name: str) -> None:
    images = [Image.open(x) for x in ["white.png", "black.png"]]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new("RGB", (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save(f"{name}.png")


def try_cmap(cmap, name: str) -> None:
    plot("default", cmap, name)
    plt.savefig("white.png")
    plot("dark_background", cmap, name)
    plt.savefig("black.png")
    combine(name)


def native() -> None:
    colors = [mpl.colors.to_rgba(x["color"]) for x in plt.rcParams["axes.prop_cycle"]]
    cmap = mpl.colors.ListedColormap(colors)
    try_cmap(cmap, "native")


def cutstom1() -> None:
    try_cmap(cutstom1_cmap(), "custom1")


########
# Main #
########

if __name__ == "__main__":
    print("#" * 80)
    cutstom1()
