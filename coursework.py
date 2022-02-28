import csv
import yaml


## Formatting helper functions

def bib_entry_format(entry_name):
    if entry_name[0] != "!":
        return entry_name

    entry_name = entry_name[1:]
    entry = literature_dict[entry_name]
    title = entry["title"]
    authors = ", ".join([author["lastname"] for author in entry["author"]])
    entry_output = ", ".join([authors, f'<em>{title}</em>'])
    return entry_output


def format_literature(lit_string):
    lit_list = [entry.strip() for entry in lit_string.split(",")]
    lit_output = []
    for entry in lit_list:
        entry = bib_entry_format(entry)
        lit_output.append(entry)
    return ". ".join(lit_output) + "."


## Sorting helper functions

def sort_semester(s):
    s = s.lower()
    if s == "spring":
        return 0
    else:
        return 1


def sort_department(s):
    s = s.lower()
    if "math" in s:
        return 0
    elif "phys" in s:
        return 1
    else:
        return 2


def sort_ordinary(s):
    s = s.lower()
    if s == "yes":
        return 0
    else:
        return 1


def area_ordering(s):
    order = ('Analysis',
             'Algebra',
             'Geometry',
             'Statistics',
             'Misc mathematics',
             'Physics',
             'Programming',
             'Theoretical CS',
             'Misc CS')
    return order.index(s)


## I/O

with open('coursework.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    data = [row for row in reader]
bom = True

with open('literature.yaml', encoding='utf-8') as literature:
    # We trust the input, but we don't need the full power of
    # yaml.FullLoader, so we just use yaml.SafeLoader.
    literature_dict = yaml.load(literature, yaml.SafeLoader)


keys = data[0]
if bom:
    keys[0] = keys[0][1:]

dict_list = []
for row in range(1, len(data)):
    d = {keys[col]: data[row][col] for col in range(len(keys))}
    dict_list.append(d)

sorted_list = sorted(dict_list, key = lambda d: (area_ordering(d['Area']),
                                                 d['Year'],
                                                 sort_semester(d['Semester']),
                                                 sort_ordinary(d['Ordinary']),
                                                 sort_department(d['Department'])))


## Build output

current_area = None
output = []
indent = '  '

for idx, d in enumerate(sorted_list):
    course = d['English']
    hidden = d['Hidden']

    if not course: # Or filter them out when sorting?
        continue

    if hidden == 'Yes':
        continue

    area = d['Area']
    year = int(d['Year'])
    semester = d['Semester']
    grade = d['Grade']
    grade_format = grade if d['Ordinary'] == 'Yes' else '*'
    if grade_format == "Pass":
        grade_format = "P"
    description = d['Content']

    if current_area != area:
        current_area = area
        output.append(f'<h3>{area}</h3>')
        output.append('<ul>')

    output.append(f'{indent}<li style="--grade: \'{grade_format}\'">')
    output.append(f'{2*indent}<span class="course">{course}</span><span class="time">{semester} {year}</span>')

    # Course description
    output.append(f'{2*indent}<div class="description">{description}</div>')

    # Literature
    literature = format_literature(d['Literature'])
    if literature:
        output.append(f'{2*indent}<div class="literature"><em>Literature</em>: {literature}</div>')
    
    output.append(f'{indent}</li>')

    try:
        next_area = sorted_list[idx+1]['Area']
    except:
        next_area = None
    if current_area != next_area:
        output.append('</ul>')
        current_area = area

output = '\n'.join(output)

with open('coursework_body.html', 'w', encoding='utf-8') as f:
    f.write(output)
