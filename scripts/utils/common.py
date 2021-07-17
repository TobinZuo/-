import re


def get_index_from_file(dir, file_name):
    file_path = "../../Notes/{}/{}".format(dir, file_name)
    print(file_path)
    try:
        with open(file_path, 'r', encoding='utf8') as f:
            note_data = f.read()
            pos = re.search("https://.+.com/problems/.+\s", note_data).span()
            addr_split = note_data[pos[0]: pos[1]].strip().replace("\n", "").split("/")
            index = addr_split[-1] if addr_split[-1] != "" else addr_split[-2]
    except:
        print("{} does not exist!".format(file_path))
    return index

