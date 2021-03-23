import math
import os
from pathlib import Path

import matplotlib
import matplotlib.cm as cm
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from tqdm import tqdm

from enum import Enum


def getminmax(input_array):
    minn, maxx = np.zeros(365), np.zeros(365)
    for i in range(365):
        day = input_array[i * 24:(i + 1) * 24]
        minn[i] = (min(day))
        maxx[i] = (max(day))

    return minn, maxx


def getdailyarrayY(minn, maxx):
    # problem when amplitude is too small
    if (abs(maxx - minn)) > 2:
        arr = np.linspace(minn, maxx, (math.ceil(abs(maxx - minn)) + 1))
    else:
        arr = np.linspace(minn, maxx, (math.ceil(abs(maxx - minn)) + 2))
    return arr.tolist()


def scaleInputs(y, ymin, ymax, yorigin, ax):
    if yorigin is None:
        ax.set_rorigin(-70)
    else:
        ax.set_rorigin(yorigin)
    if ymax is None:
        ax.set_rmax(max(y) + 5)
    else:
        ax.set_rmax(ymax)

    if ymin is None:
        ax.set_rmin(min(y) - 5)
    else:
        ax.set_rmin(ymin)
    return ax


def setTickLocations(ax):
    # ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
    # ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line

    # Set the major and minor tick locations
    ax.xaxis.set_major_locator(ticker.MultipleLocator(np.pi / 6))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(np.pi / 12))

    # Turn off major tick labels
    ax.xaxis.set_major_formatter(ticker.NullFormatter())

    # Set the minor tick width to 0 so you don't see them
    for tick in ax.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center')

    # Set the names of your ticks
    months = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11:
            'Nov', 12: 'Dec', 13: 'Dec'
    }

    # ax.set_xticks(list(reversed(list(months.keys()))))
    ax.set_xticklabels(list(reversed(list(months.values()))), minor=True)
    ax.set_rlabel_position(0)

    # ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
    # ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.set_theta_zero_location("N")

    ax.grid(color='lightgrey', linestyle='-', linewidth=0.4, zorder=0)
    ax.grid(True)
    return ax


def getColorMap(fig, ax, x, y, boundary_norm=None):
    # ValueError: Colormap tarn is not recognized. Possible values are: Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cmo.algae, cmo.algae_r, cmo.amp, cmo.amp_r, cmo.balance, cmo.balance_r, cmo.curl, cmo.curl_r, cmo.deep, cmo.deep_r, cmo.delta, cmo.delta_r, cmo.dense, cmo.dense_r, cmo.diff, cmo.diff_r, cmo.gray, cmo.gray_r, cmo.haline, cmo.haline_r, cmo.ice, cmo.ice_r, cmo.matter, cmo.matter_r, cmo.oxy, cmo.oxy_r, cmo.phase, cmo.phase_r, cmo.rain, cmo.rain_r, cmo.solar, cmo.solar_r, cmo.speed, cmo.speed_r, cmo.tarn, cmo.tarn_r, cmo.tempo, cmo.tempo_r, cmo.thermal, cmo.thermal_r, cmo.topo, cmo.topo_r, cmo.turbid, cmo.turbid_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, icefire, icefire_r, inferno, inferno_r, jet, jet_r, magma, magma_r, mako, mako_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, rocket, rocket_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, vlag, vlag_r, winter, winter_r
    # Create a continuous norm to map from data points to colors

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    cmap = 'jet'

    if boundary_norm is None:

        # Create a set of line segments so that we can color them individually
        # This creates the points as a N x 1 x 2 array so that we can stack points
        # together easily to get the segments. The segments array for line collection
        # needs to be (numlines) x (points per line) x 2 (for x and y)

        norm = plt.Normalize(y.min(), y.max())
        lc = LineCollection(segments, cmap='jet', norm=norm)
        # Set the values used for colormapping
        lc.set_array(y)
        lc.set_linewidth(1.5)
        line = ax.add_collection(lc)
        cbar = fig.colorbar(line, ax=ax)
        cbar.ax.set_ylabel('Dry Bulb Temperature $[°C]$')
        return fig, ax
    else:
        # Use a boundary norm instead
        # [-40, -27, -13, 0, 9, 26, 28, 32, 38, 46]
        cmap = ListedColormap(['#7F00FF', '#8a2be2', '#0000FF', '#00FFFF',
                               '#2ade2a', '#008000', '#FFFF00', '#FF8C00', '#FF0000'])
        norm = BoundaryNorm(boundary_norm, cmap.N)
        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(y)
        lc.set_linewidth(1.5)
        line = ax.add_collection(lc)
        cbar = fig.colorbar(line, ax=ax)
        ax.set_ylabel('Dry Bulb Temperature $[°C]$')
        return fig, ax


def constructXY(arr):
    minn, maxx = getminmax(arr)

    X, Y = [], []

    for d in range(365):
        dailyarrY = getdailyarrayY(minn[d], maxx[d])
        Y.append(dailyarrY)
        temp = [d] * len(dailyarrY)
        X.append(temp)

    flat_listY = [item for sublist in Y for item in sublist]
    flat_listX = [item for sublist in X for item in sublist]

    scale = 0.01721420632103996  # math.pi/365*2

    return np.array(flat_listX) * scale, np.array(flat_listY)
