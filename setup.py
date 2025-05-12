from setuptools import setup, find_packages

setup(
    name='cse_logging',
    version='1.0.0',
    description='Centralized logging library for CSE services',
    author='YourOrg',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'alembic',
        'psycopg2-binary'
    ],
    entry_points={
        'console_scripts': [
            'cse-logging-migrate = cse_logging.migrations.env:run_migrations'
        ]
    }
)