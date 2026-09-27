"""
Shared matplotlib styling for all notebooks in this project.
Colors come from a validated categorical palette (CVD-safe, fixed hue order) -
see the design system reference this was drawn from for the validation details.
"""

import matplotlib as mpl

# Categorical palette, fixed order - never reassign/cycle these per chart.
CATEGORICAL = [
    '#2a78d6',  # 1 blue
    '#eb6834',  # 2 orange
    '#1baf7a',  # 3 aqua
    '#eda100',  # 4 yellow
    '#e87ba4',  # 5 magenta
    '#008300',  # 6 green
    '#4a3aa7',  # 7 violet
    '#e34948',  # 8 red
]
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = CATEGORICAL

# Chart chrome
SURFACE = '#fcfcfb'
INK_PRIMARY = '#0b0b0b'
INK_SECONDARY = '#52514e'
INK_MUTED = '#898781'
GRIDLINE = '#e1e0d9'
BASELINE = '#c3c2b7'

# Region is used as a color-coded entity across multiple charts (bar + two line
# charts) - keep the same color for the same region everywhere it appears.
REGION_COLORS = {
    'Central': CATEGORICAL[0],
    'East': CATEGORICAL[1],
    'South': CATEGORICAL[2],
    'West': CATEGORICAL[3],
}


def apply_style():
    """Call once per notebook, after importing matplotlib.pyplot."""
    mpl.rcParams.update({
        'figure.facecolor': SURFACE,
        'axes.facecolor': SURFACE,
        'savefig.facecolor': SURFACE,
        'axes.edgecolor': BASELINE,
        'axes.labelcolor': INK_SECONDARY,
        'text.color': INK_PRIMARY,
        'xtick.color': INK_MUTED,
        'ytick.color': INK_MUTED,
        'axes.titlecolor': INK_PRIMARY,
        'axes.titleweight': 'bold',
        'axes.titlesize': 13,
        'axes.labelsize': 11,
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.grid': True,
        'axes.axisbelow': True,
        'grid.color': GRIDLINE,
        'grid.linewidth': 0.8,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'legend.frameon': False,
        'figure.dpi': 100,
    })
