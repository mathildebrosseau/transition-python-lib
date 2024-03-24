from setuptools import setup,  find_packages
from pathlib import Path

# The directory containing this file
HERE = Path(__file__).parent
description = (HERE / "README.md").read_text()
setup(
    name='transition_lib',
    version='0.1.0',    
    description='',
    packages=find_packages(),
    install_requires=['requests', 'configparser', 'geojson'                    
                      ],

    classifiers=[
        'License :: OSI Approved :: MIT License',  
        'Operating System :: Linux', 
        'Programming Language :: Python :: 3',
    ],
)
