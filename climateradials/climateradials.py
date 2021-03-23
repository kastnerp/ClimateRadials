from helper_funcs import *
import requests
from epw import epw
import streamlit as st

class PlotType(Enum):
    BarPlot = 0
    LinePlot = 1


class Radial:
    """A class to create a climate radial from an epw input file
    """

    fig, ax = None, None

    def __init__(self, epw_path):

        self.epwPath = epw_path
        self.read_from_url = False
        self.file_path_local = ''
        self.data, self.location = self.read_epw()
        self.plot_settings = self.PlotSettings()

    class PlotSettings:

        def __init__(self, x=None, y=None, ymin=None, ymax=None, yorigin=None, cmap='jet', dpi=100):
            self.x = x
            self.y = y
            self.ymin = ymin
            self.ymax = ymax
            self.yorigin = yorigin
            self.cmap = cmap
            self.dpi = dpi

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

    def export_result(self, plot_type, dpi=72, export=False):

        if export is True:
            fileName = self.location
            fileName = fileName.replace(" ", "_")
            matplotlib.use('Agg')

            #  export_name = fileName + "_" + plot_type + '.pdf'
            #  print("Exporting to", str(export_name) + "...")
            #  self.fig.savefig(export_name, bbox_inches='tight', pad_inches=0.0)
            export_name = fileName + "_" + plot_type + '.png'
            print("Exporting to", str(export_name) + "...")
            self.fig.savefig(export_name, bbox_inches='tight', pad_inches=0.0, dpi=dpi)


        else:
            print("Showing plot...")
            plt.show()
        plt.clf()
        plt.close(self.fig)
        print("Done.")

    def scale_inputs(self, y, ymin, ymax, yorigin):
        self.ax = scaleInputs(y, ymin, ymax, yorigin, self.ax)
        self.ax = setTickLocations(self.ax)

    def set_title(self):
        self.ax.set_title(self.location, va='bottom', y=0.47)

    # @profile
    def plot_bar_generic(self, x=None, y=None, ymin=None, ymax=None, yorigin=None, ):
        print("Plotting bar chart...")
        if (x is None and y is None):
            y = self.data['Dry Bulb Temperature'][::-1]
            x = np.linspace(0, 2 * np.pi, 8760)

        # Idea: Subdivide all points to incremental bars that have their own color
        X, Y = constructXY(y)

        radii = np.ones(len(Y))
        days = X
        bottom = Y
        width = 0.01

        self.createFig()

        # Rescale the color map

        # https://matplotlib.org/3.1.0/tutorials/colors/colormap-manipulation.html
        cmap = 'jet'
        norm = col.Normalize(vmin=min(y), vmax=max(y))

        # First we should filter input_array so that it does not contain NaN or Inf.
        input_array = np.array(Y)
        result_array = np.array([])
        if not np.unique(input_array).shape[0] == 1:
            result_array = (input_array - np.min(input_array)) / np.ptp(input_array)
        # To extend it to higher dimension, add axis= kwarvg to np.min and np.ptp

        colors = plt.cm.get_cmap(cmap, int(max(Y) - min(Y)))
        color_vals = colors(result_array)
        # print("colors: ",colors.shape)

        # create a scalarmappable from the colormap
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array(np.array([]))

        cbar = self.fig.colorbar(sm)
        cbar.ax.set_ylabel('Dry Bulb Temperature $[°C]$')

        self.ax.bar(days, radii, width=width,
                    bottom=bottom, color=color_vals, zorder=5)

        self.scale_inputs(y, ymin, ymax, yorigin)
        self.set_title()

        # fig, ax = self.getColorMap(fig,ax, x,y, cmap)

    def plot_bars(self, dpi=100, x=None, y=None, ymin=None, ymax=None, yorigin=None, export=False):
        plot_type = PlotType.BarPlot

        self.plot_bar_generic(x, y, ymin, ymax, yorigin)
        self.export_result(plot_type.name, dpi, export)

    def plot_bars_st(self):
        self.plot_bar_generic(x=None, y=None, ymin=None, ymax=None, yorigin=None)
        st.pyplot(self.fig)

    def plot_line_generic(self, x=None, y=None, ymin=None, ymax=None, yorigin=None):
        print("Plotting line chart...")
        if (x is None and y is None):
            y = self.data['Dry Bulb Temperature'][::-1]
            x = np.linspace(0, 2 * np.pi, 8760)

        self.createFig()

        # rain
        # ax.scatter(x, y, s= precipitation*10, alpha=0.2, linewidth=0, zorder=5)

        self.scale_inputs(y, ymin, ymax, yorigin)

        self.fig, self.ax = getColorMap(self.fig, self.ax, x, y)

        self.set_title()

    def plot_lines(self, dpi=100, x=None, y=None, ymin=None, ymax=None, yorigin=None, export=False):
        plot_type = PlotType.LinePlot

        self.plot_line_generic(x, y, ymin, ymax, yorigin)
        self.export_result(plot_type.name, dpi, export)

    def plot_lines_st(self):

        self.plot_line_generic(x=None, y=None, ymin=None, ymax=None, yorigin=None)
        st.pyplot(self.fig)
