from setuptools import setup, find_packages

with open('requirements.txt') as req:
    install_requires = req.read()

setup(
    name = "API_de_usuarios_v5",
    version = "0.0.1",
    description = "Rest API with Python and Flask",
    url = "https://github.com/lucasharzer/API_de_usuarios_v5",
    author = "Lucas Harzer",
    author_email = "lucasmatos592@gmail.com",
    packages = find_packages(),
    install_requires = [install_requires],
    zip_safe = False
)