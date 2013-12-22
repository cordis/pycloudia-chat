from setuptools import setup, find_packages

setup(
    name='PyCloudia',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'twisted >= 13.2.0',

        # pycloudia
        'pyzmq >= 14.0.1',
        'tornado >= 3.1.1',
        'zope.interface >= 4.0.5',
    ],
    author='CordiS',
    author_email='cordis@game-mafia.ru',
    description='PyCloudia distributed software architecture',
    keywords='pycloudia distributed scale fault-tolerant',
    url='https://github.com/cordis/pycloudia',
)
