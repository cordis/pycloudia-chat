from setuptools import setup, find_packages

setup(
    name='PyCloudia Chat example',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # pycloudia
        'twisted >= 13.2.0',
        'pyzmq >= 14.0.1',
        'tornado >= 3.1.1',
        #'springpython >= 1.3.0.RC1',
    ],
    author='CordiS',
    author_email='cordis@game-mafia.ru',
    description='PyCloudia Chat example demonstrates how to built distributed software',
    keywords='pycloudia chat example',
    url='https://github.com/cordis/pycloudia-chat',
)
