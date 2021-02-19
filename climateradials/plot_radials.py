import argparse
from climateradials import Radial

def q(s):
    return "'"+s+"'"

desc = "Please pass the epw file you would like to plot like: "+ q("plot_radials.py -f file.epw") + ""



parser = argparse.ArgumentParser(
    description=desc)
parser.add_argument('-f', '--file', type=str,  help='filepath, either as local path or url')
parser.add_argument('-e', '--export', type=bool, default=True, help='export, either True or False')


args = vars(parser.parse_args())
print(desc)

if args['file'] == '' or args['file'] == None:
    print("No filename given, abort.")
else:

    r = Radial(args['file'])
    r.plot_bars(export = args['export'])


