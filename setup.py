from setuptools import setup, find_packages

setup(
    name="translate_export_agent",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "streamlit",
        "openai",
        "anthropic",
        "pydantic",
        "aiohttp",
        "pytest",
    ],
)
