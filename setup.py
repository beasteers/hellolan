import setuptools

NAME = 'hellolan'
VERSION = '0.0.12'
ORG = 'beasteers'

setuptools.setup(
    name=NAME,
    version=VERSION,
    description='Scan and filter devices on your local network.',
    long_description=open('README.md').read().strip(),
    long_description_content_type='text/markdown',
    author='Bea Steers',
    author_email='bea.steers@gmail.com',
    url='https://github.com/{}/{}'.format(ORG, NAME),
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['hellolan=hellolan:main', 'hellossh=hellolan:ssh_main']},
    install_requires=['python-nmap', 'tabulate', 'fire', 'reprint', 'ifcfg'],
    license='MIT License',
    keywords='port scanning filter hostname ip lan wan localhost '
             '192.168 192.168.1.0 192.168.1.1')
