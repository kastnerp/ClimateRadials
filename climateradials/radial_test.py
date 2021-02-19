from climateradials import Radial

url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/NY/USA_NY_New.York-J.F.Kennedy.Intl.AP.744860_TMY3/USA_NY_New.York-J.F.Kennedy.Intl.AP.744860_TMY3.epw"


r = Radial(url)
r.plot_bars(export=True)
r.plot_line(export=True)
r.plot_bars()
r.plot_line()
