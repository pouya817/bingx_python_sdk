from setuptools import setup


setup(
    name='bingx-python',
    version='v1.0.0',
    packages=['bingx', 'bingx/base_request','kucoin/trade'],
    license="HUT",
    author='pouya',
    author_email="m.pouya.ch@gmail.com",
    url='https://github.com/pouya817/bingx_python_sdk',
    description="bingx-api-sdk",
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: HUT License",
        "Operating System :: OS Independent",
    ],
)