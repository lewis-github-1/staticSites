def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
        elif node.text_type == TextType.TEXT:
            substring = node.text.split(delimiter)
            if len(substring) % 2 == 0:
                raise Exception("Error: Bad delimiter")
            for i in range(len(substring)):
                part = substring[i]
                if part == "":
                    continue
                if i % 2 == 0:
                    new_list.append(TextNode(part, TextType.TEXT))
                else:
                    new_list.append(TextNode(part, text_type))
    return new_list




