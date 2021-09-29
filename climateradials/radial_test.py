from climateradials import Radial

url = "https://energyplus-weather.s3.amazonaws.com/europe_wmo_region_6/DEU/DEU_Koln.105130_IWEC/DEU_Koln.105130_IWEC.epw"

r = Radial(url)

r.plot_bars()

r.plot_bars(export=True)

r.plot_lines()

r.plot_lines(export=True)

# from pathlib import Path
# import requests
# from tqdm import tqdm
# response = requests.get("https://energyplus-weather.s3.amazonaws.com/europe_wmo_region_6/DEU/DEU_Koln.105130_IWEC/DEU_Koln.105130_IWEC.epw", stream=True, headers={'User-agent': 'Mozilla/5.0'})
# file_path_local =  Path(Path.cwd() / Path(url.split('/')[-1]))
#
# print("Downloading file...")
# with open(file_path_local, "wb") as handle:
#     for data in tqdm(response.iter_content()):
#         handle.write(data)

