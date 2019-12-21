import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cspHyd8-cha10vd", # Replace with your own username
    version="0.0.1",
    author="Victor L. Do Nascimento",
    author_email="contact@victordn.me",
    description="Quasi-random hydration of organic crystal structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cha10vd/csphyd8",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
