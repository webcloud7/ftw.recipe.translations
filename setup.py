import os
from setuptools import setup, find_packages


version = '2.0.0.dev0'

extras = {
    'tests': [
        'plone.testing',
    ],

    'masstranslate': [
        'gspread',
        'keyring',
        'oauth2client < 2a',
    ]
}

extras['tests'] += extras['masstranslate']


setup(name='ftw.recipe.translations',
      version=version,
      description='Mass export / import of translations into' +
      ' Google Docs Spreadsheets',

      long_description=open('README.rst').read() + '\n' +
      open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
          'Framework :: Plone',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.9',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],

      keywords='ftw recipe translations import export google docs',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.recipe.translations',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', 'ftw.recipe'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'argparse',
          'i18ndude',
          'path.py',
          'setuptools',
          'zc.buildout',
          'zc.recipe.egg',
      ],

      tests_require=extras['tests'],
      extras_require=extras,

      entry_points={
          'zc.buildout': [
              'default = ftw.recipe.translations.masstranslate.recipe:Recipe',
              'package = ftw.recipe.translations.i18nbuild.recipe:Recipe'],
          'console_scripts': [
              'masstranslate = ftw.recipe.translations.masstranslate.command:main',
              'i18n-build = ftw.recipe.translations.i18nbuild.command:main']
      })
