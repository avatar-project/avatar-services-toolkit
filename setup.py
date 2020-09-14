import setuptools
from os import path

here = path.abspath(path.dirname(__file__))

about = {}
about_path = path.join(here, 'services_toolkit', '__version__.py')
with open(about_path, 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    packages=setuptools.find_packages(),
    install_requires=[
        'flask>=1.1.1',
        'flask-sqlalchemy>=2.3.2',
        'psycopg2-binary>=2.7.5',
        'requests>=2.23.0',    # registration
        'apispec>=3.3.0',      # registration
        'marshmallow>=3.6.0',  # registration
        'flasgger>=0.9.4',     # registration
        'python-keycloak~=0.21.0',  # sso_helper
        'cryptography~=3.0',        # sso_helper
        'PyJWT~=1.7.1',             # sso_helper
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
