from setuptools import setup, find_packages
from io import open

setup(
    name = 'Scyland3D',
    version = '1.0.18',
    description = 'A Python package for processing 3D landmarks',
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author = 'Fidji Berio and Yann Bayle',
    author_email = 'bayle.yann@live.fr',
    license='LICENSE',
    url = 'https://github.com/ybayle/Scyland3D',
    packages=find_packages(),
    include_package_data=True,
    package_data={'Scyland3D': ['test/*.csv', 'example/*.csv', 'test.sh']},
    install_requires=[
        "numpy >= 1.13.3"
    ],
    entry_points='''
        [console_scripts]
        Scyland3D=Scyland3D:main
    ''',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Bug Reports': 'https://github.com/ybayle/Scyland3D/issues',
    }
)
