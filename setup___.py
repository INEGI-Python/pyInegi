import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyInegi",
    version="0.1.1",
    author="Instituto Nacional de Estadística y  Geografía",
    author_email="inegi.soporte@inegi.org.mx",
    description="Aplicación para el tratamiento de información estadística y geográfica",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/INEGI-Python/pyInegi.git",
    packages=setuptools.find_packages(),
    scripts=["pyInegi"],
    install_requires=[
        'numpy>=2.1.1',
        'matplotlib>=3',
        'folium>=0.17.0',
		'mapclassify>=2.8.0',
		'httpimport>=1.4.0',
		'geopandas>=1.0.1',
		'requests>=2.32.3',
		'shapely>=2.0.6',
        'scipy>=1.14.1'
    ],
    extras_require={
        'lark-parser': ["regex"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
 )