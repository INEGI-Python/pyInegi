from setuptools import setup, find_packages

setup(
    name="pyInegi",
    version="2025.0.1",
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'wheel',
    ],
    install_requires=[
        'numpy>=2.1.1',
        'matplotlib>=3.9.2',
        'folium>=0.17.0', 
        'mapclassify>=2.8.0',
        'httpimport>=1.4.0',
        'geopandas>=1.0.1',
        'requests>=2.32.3',
        'shapely>=2.0.6',
        'scipy>=1.14.1',
        'fiona>=1.10.1',
        'euclid3>=0.1',
        'rtree>=1.0.1'
    ],
)