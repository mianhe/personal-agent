from setuptools import setup, find_namespace_packages

setup(
    name="personal-agent",
    version="0.1.0",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        # Add your project dependencies here
    ],
    entry_points={
        "console_scripts": [
            "personal-agent=cli.cli:main",
        ],
    },
) 