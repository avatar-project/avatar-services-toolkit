import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Avatar Services Toolkit',
    version='0.1.0',
    description='Toolkit for services development for avatar ecosystem',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
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
