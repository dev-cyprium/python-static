import os


def discover_files(static_dir):
    if not os.path.exists(static_dir):
        raise Exception(f"{static_dir} doesn't exist")

    return __discover_internal(static_dir, [])


def __discover_internal(file_path, found=[]):
    contents = os.listdir(file_path)
    for path in contents:
        full_path = os.path.join(file_path, path)

        if os.path.isdir(full_path):
            __discover_internal(full_path, found)
        else:
            found.append(full_path)

    return found
