from setuptools import setup, find_packages

setup(
    name='transition-lib-test',
    version='0.1.11',    
    description='A Python package to interact with the Transition API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mathilde',
    packages=find_packages(),
    install_requires=['requests', 'geojson'],
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent', 
        'Programming Language :: Python :: 3',
    ],
)
