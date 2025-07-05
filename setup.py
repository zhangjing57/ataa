from setuptools import setup, find_packages

setup(
    name="auto_test",
    version="0.1.0",
    description="Fastapi Command Project",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "oslo.config",
        "alembic",
        "sqlalchemy",
        "databases",
        "pymysql",
    ],
)
