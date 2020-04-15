from setuptools import setup, find_packages
from codecs import open
from os import path


setup(name='climateradials',
      version='0.0.1',
      description='A python tool to create radial plots of climate data.',
      url='https://github.com/kastnerp/ClimateRadials',
      author='Patrick Kastner',
      author_email='patrick.kastner@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'epw @ https://github.com/building-energy/epw/tarball/master#egg=epw-d352d11',
          'seaborn==0.10.0',
          'cmocean>=2.0',
          'scipy>=1.4.1',
          'windrose==1.6.7',
          'numpy>=1.18.2',
          'matplotlib>=3.2.1',
      ]
      )
