from setuptools import setup, find_packages

setup(
    name="pyInegi",
    version="2025.0.2",
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'wheel',
    ],
    dependencies=[
        'numpy',
        'matplotlib',
        'folium', 
        'mapclassify',
        'httpimport',
        'geopandas',
        'requests',
        'shapely'
        'scipy',
        'fiona',
        'euclid3',
        'rtree'
    ],
)
