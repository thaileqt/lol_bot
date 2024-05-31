def extract_name_tag(name_with_tag):
    """
   Extracts the name and tag from a string containing both.
   :param name_with_tag: 'Thái Lê Tôn Giả#3110'
   :return: ('Thái Lê Tôn Giả', '3110')
   """
    if "#" not in name_with_tag:
        return None

    name, tag = name_with_tag.split("#")
    return name.strip(), tag.strip()



