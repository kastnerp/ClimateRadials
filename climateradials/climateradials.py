import math
import os
from pathlib import Path

import matplotlib.cm as cm
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import requests
import streamlit as st
from epw import epw
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from tqdm import tqdm


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
    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
        'Nov', 'Dec', 'Dec'
    ]
    months.reverse()
    ax.set_xticklabels(months, minor=True)
    ax.set_rlabel_position(0)

    # ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
    # ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.set_theta_zero_location("N")
    ax.grid(True)
    ax.grid(color='lightgrey', linestyle='-', linewidth=0.4, zorder=0)
    return ax


def getColorMap(fig, ax, x, y, boundary_norm=None, cmap=None):
    # ValueError: Colormap tarn is not recognized. Possible values are: Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cmo.algae, cmo.algae_r, cmo.amp, cmo.amp_r, cmo.balance, cmo.balance_r, cmo.curl, cmo.curl_r, cmo.deep, cmo.deep_r, cmo.delta, cmo.delta_r, cmo.dense, cmo.dense_r, cmo.diff, cmo.diff_r, cmo.gray, cmo.gray_r, cmo.haline, cmo.haline_r, cmo.ice, cmo.ice_r, cmo.matter, cmo.matter_r, cmo.oxy, cmo.oxy_r, cmo.phase, cmo.phase_r, cmo.rain, cmo.rain_r, cmo.solar, cmo.solar_r, cmo.speed, cmo.speed_r, cmo.tarn, cmo.tarn_r, cmo.tempo, cmo.tempo_r, cmo.thermal, cmo.thermal_r, cmo.topo, cmo.topo_r, cmo.turbid, cmo.turbid_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, icefire, icefire_r, inferno, inferno_r, jet, jet_r, magma, magma_r, mako, mako_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, rocket, rocket_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, vlag, vlag_r, winter, winter_r
    # Create a continuous norm to map from data points to colors

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    if cmap is None:
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


