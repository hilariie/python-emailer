import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='python_emailer',
    version='1.5.3',
    author='Akpu Chukwuma Hilary Jnr',
    author_email='holaryc@gmail.com',
    description='Package that aids in sending emails to recipient(s)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hilariie/py-emailer',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['wheel']
)
