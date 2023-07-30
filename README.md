# Cosmopolitan colormap

Experiments on matplotlib to find colormaps that render well dark and light backgrounds.

## Results

The different colormaps can be copied from the colormap section of `colormap.py`. Overall, the `light_native_cmap` seem the most pleasant even though it's not the most contrasted palette.

## Comparisons

We will be comparing the colormaps against the native/default color palette of matplotlib for light and dark backgrounds.

![a plot of colored lines above a plot of color gradient above the word "text" repeated in each color of the colormap against a light and dark backgrounds](/native.png)

A first idea is to check how well the native light colormap performs on a dark background and vice-versa. Note that the following images also include a version of the plot on a transparent background, for easy testing against other colored backgrounds.

![a plot of colored lines above a plot of color gradient above the word "text" repeated in each color of the colormap against a light and dark backgrounds](/light_native.png)

![a plot of colored lines above a plot of color gradient above the word "text" repeated in each color of the colormap against a light and dark backgrounds](/dark_native.png)

Clearly the light version performs much better on the dark background than the opposite.

Now two custom colomaps intented to have a better contrast, first one being done by hand, the second one pick colors from this [article](https://dev.to/finnhvman/which-colors-look-good-on-black-and-white-2pe6).

![a plot of colored lines above a plot of color gradient above the word "text" repeated in each color of the colormap against a light and dark backgrounds](/custom1.png)

![a plot of colored lines above a plot of color gradient above the word "text" repeated in each color of the colormap against a light and dark backgrounds](/custom2.png)


## Limitations, future work

While contrast to the background is better on custom colormaps, the result is less aesthetic, and the different colors have less constrast between them.

## Name

It's a reference to the [Cosmopolitan libc](https://justine.lol/cosmopolitan/index.html) project, a build-once run-anywhere c library.