class Radial:
    """A class to create a climate radial from an epw input file
    """

    fig, ax = None, None

    def __init__(self, epw_path):

        self.epwPath = epw_path
        self.read_from_url = False
        self.file_path_local = ''
        self.data, self.location = self.read_epw()

    def read_epw(self):
        """returns dataframe"""

        if str.startswith(self.epwPath, 'http') and not Path(self.epwPath.split('/')[-1]).is_file():
            self.read_from_url = True
            self.file_path_local = Path(Path.cwd() / Path(self.epwPath.split('/')[-1]))

            response = requests.get(self.epwPath, stream=True)

            print("Downloading file...")
            with open(self.file_path_local, "wb") as handle:
                for data in tqdm(response.iter_content()):
                    handle.write(data)

        elif Path(Path.cwd() / Path(self.epwPath.split('/')[-1])).is_file():
            self.file_path_local = Path(Path.cwd() / Path(self.epwPath.split('/')[-1]))

        else:
            self.file_path_local = self.epwPath
        epwO = epw()
        print("Reading file...")
        epwO.read(self.file_path_local)

        return epwO.dataframe, epwO.headers['LOCATION'][0]

    def delete_epw(self):
        os.remove(self.file_path_local)



    def createFig(self):

        size = 10
        self.fig, self.ax = plt.subplots(nrows=1, ncols=1, figsize=(size, size))
        self.ax = plt.subplot(111, projection='polar')

    def show_result(self, dpi=600, fileName=None, export=False):
        if fileName is None:
            fileName = self.location
        if export is True:
            print("Exporting to file...")
            self.fig.savefig(fileName + '.pdf', bbox_inches='tight', pad_inches=0.0)
            self.fig.savefig(fileName + '.png', bbox_inches='tight',
                             pad_inches=0.0, dpi=dpi)
        else:
            print("Showing plot...")
            plt.show()
        print("Done.")

    def scale_inputs(self, y, ymin, ymax, yorigin):
        self.ax = scaleInputs(y, ymin, ymax, yorigin, self.ax)
        self.ax = setTickLocations(self.ax)

    def set_title(self):
        self.ax.set_title(self.location, va='bottom', y=0.47)

    def plot_bar_generic(self, dpi=600, x=None, y=None, ymin=None, ymax=None, yorigin=None, cmap=None,
                         fileName=None):
        print("Plotting bar chart...")
        if (x is None and y is None):
            y = self.data['Dry Bulb Temperature'][::-1]
            x = np.linspace(0, 2 * np.pi, 8760)

        # Idea: Subdivide all points to incremental bars that have their own color
        X, Y = constructXY(y)

        days = X
        radii = np.ones(len(Y)) * 1.0
        # reverse
        radii_rev = radii[::-1]
        bottom = Y
        width = 0.01

        self.createFig()

        cmap = 'jet'

        # Rescale the color map

        # https://matplotlib.org/3.1.0/tutorials/colors/colormap-manipulation.html
        norm = col.Normalize(vmin=min(y), vmax=max(y))

        # First we should filter input_array so that it does not contain NaN or Inf.
        input_array = np.array(Y)
        result_array = np.array([])
        if np.unique(input_array).shape[0] == 1:
            pass  # do thing if the input_array is constant
        else:
            result_array = (input_array - np.min(input_array)) / \
                           np.ptp(input_array)
        # To extend it to higher dimension, add axis= kwarvg to np.min and np.ptp

        colors = plt.cm.get_cmap(cmap, (max(Y) - min(Y)))
        color_vals = colors(result_array)
        # print("colors: ",colors.shape)

        # create a scalarmappable from the colormap
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array(np.array([]))

        cbar = self.fig.colorbar(sm)
        cbar.ax.set_ylabel('Dry Bulb Temperature $[°C]$')

        self.ax.bar(days, radii_rev, width=width,
                    bottom=bottom, color=color_vals, zorder=0)

        self.scale_inputs(y, ymin, ymax, yorigin)
        self.set_title()

        # fig, ax = self.getColorMap(fig,ax, x,y, cmap)

    def plot_bars(self, dpi=600, x=None, y=None, ymin=None, ymax=None, yorigin=None, cmap=None,
                  fileName=None, export=False):
        self.plot_bar_generic(x, y, ymin, ymax, yorigin)
        self.show_result(dpi, fileName, export)

    def plot_bars_st(self, x=None, y=None, ymin=None, ymax=None, yorigin=None):
        self.plot_bar_generic(x, y, ymin, ymax, yorigin)
        st.pyplot(self.fig)

    def plot_line_generic(self, dpi=600, x=None, y=None, ymin=None, ymax=None, yorigin=None, cmap=None,
                          fileName=None, export=False):
        print("Plotting line chart...")
        if (x is None and y is None):
            y = self.data['Dry Bulb Temperature'][::-1]
            x = np.linspace(0, 2 * np.pi, 8760)

        self.createFig()

        # rain
        # ax.scatter(x, y, s= precipitation*10, alpha=0.2, linewidth=0, zorder=5)

        self.scale_inputs(y, ymin, ymax, yorigin)

        self.fig, self.ax = getColorMap(self.fig, self.ax, x, y, cmap)

        self.set_title()

    def plot_lines(self, dpi=600, x=None, y=None, ymin=None, ymax=None, yorigin=None, cmap=None,
                   fileName=None, export=False):
        self.plot_line_generic(dpi, x, y, ymin, ymax, yorigin, cmap,
                               fileName, export)
        self.show_result(dpi, fileName, export)

    def plot_line_st(self, dpi=600, x=None, y=None, ymin=None, ymax=None, yorigin=None, cmap=None,
                     fileName=None, export=False):
        self.plot_line_generic(dpi, x, y, ymin, ymax, yorigin, cmap,
                               fileName, export)
        st.pyplot(self.fig)
