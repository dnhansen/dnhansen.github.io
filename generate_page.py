import json
import textwrap
import sys

# FUNCTIONS

def format_element(page_info, element):
    return page_info[element]


def format_list(page_info, lst, wrapper, indent=''):
    return '\n'.join(wrapper.format(indent=indent, element=element) for element in page_info[lst])


def format_file(page_info, path, encoding, indent=''):
    if page_info[path] == None:
        return ''
    
    with open(page_info[path], encoding=encoding) as page:
        content = ''.join(row for row in page)
    content = textwrap.indent(content, indent)
    return content


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print('ERROR: No page specified.')
    else:
        page = args[1]
    
    encoding = 'utf-8'

    # Indentation
    css_indent = '    '
    head_indent = '    '
    body_indent = '      '

    # I/O
    with open('page_template.html', encoding=encoding) as template_file:
        template = ''.join(row for row in template_file)

    with open('page_info.json', encoding=encoding) as json_page_info:
        page_dict = json.load(json_page_info)

    page_info = page_dict[page]

    # Content
    title = format_element(page_info, 'title')
    css = format_list(page_info, 'css', '{indent}<link rel="stylesheet" type="text/css" href="/{element}">', css_indent)
    head = format_file(page_info, 'headPath', encoding, head_indent)
    body = format_file(page_info, 'bodyPath', encoding, body_indent)
    with open('header.html', encoding=encoding) as header_file:
        header = ''.join(row for row in header_file)
    header = textwrap.indent(header, body_indent)
    with open('footer.html', encoding=encoding) as footer_file:
        footer = ''.join(row for row in footer_file)
    footer = textwrap.indent(footer, body_indent)

    # Format and save
    formatted_page = template.format(title=title, head=head, css=css, main=body, header=header, footer=footer)

    with open(page_info['filename'], 'w', encoding=encoding) as f:
        f.write(formatted_page)