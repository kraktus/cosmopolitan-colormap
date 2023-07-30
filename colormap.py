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

# Based on https://dev.to/finnhvman/which-colors-look-good-on-black-and-white-2pe6
def cutstom2_cmap():
    colors = [
        mpl.colors.to_rgba(x)
        for x in [
            "#3377cc",
            "#dd3311",
            "#008800",
            "#ee0000",
            "#8855ee",
            "#aa6600",
            "#dd1188",
            "#667788",
            "#777755",
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
    ax.set_ylabel(name, fontsize=10, rotation=0, va="center", ha="right", color=mpl.colors.to_rgba("#FF5B00"),weight="bold")


def plot(style: str, cmap, name) -> None:
    figh = 0.962
    with plt.style.context(style):
        fig, axs = plt.subplots(nrows=2, gridspec_kw={"height_ratios": [10, 1]})
    plot_colored_lines(axs[0], cmap)
    plot_color_gradients(name, cmap, axs[1])
    for ax in axs:
        ax.spines[:].set_color(None)
        ax.set_xticks([])
        ax.set_yticks([])


def combine(name: str, include_transparent = True) -> None:
    name = name.replace('\n', '_')
    print("save as ", name.replace('\n', '_'))
    files_list = ["white.png", "black.png"]
    if include_transparent:
        files_list.append("transparent.png")
    images = [Image.open(x) for x in files_list]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new("RGBA", (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save(f"{name}.png")


def try_cmap(cmap, name: str) -> None:
    plot("default", cmap, name)
    plt.savefig("white.png")
    plt.savefig("transparent.png",transparent=True)
    plot("dark_background", cmap, name)
    plt.savefig("black.png")
    combine(name)


def light_native() -> None:
    colors = [mpl.colors.to_rgba(x["color"]) for x in plt.rcParams["axes.prop_cycle"]]
    cmap = mpl.colors.ListedColormap(colors)
    try_cmap(cmap, "light\nnative")

def adaptative_native() -> None:
    colors = [mpl.colors.to_rgba(x["color"]) for x in plt.rcParams["axes.prop_cycle"]]
    cmap = mpl.colors.ListedColormap(colors)
    name = "adaptative\nnative"
    plot("default", cmap, name)
    plt.savefig("white.png")
    with plt.style.context("dark_background"):
        colors = [mpl.colors.to_rgba(x["color"]) for x in plt.rcParams["axes.prop_cycle"]]
    cmap = mpl.colors.ListedColormap(colors)
    plot("dark_background", cmap, name)
    plt.savefig("black.png")
    combine(name,include_transparent=False)


def dark_native() -> None:
    with plt.style.context("dark_background"):
        colors = [mpl.colors.to_rgba(x["color"]) for x in plt.rcParams["axes.prop_cycle"]]
    cmap = mpl.colors.ListedColormap(colors)
    try_cmap(cmap, "dark\nnative")


def cutstom1() -> None:
    try_cmap(cutstom1_cmap(), "custom1")

def cutstom2() -> None:
    try_cmap(cutstom2_cmap(), "custom2")

def plt_test():
    fig, ax = plt.subplots()
    fig.set_edgecolor(mpl.colors.to_rgba("#FF6600"))
    plt.show()

########
# Main #
########

if __name__ == "__main__":
    print("#" * 80)
    light_native()
