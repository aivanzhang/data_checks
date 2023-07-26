python -m build &&
tar tzf dist/data_checks-0.1.tar.gz &&
twine check dist/*