from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='1.0.5',
      description='Sorting and cleaning folder',
      url='https://github.com/HatsulaSeveryn/sort.py',
      author='Severyn Hatsula',
      author_email='',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:sort_folder']})