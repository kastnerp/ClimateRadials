import os
import math

from epw import epw

import seaborn as sns
import cmocean

from scipy.stats import gamma

from pathlib import Path, PureWindowsPath

from windrose import WindroseAxes
from windrose import WindAxes

import numpy as np

import matplotlib.cm as cm
import matplotlib.ticker as ticker
import matplotlib.colors as col
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm




class radial():
    """A class to create a climate radial from an epw input file
    """

    def __init__(self, epwPath):
        epwO = epw()
        epwO.read(epwPath)

        data = epwO.dataframe

        self.data = data
        self.location = epwO.headers['LOCATION'][0]
        self.epwPath = epwPath

    def wind(self, data):
        self.windvel = data['Wind Speed']
        self.winddir = data['Wind Direction']

    def plot_windrose(self):
        self.wind(self.data)

        ax = WindroseAxes.from_ax()
        ax.contourf(self.winddir, self.windvel, bins=np.arange(
            0, 6, 1), nsector=36, cmap=cm.get_cmap(name="hot"))
        ax.contour(self.winddir, self.windvel, bins=np.arange(
            0, 6, 1), nsector=36, colors='black', lw=1)
        ax.set_legend()

    def print_wind_PDF(self):
        self.wind(self.data)

        ax = WindAxes.from_ax()
        bins = np.arange(0, 6 + 1, 0.5)
        bins = bins[1:]
        ax = ax.pdf(self.windvel, bins=bins)

    def getminmax(self, arr):

        minn = []
        maxx = []
        for i in range(365):
            day = arr[(i)*24:(i+1)*24]
            mind = min(day)
            maxd = max(day)
            minn.append(mind)
            maxx.append(maxd)

        return minn, maxx

    def getdailyarrayY(self, minn, maxx):
        # problem when amplitude is too small
        if (np.abs(maxx-minn)) > 2:
            arr = np.linspace(minn, maxx, (math.ceil(np.abs(maxx - minn)) + 1))
            return arr.tolist()
        else:
            arr = np.linspace(minn, maxx, (math.ceil(np.abs(maxx - minn)) + 2))
            return arr.tolist()

    def constructXY(self, arr):

        minn, maxx = self.getminmax(arr)

        X, Y = [], []

        for d in range(365):

            dailyarrY = self.getdailyarrayY(minn[d], maxx[d])
            Y.append(dailyarrY)
            temp = [d] * len(dailyarrY)
            X.append(temp)

        flat_listY = [item for sublist in Y for item in sublist]
        flat_listX = [item for sublist in X for item in sublist]

        return np.array(flat_listX) * 0.01726149, np.array(flat_listY)

    def scaleInputs(self, y, ymin, ymax, yorigin, ax):
        if(yorigin is None):
            ax.set_rorigin(-70)
        else:
            ax.set_rorigin(yorigin)
        if ymax is None:
            ax.set_rmax(max(y)+5)
        else:
            ax.set_rmax(ymax)

        if ymin is None:
            ax.set_rmin(min(y)-5)
        else:
            ax.set_rmin(ymin)
        return ax

    def setTickLocations(self, ax):
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
        return ax

    def createFig(self, size=10):

        if size is None:
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
            ax = plt.subplot(111, projection='polar')
            return fig, ax
        else:
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(size, size))
            ax = plt.subplot(111, projection='polar')
            return fig, ax

    def getColorMap(self, fig, ax, x, y, boundaryNorm=None, cmap=None):
        # ValueError: Colormap tarn is not recognized. Possible values are: Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cmo.algae, cmo.algae_r, cmo.amp, cmo.amp_r, cmo.balance, cmo.balance_r, cmo.curl, cmo.curl_r, cmo.deep, cmo.deep_r, cmo.delta, cmo.delta_r, cmo.dense, cmo.dense_r, cmo.diff, cmo.diff_r, cmo.gray, cmo.gray_r, cmo.haline, cmo.haline_r, cmo.ice, cmo.ice_r, cmo.matter, cmo.matter_r, cmo.oxy, cmo.oxy_r, cmo.phase, cmo.phase_r, cmo.rain, cmo.rain_r, cmo.solar, cmo.solar_r, cmo.speed, cmo.speed_r, cmo.tarn, cmo.tarn_r, cmo.tempo, cmo.tempo_r, cmo.thermal, cmo.thermal_r, cmo.topo, cmo.topo_r, cmo.turbid, cmo.turbid_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, icefire, icefire_r, inferno, inferno_r, jet, jet_r, magma, magma_r, mako, mako_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, rocket, rocket_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, vlag, vlag_r, winter, winter_r
        # Create a continuous norm to map from data points to colors
        if cmap is None:
            cmap = 'jet'

        if boundaryNorm is None:

            # Create a set of line segments so that we can color them individually
            # This creates the points as a N x 1 x 2 array so that we can stack points
            # together easily to get the segments. The segments array for line collection
            # needs to be (numlines) x (points per line) x 2 (for x and y)
            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

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
            #[-40, -27, -13, 0, 9, 26, 28, 32, 38, 46]
            cmap = ListedColormap(['#7F00FF', '#8a2be2', '#0000FF', '#00FFFF',
                                   '#2ade2a', '#008000', '#FFFF00', '#FF8C00', '#FF0000'])
            norm = BoundaryNorm(boundaryNorm, cmap.N)
            lc = LineCollection(segments, cmap=cmap, norm=norm)
            lc.set_array(y)
            lc.set_linewidth(1.5)
            line = ax.add_collection(lc)
            cbar = fig.colorbar(line, ax=ax)
            ax.set_ylabel('Dry Bulb Temperature $[°C]$')
            return fig, ax

    def plot_line(self, size=None, dpi=600, x=None, y=None, ymin=None, ymax=None,  yorigin=None, cmap=None, fileName=None, export=False):

        if(x is None and y is None):
            y = self.data['Dry Bulb Temperature'][::-1]
            x = np.linspace(0, 2 * np.pi, 8760)

        fig, ax = self.createFig(size)

        # rain
        # ax.scatter(x, y, s= precipitation*10, alpha=0.2, linewidth=0, zorder=5)

        ax = self.scaleInputs(y, ymin, ymax, yorigin, ax)
        ax = self.setTickLocations(ax)

        fig, ax = self.getColorMap(fig, ax, x, y, cmap)

        ax.set_title(self.location, va='bottom', y=0.47)
        plt.show()

        if fileName is None:
            fileName = self.location
        if export is True:
            fig.savefig(fileName + '.pdf', bbox_inches='tight', pad_inches=0.0)
            fig.savefig(fileName + '.png', bbox_inches='tight',
                        pad_inches=0.0, dpi=dpi)

    def plot_bars(self, size=None, dpi=600, x=None, y=None, ymin=None, ymax=None,  yorigin=None, cmap=None, fileName=None, export=False):

        if(x is None and y is None):
            y = self.data['Dry Bulb Temperature'][::-1]
            x = np.linspace(0, 2 * np.pi, 8760)

        # Idea: Subdivide all points to incremental bars that have their own color
        X, Y = self.constructXY(y)

        days = X
        radii = np.ones(len(Y))*1.0
        # reverse
        radii_rev = radii[::-1]
        bottom = Y
        width = 0.01

        fig, ax = self.createFig(size)

        cmap = 'jet'

        # Rescale the color map

        # https://matplotlib.org/3.1.0/tutorials/colors/colormap-manipulation.html
        norm = col.Normalize(vmin=min(y), vmax=max(y))

        # First we should filter input_array so that it does not contain NaN or Inf.
        input_array = np.array(Y)
        if np.unique(input_array).shape[0] == 1:
            pass  # do thing if the input_array is constant
        else:
            result_array = (input_array-np.min(input_array)) / \
                np.ptp(input_array)
        # To extend it to higher dimension, add axis= kwarvg to np.min and np.ptp

        colors = plt.cm.get_cmap(cmap, (max(Y)-min(Y)))
        color_vals = colors(result_array)
        #print("colors: ",colors.shape)

        # create a scalarmappable from the colormap
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        cbar = fig.colorbar(sm)
        cbar.ax.set_ylabel('Dry Bulb Temperature $[°C]$')

        ax.bar(days, radii_rev, width=width,
               bottom=bottom, color=color_vals, zorder=2)

        ax = self.scaleInputs(y, ymin, ymax, yorigin, ax)
        ax = self.setTickLocations(ax)

        #fig, ax = self.getColorMap(fig,ax, x,y, cmap)

        ax.set_title(self.location, va='bottom', y=0.47)
        plt.show()

        if fileName is None:
            fileName = self.location
        if export is True:
            fig.savefig(fileName + '.pdf', bbox_inches='tight', pad_inches=0.0)
            fig.savefig(fileName + '.png', bbox_inches='tight',
                        pad_inches=0.0, dpi=dpi)
