import setuptools

setuptools.setup(name='hellolan',
                 version='0.0.1',
                 description='Scan and filter devices on your local network.',
                 long_description=open('README.md').read().strip(),
                 long_description_content_type='text/markdown',
                 author='Bea Steers',
                 author_email='bea.steers@gmail.com',
                 # url='http://path-to-my-packagename',
                 packages=setuptools.find_packages(),
                 entry_points={'console_scripts': ['hellolan=hellolan:main']},
                 install_requires=['python-nmap', 'tabulate', 'reprint'],
                 license='MIT License',
                 keywords='')
