import bencodepy as bcp
import json

def parse_torrent(torrent_file_path: str) -> list[dict]:
    """
    Parse the torrent file and extract the file data.

    Parameters:
        torrent_file_path (str): The path to the torrent file.

    Returns:
        list[dict]: A list of dictionaries, each containing the 'path' and 'length' of a file.
    """
    with open(torrent_file_path, "rb") as f:
        torrent_data = bcp.Bencode(encoding="utf-8", encoding_fallback="value").decode(f.read())

    file_data_list = []
    if "info" in torrent_data and "files" in torrent_data["info"]:
        files_len = len(torrent_data["info"]["files"])
        for file_info in torrent_data["info"]["files"]:
            length = file_info["length"]
            path = "/".join(file_info["path"])
            if files_len > 1:
                path = torrent_data["info"]["name"] + "/" + path

            file_data_list.append({"path": path, "length": length})

    return file_data_list

def build_path_tree(file_data_list: list[dict]) -> dict:
    """
    Build the tree-like structure out of the file data.

    Parameters:
        file_data_list (list[dict]): A list of dictionaries, each containing the 'path' and 'length' of a file.

    Returns:
        dict: A dictionary representing the tree-like structure of the files and directories, with the file lengths as values.
    """
    def _recurse(dic, path_parts, length):
        if not path_parts:
            return
        if len(path_parts) == 1:
            dic[path_parts[0]] = length
            return
        key, *new_path_parts = path_parts
        if key not in dic:
            dic[key] = {}
        _recurse(dic[key], new_path_parts, length)

    path_dict = {}
    for file_info in file_data_list:
        path_parts = file_info["path"].split("/")
        file_length = file_info["length"]
        _recurse(path_dict, path_parts, file_length)

    return path_dict

if __name__ == "__main__":
    while(1):
        torrent_file_path = input("输入Torrent文件路径：")
        # torrent_file_path = "s4665.torrent"
        file_data_list = parse_torrent(torrent_file_path)
        result = build_path_tree(file_data_list)
        decoded_str = bytes(json.dumps(result, indent=2), 'utf-8').decode('unicode_escape')
        print(decoded_str)

    
