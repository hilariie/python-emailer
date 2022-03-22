import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pymails',
    version='4.1.0',
    author='Akpu Chukwuma Hilary Jnr',
    description='Package that aids in sending emails to recipient(s)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hilariie/Pymail',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    setup_requires=['wheel']
)
