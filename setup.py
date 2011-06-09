from setuptools import setup, find_packages

with open('README') as f:

    setup(name="Refugee",
          version="dev",
          packages=find_packages(),
          namespace_packages=['refugee'],
          include_package_data=True,
          author='Dan Colish',
          author_email='dcolish@gmail.com',
          description='Migration made easy',
          long_description=f.read(),
          zip_safe=False,
          platforms='any',
          license='BSD',
          url='http://www.github.com/dcolish/refugee',
          classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Console',
            'Intended Audience :: Education',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 2.7',
            'Operating System :: Unix',
            ],

          entry_points={
            'console_scripts': [
                'refugee=refugee.cli:main',
                ],
            },

          extras_require={
            'PG': ['psycopg2>=2.0.10'],
            'MYSQL': ['MySQL-python>=1.2.2'],
            'ORACLE': ['cx_Oracle>=5.0'],
            'MSSQL': ['pymssql>=1.0.2'],
            },

          install_requires=[
            'SQLAlchemy',
            ],
          )
