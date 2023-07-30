#!/usr/local/bin/python3
# coding: utf-8
# Licence: GNU AGPLv3

"""Experiments on matplotlib to find colormaps that render well on dark and light backgrounds"""

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

DPI = 100 if __debug__ else 400
FORMAT = "png"

#############
# Colormaps #
#############


def light_native_cmap():
    colors = [
        mpl.colors.to_rgba(x)
        for x in [  # [x["color"] for x in plt.rcParams["axes.prop_cycle"]] with default theme
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ]
    ]
    return mpl.colors.ListedColormap(colors)


def dark_native_cmap():
    colors = [
        mpl.colors.to_rgba(x)
        for x in [  # [x["color"] for x in plt.rcParams["axes.prop_cycle"]] with dark_background theme
            "#8dd3c7",
            "#feffb3",
            "#bfbbd9",
            "#fa8174",
            "#81b1d2",
            "#fdb462",
            "#b3de69",
            "#bc82bd",
            "#ccebc4",
            "#ffed6f",
        ]
    ]
    return mpl.colors.ListedColormap(colors)


# Thanks to @mayushii.
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


#############
# Functions #
#############


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
    ax.set_ylabel(
        name,
        fontsize=10,
        rotation=0,
        va="center",
        ha="right",
        weight="bold",
        color=mpl.colors.to_rgba("#FF5B00")
    )


def plot_colored_text(cmap, ax):
    ax.axis([0, len(cmap.colors) * 4, 0, 1])
    for i, color in enumerate(cmap.colors):
        ax.text(i * 4 + 1, 0, "text", color=color)


def plot(style: str, cmap, name) -> None:
    figh = 0.962
    with plt.style.context(style):
        fig, axs = plt.subplots(nrows=3, gridspec_kw={"height_ratios": [11, 1, 1]})
    plot_colored_lines(axs[0], cmap)
    plot_color_gradients(name, cmap, axs[1])
    plot_colored_text(cmap, axs[2])
    for ax in axs:
        ax.spines[:].set_color(None)
        ax.set_xticks([])
        ax.set_yticks([])


def combine(name: str, include_transparent=True) -> None:
    name = name.replace("\n", "_")
    print("save as ", name.replace("\n", "_"))
    files_list = [f"white.{FORMAT}", f"black.{FORMAT}"]
    if include_transparent:
        files_list.append(f"transparent.{FORMAT}")
    images = [Image.open(x) for x in files_list]
    print([i.size for i in images])
    widths, heights = zip(*(i.size for i in images))
    print("widths, heights", widths, heights)
    total_width = sum(widths)
    max_height = max(heights)
    print("total_width max_height",total_width, max_height)
    new_im = Image.new("RGBA", (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save(f"{name}.{FORMAT}")


def try_cmap(cmap, name: str) -> None:
    plot("default", cmap, name)
    plt.savefig(f"white.{FORMAT}", dpi=DPI)
    plt.savefig(f"transparent.{FORMAT}", transparent=True, dpi=DPI)
    plot("dark_background", cmap, name)
    plt.savefig(f"black.{FORMAT}", dpi=DPI)
    combine(name)


def light_native() -> None:
    cmap = light_native_cmap()
    try_cmap(cmap, "light\nnative")


def adaptative_native() -> None:
    colors = [mpl.colors.to_rgba(x["color"]) for x in plt.rcParams["axes.prop_cycle"]]
    cmap = mpl.colors.ListedColormap(colors)
    name = "native"
    plot("default", cmap, name)
    plt.savefig(f"white.{FORMAT}", dpi=DPI)
    with plt.style.context("dark_background"):
        colors = [
            mpl.colors.to_rgba(x["color"]) for x in plt.rcParams["axes.prop_cycle"]
        ]
    cmap = mpl.colors.ListedColormap(colors)
    plot("dark_background", cmap, name)
    plt.savefig(f"black.{FORMAT}", dpi=DPI)
    combine(name, include_transparent=False)


def dark_native() -> None:
    cmap = dark_native_cmap()
    try_cmap(cmap, "dark\nnative")


def cutstom1() -> None:
    try_cmap(cutstom1_cmap(), "custom1")


def cutstom2() -> None:
    try_cmap(cutstom2_cmap(), "custom2")


########
# Main #
########

if __name__ == "__main__":
    print("#" * 80)
    adaptative_native()
    light_native()
    dark_native()
    cutstom1()
    cutstom2()
