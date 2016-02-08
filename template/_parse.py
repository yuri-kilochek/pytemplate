
def split(characters):
    line = ''
    for character in characters:
        if character == '\n':
            yield line
            line = ''
        else:
            line += character

    yield line


def probe_depth(lines):
    for line in lines:
        depth = 0
        for character in line:
            if character != ' ':
                break

            depth += 1

        yield depth, line.strip()


def adjust_empty_depth(lines):
    base_depth = None

    empty_count = 0
    for depth, text in lines:
        if text == '':
            empty_count += 1
            continue

        if base_depth is None:
            base_depth = depth

        while empty_count > 0:
            yield depth, ''
            empty_count -= 1

        yield depth, text

    while empty_count > 0:
        yield base_depth, ''
        empty_count -= 1


def build_tree(lines):
    rest, depth, childs = None, -1, []
    for line_depth, line_text in lines:
        while depth >= line_depth:
            rest, depth, childs = rest

        line_childs = []
        childs.append((line_depth, line_text, line_childs))
        rest, depth, childs = (rest, depth, childs), line_depth, line_childs

    while depth >= 0:
        rest, depth, childs = rest

    return childs


def simplify_tree(nodes):
    common_depth, simplified_nodes = None, []
    for depth, text, childs in nodes:
        if common_depth is None:
            common_depth = depth
        else:
            assert depth == common_depth

        child_depth, childs = simplify_tree(childs)
        simplified_nodes.append((text, child_depth, childs))

    return common_depth, simplified_nodes






def parse(characters):
    lines = split(characters)
    lines = probe_depth(lines)
    lines = adjust_empty_depth(lines)
    nodes = build_tree(lines)
    nodes = simplify_tree(nodes)
    return nodes


text = r'''
    <table>
        % for i in range(n):
            <tr>
                % if i % 2 == 0:
                    <td>i = {% i %}</td>
                % else:
                    % j = i**2
                    <td>i**2 = {% j %}</td>
            </tr>
    </table>
    
'''

from pprint import pprint
pprint(parse(text))

