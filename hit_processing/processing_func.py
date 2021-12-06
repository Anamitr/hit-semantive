import os


def hit_init():
    hit_file_name = ".hit"
    if os.path.exists(hit_file_name):
        print(f"Hit repo already initialized at {os.getcwd()}")
        return
    file = open(hit_file_name, 'w')
    file.write("# Hit Semantive file")
    file.close()
    print(f"Initialized empty Hit repository in {os.getcwd()}")


def get_new_files(hit_content: str) -> list:
    dir_content = os.listdir(os.getcwd())
    return [file for file in dir_content if file not in hit_content]


def read_hit_content() -> str:
    return open(".hit", 'r').read()


def hit_status():
    hit_content = read_hit_content()
    new_files = get_new_files(hit_content)
    [print(f"> {file_name} (new file)") for file_name in new_files]
