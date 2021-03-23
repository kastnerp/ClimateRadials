import streamlit as st
from climateradials import Radial, PlotType
import random
from datetime import datetime
from os.path import basename
import epw_urls

random.seed(datetime.today().date())


def plot(epw_url, epw_value, plot_type):
    if not epw_url.endswith(".epw"):
        st.write('Please provide a proper url that ends with ''.epw''.')
        st.stop()

    st.write('Plotting', str(epw_value) + "...")
    r = Radial(epw_url)

    if plot_type == PlotType.BarPlot.name:
        r.plot_bars_st()
    else:
        # r.plot_line_st()
        r.plot_lines_st()
    r.delete_epw()


###
# Input
###

default_url = random.choice(list(epw_urls.epw_dict.values()))

# Draw a title and some text to the app:
'''
# ClimateRadials

To plot EPW data in a radial chart, please provide a url pointing to an EPW file of your choice. You may find urls [here]( https://www.energyplus.net/weather).
'''

url = st.text_input('Please provide a url here', value=default_url, max_chars=None, key="2", type='default')

'''
Or select several ones from the dropdown below.
'''

url_multi = st.multiselect(
    'Please select one or more files to plot.',
    list(epw_urls.epw_dict.keys()))

st.write('You selected:', url_multi)

style = st.radio(
    "Please select a preferred style for the plot",
    (PlotType.LinePlot.name, PlotType.BarPlot.name))

###
# Plotting
###

if st.button('Plot', key="1"):

    # st.write(url_multi)
    # st.write(url)

    if len(url_multi) > 0 and url_multi is not None:
        for value in url_multi:
            plot(epw_urls.epw_dict[value], value, style)
    else:
        plot(url, basename(url), style)

st.stop()
