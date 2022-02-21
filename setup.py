import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bvPlayer",
    version="0.1.0",
    author="Joshua Carlson",
    author_email="joshuacarlson@cedarville.edu",
    description="A borderless video player with sound",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jwcarlson01/bvPlayer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'ffpyplayer>=4.3.2',
        'opencv-python>=4.5.5.62',
        'Pillow>=9.0.1'
    ],
    packages=["bvPlayer"],
    include_package_data = True
)
