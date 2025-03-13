from setuptools import setup, find_packages

setup(
    name="anonymization",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mistralai==1.2.6",
        "transformers==4.49.0",
        "pytest==8.3.5",
        "unittest-xml-reporting==3.2.0",
        "torch==2.6.0",
        "tiktoken==0.9.0",
        "protobuf==6.30.0",
        "sentencepiece==0.2.0",
        "cmake==3.31.6"
    ],
    author="Florent Grenier",
    description="A Python library for text anonymization.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FlorentGrenier/FacerAnonim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
