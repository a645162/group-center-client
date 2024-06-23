import os

current_py_path = os.path.abspath(__file__)
path_dir_config = os.path.dirname(current_py_path)
path_dir_base = os.path.dirname(path_dir_config)

if __name__ == "__main__":
    print(path_dir_base)
