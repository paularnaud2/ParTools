from os.path import realpath


def get_root():
    root = realpath(__file__)
    root = str(root).replace("\\", "/")
    root = root.replace("__init__.py", "")
    return root
