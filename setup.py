import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pxng",
    version="0.0.10",
    author="Jean-Paul Balabanian",
    author_email="jepebe@prador.net",
    description="A library for fiddling with pixels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jepebe/pixelengine",
    packages=setuptools.find_packages(),
    license='BSD',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'glfw>=2.0.0',
        'pyopengl>=3.1.0',
        'freetype-py>=2.2.0',
        'numpy>=1.19.0',
        'imageio>=2.9.0',
        'pyglm>=1.99.0',
    ],
    extras_require={
        ':python_version < "3.7"': [
            'dataclasses',
        ],
    },
    package_data={'pxng': [
        'resources/fonts/C64_Pro_Mono-STYLE.ttf',
        'resources/shaders/*',
    ]
    },
    python_requires='>=3.6',
)
