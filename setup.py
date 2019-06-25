from setuptools import setup

setup(
    name = 'Scyland3D',
    version = '1.0.9',
    description = 'A Python package for processing 3D landmarks',
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author = 'Fidji Berio and Yann Bayle',
    author_email = 'bayle.yann@live.fr',
    license='LICENSE',
    url = 'https://github.com/ybayle/Scyland3D',
    py_modules=['Scyland3D'],
    include_package_data=True,
    package_data={'Scyland3D': ['test/*', 'example/*', 'test.sh']},
    install_requires=[
        "numpy >= 1.13.3"
    ],
    entry_points='''
        [console_scripts]
        Scyland3D=Scyland3D:main
    ''',
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
