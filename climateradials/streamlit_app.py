import streamlit as st
from climateradials import Radial
from epw_urls import epw_urls
import random
from datetime import datetime
random.seed(datetime.today().date())

default_url = random.choice(epw_urls)
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
    'Please select a file to plot.',
    epw_urls)

st.write('You selected:', url_multi)

style = st.radio(
    "Please provide a style for the plot",
    ('Line chart', 'Bar chart'))


def run():
    st.write('Plot', key="1")
    return


if st.button('Plot', key="1"):

    if len(url_multi) > 0 and url_multi is not None:
        url = url_multi

        for epw in url:
            r = Radial(epw)

            st.write('Plotting...')
            if style == "Bar chart":

                r.plot_bars_st()
            else:
                r.plot_line_st()
            r.delete_epw()
        st.stop()

    else:
        r = Radial(url)

        # if st.button('Plot'):
        st.write('Plotting...')
        if style == "Bar chart":

            r.plot_bars_st()
        else:
            r.plot_line_st()
        r.delete_epw()
        st.stop()
