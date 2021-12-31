Remove-Item "dist" -Recurse
python setup.py bdist_wheel
twine upload dist/*
