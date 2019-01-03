from setuptools import setup

setup(
    name = 'Scyland3D',
    version = '1.0.0',
    description = 'A Python package for processing 3D landmarks',
    long_description=open('README.md').read(),
    author = 'Fidji Berio and Yann Bayle',
    author_email = 'bayle.yann@live.fr',
    license='LICENSE',
    url = 'https://github.com/ybayle/Scyland3D',
    py_modules=['Scyland3D'],
    install_requires=[
        "numpy >= 1.13.3"
    ],
    entry_points='''
        [console_scripts]
        Scyland3D=Scyland3D:pts2csv
    ''',
)
