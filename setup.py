from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="modern-eliza",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A modern implementation of the ELIZA chatbot with web interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ELIZA",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=3.0.0",
        "flask-socketio>=5.3.6",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "eliza-cli=eliza.cli:main",
            "eliza-web=eliza.web.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "eliza": [
            "web/static/css/*.css",
            "web/static/js/*.js",
            "web/templates/*.html",
        ],
    },
)
