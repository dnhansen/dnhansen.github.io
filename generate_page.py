import yaml
import textwrap
import sys
from typing import Optional

elem = str | list[str]

# FUNCTIONS

def get_filetype(s: str) -> str:
    return s.split(".")[-1]


def format_file(path: str, indent: str = '') -> str:
    with open(path, encoding='utf-8') as page:
        content: str = ''.join(row for row in page)
    content = textwrap.indent(content, indent)
    return content


def format_element(element: Optional[str], indent: str) -> str:
    if not element:
        return ''
    filetype: str = get_filetype(element)
    match filetype:
        case 'css':
            return f'{indent}<link rel="stylesheet" type="text/css" href="./{element}">'
        case 'js':
            return f'{indent}<script src="{element}"></script>'
        case 'html':
            return format_file(element, indent = indent)
        case _:
            return element


def format_elements(page_info: dict[str, elem], element: str, indent: str = '') -> str:
    data: elem = page_info[element]
    if not type(data) == list:
        data = [data]
    return '\n'.join(map(lambda e: format_element(e, indent), data))


def format_body(page_info: dict[str, elem],
                nav_include: bool,
                encoding: str,
                indent: str = '',
                nav_indent: str = '') -> tuple[str, str]:
    with open(page_info['body'], encoding=encoding) as page:
        content: list[str] = [row for row in page]
    
    # Format code
    code: bool = False
    for i in range(len(content)):
        row: str = content[i]
        if row.startswith('//code-start'):
            content[i] = '<pre><code>'
            code = True
        elif row.startswith('//code-end'):
            content[i] = '</code></pre>\n'
            code = False
        elif code:
            content[i] = f'<span>{row[:-1]}</span>\n'





    nav: list[str]
    if nav_include:
        nav = [f'{nav_indent}<nav>', f'{nav_indent}  <h2>Contents</h2>']
    else:
        nav = ['']
    
    current_level: int = 2
    for i in range(len(content)):
        row: str = content[i]
        if row[:2] != "//":
            continue
        row = row[2:]
        
        header_type: str
        header_text: str
        header_num: int
        header_type, header_text = row[:-1].split(";")
        header_num = int(header_type[1])
        header_id = header_text.lower().replace(" ", "_")
        if header_num > 2:
            content[i] = f'<h{header_num} id="{header_id}"><a href="#{header_id}">{header_text}</a></h{header_num}>\n'
        else:
            content[i] = f'<h{header_num}>{header_text}</h{header_num}>'

        if nav_include and header_num > 2:
            if header_num > current_level:
                current_level = header_num
                nav_indent += '  '
                nav.append(f'{nav_indent}<ul>')
                nav_indent += '  '
            elif header_num < current_level:
                current_level = header_num
                nav[-1] = nav[-1] + '</li>'
                nav_indent = nav_indent[2:]
                nav.append(f'{nav_indent}</ul>')
                nav_indent = nav_indent[2:]
                nav.append(f'{nav_indent}</li>')
            else:
                nav[-1] = nav[-1] + '</li>'

            nav.append(f'{nav_indent}<li><a href="#{header_id}" class="navlink">{header_text}</a>')

    if nav_include:
        if current_level > 2:
            nav[-1] = nav[-1] + '</li>'
            nav_indent = nav_indent[2:]
            nav.append(f'{nav_indent}</ul>')
            current_level -= 1

        while current_level > 2:
            nav_indent = nav_indent[2:]
            nav.append(f'{nav_indent}</li>')
            nav_indent = nav_indent[2:]
            nav.append(f'{nav_indent}</ul>')
            current_level -= 1
        
        nav_indent = nav_indent[2:]
        nav.append(f'{nav_indent}</nav>')

    return (textwrap.indent(''.join(content), indent), '\n'.join(nav))


def generate_page(page_dict, page):
    encoding: str = 'utf-8'

    # Indentation
    head_indent: str = '    '
    body_indent: str = '      '

    # I/O
    with open('page_template.html', encoding=encoding) as template_file:
        template: str = ''.join(row for row in template_file)

    page_info: dict[str, elem] = page_dict[page]

    # Content
    title: str = format_elements(page_info, 'title')
    css: str = format_elements(page_info, 'css', head_indent)
    script: str = format_elements(page_info, 'script', head_indent)
    nav_include: bool = page_info['nav']
    body: str
    nav: str
    body, nav = format_body(page_info, nav_include, encoding, body_indent, head_indent)

    with open('header.html', encoding=encoding) as header_file:
        header = ''.join(row for row in header_file)
    header: str = textwrap.indent(header, body_indent)

    with open('footer.html', encoding=encoding) as footer_file:
        footer = ''.join(row for row in footer_file)
    footer: str = textwrap.indent(footer, body_indent)

    # Format and save
    formatted_page: str = template.format(title=title, css=css, script=script, nav=nav, main=body, header=header, footer=footer)

    with open(page_info['filename'], 'w', encoding=encoding) as f:
        f.write(formatted_page)


if __name__ == '__main__':
    encoding: str = 'utf-8'

    # I/O
    with open('page_info.yaml', encoding=encoding) as yaml_page_info:
        # We trust the input, but we don't need the full power of
        # yaml.FullLoader, so we just use yaml.SafeLoader.
        page_dict = yaml.load(yaml_page_info, yaml.SafeLoader)

    args: list[str] = sys.argv
    pages: str
    if len(args) < 2:
        # Generate all pages
        pages = page_dict.keys()
    else:
        pages = [args[1]]

    for page in pages:
        generate_page(page_dict, page)