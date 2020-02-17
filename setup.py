from setuptools import setup

setup(
    name='PhotogrammetryLab1',
    version='0.1',
    description='Similarity, Affine, and Projective transforms for ' +
        'comparator measurements of image fiducial marks.',
    author='Preston Hartzell',
    author_email='preston.hartzell@gmail.com',
    packages=['lab1'],
    entry_points={
        'console_scripts':['transform=lab1.lab1:main'],
    }
)
