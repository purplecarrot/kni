from setuptools import setup, find_packages


setup(
    name = 'kni',
    version = '1.01',
    description = "Python Container Demo Tool",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    install_scripts = ['bin/app.sh'],
    install_requires = [
        'flask'
    ]
)
