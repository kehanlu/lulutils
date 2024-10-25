from setuptools import setup, find_packages

setup(
    name="lulutils",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here
        ],
    },
    author="Ke-Han Lu",
    description="A utility package for various tasks",
    long_description="",
    long_description_content_type='text/markdown',
    url="https://github.com/kehanlu/lulutils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
