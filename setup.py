from setuptools import setup, find_packages

setup(
    name='registry-inspector',
    version='1.0.0',
    description='A tool for inspecting the contents of your docker registry',
    #long_description=
    #url=
    author='John Odetokun',
    author_email='rbcs.john@gmail.com',
    #license=
    classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: SRE team',
    'Topic :: Docker registry :: inspector',
    #'License ::
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    ],
    keywords='Docker registry image layer inspector',
    packages=find_packages(),
    install_requires=['requests'],
    #extras_require={},
    #package_data={},
    #data_files[]
    #entry_points={},
)
