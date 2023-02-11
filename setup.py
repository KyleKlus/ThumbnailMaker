__NAME__=CoverMaker.core.NAME
__VERSION__=CoverMaker.core.VERSION

REQUIREMENTS = [
    'Pillow',
    'numpy',
    'tkinter'
]

setup(
    name=__NAME__,
    version=__VERSION__,
    description='A simple Python project',
    url='',
    author='Kyle Klus',
    author_email='kyle.klus@gmx.de',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    #keywords='midi music data',
    packages=find_packages('''exclude=('test*', 'examples','docs')'''),
    install_requires=REQUIREMENTS,
    '''
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    
    project_urls={
        'Bug Reports': 'https://github.com/erinspace/sonify/issues',
        'Source': 'https://github.com/erinspace/sonify',
    },
    '''
)