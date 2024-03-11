from setuptools import setup,  find_packages

setup(
    name='transition_lib',
    version='0.1.0',    
    description='',
    url='',
    author='',
    author_email='',
    packages=find_packages(),
    install_requires=['requests', 'configparser', 'geojson'                    
                      ],

    classifiers=[
        'License :: OSI Approved :: MIT License',  
        'Operating System :: Linux', 
        'Programming Language :: Python :: 3',
    ],
)
