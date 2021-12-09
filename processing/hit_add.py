import os

from processing.hit_processing import read_hit_content, save_hit_content


def hit_add(file_paths):
    """ file_paths is str or list of str """
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    elif isinstance(file_paths, list):
        pass
    else:
        raise TypeError("file_paths should be str or list of str")

    hit_content = read_hit_content()
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"No such file {file_path}")
        else:
            if file_path not in hit_content["staged"]:
                hit_content["staged"] += [file_path]
    hit_content["staged"] = sorted(hit_content["staged"])
    save_hit_content(hit_content)
