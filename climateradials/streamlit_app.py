import streamlit as st
from climateradials import Radial

default_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/NY/USA_NY_New.York-J.F.Kennedy.Intl.AP.744860_TMY3/USA_NY_New.York-J.F.Kennedy.Intl.AP.744860_TMY3.epw"

# Draw a title and some text to the app:
'''
# ClimateRadials

To plot EPW data in a radial chart, please provide a url pointing to an EPW file of your choice. You may find urls [here]( https://www.energyplus.net/weather).
'''

url = st.text_input('Please provide a url here', value=default_url, max_chars=None, key=None, type='default')
r = Radial(url)


style = st.radio(
 "Please provide a style for the plot",
 ('Bar chart', 'Line chart'))

def run():
    st.write('Plot EPW')
    return


if st.button('Plot EPW'):
    st.write('Plotting...')
    if style == "Bar chart":

        r.plot_bars_st()
    else:
        r.plot_line_st()
    r.delete_epw()

