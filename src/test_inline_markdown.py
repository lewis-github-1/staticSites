from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

def test_split_simple_code():
    node = TextNode("this is `code` here", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    assert len(new_nodes) == 3
    assert new_nodes[0].text == "this is "
    assert new_nodes[0].text_type == TextType.TEXT
    assert new_nodes[1].text == "code"
    assert new_nodes[1].text_type == TextType.CODE
    assert new_nodes[2].text == " here"
    assert new_nodes[2].text_type == TextType.TEXT

def test_split_no_delimiters():
    node = TextNode("nothing special here", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    assert len(new_nodes) == 1
    assert new_nodes[0].text == "nothing special here"
    assert new_nodes[0].text_type == TextType.TEXT

def test_split_bold():
    node = TextNode("start **bold** end", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    assert len(new_nodes) == 3
    assert new_nodes[0].text == "start "
    assert new_nodes[0].text_type == TextType.TEXT
    assert new_nodes[1].text == "bold"
    assert new_nodes[1].text_type == TextType.BOLD
    assert new_nodes[2].text == " end"
    assert new_nodes[2].text_type == TextType.TEXT

def test_split_multiple_sections():
    node = TextNode("a `one` b `two` c", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    texts = [n.text for n in new_nodes]
    types = [n.text_type for n in new_nodes]
    assert texts == ["a ", "one", " b ", "two", " c"]
    assert types == [
        TextType.TEXT,
        TextType.CODE,
        TextType.TEXT,
        TextType.CODE,
        TextType.TEXT,
    ]

def test_split_ignores_non_text_nodes():
    text_node = TextNode("x `y` z", TextType.TEXT)
    bold_node = TextNode("already bold", TextType.BOLD)
    new_nodes = split_nodes_delimiter(
        [text_node, bold_node], "`", TextType.CODE
    )
    # should split first, keep second intact
    assert len(new_nodes) == 4
    assert new_nodes[0].text == "x "
    assert new_nodes[0].text_type == TextType.TEXT
    assert new_nodes[1].text == "y"
    assert new_nodes[1].text_type == TextType.CODE
    assert new_nodes[2].text == " z"
    assert new_nodes[2].text_type == TextType.TEXT
    assert new_nodes[3] is bold_node  # unchanged
