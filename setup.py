import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Reprocessing-Solver-Alex-M-Simmons", # Replace with your own username
    version="0.0.1",
    author="Alex Simmons",
    author_email="author@example.com",
    description="A Ore Solection Optimiser for Reprocessing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/A-M-Simmons/EVE_Reprocessing_Optimiser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)