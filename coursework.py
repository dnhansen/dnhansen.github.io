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
    entry_output = ", ".join([authors, f'<cite class="book">{title}</cite>'])
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


def subject_ordering(s):
    order = ('Mathematics',
             'Physics',
             'Computer science',
             'Electrical engineering')
    return order.index(s)


def area_ordering(s):
    order = ('Analysis',
             'Algebra',
             'Geometry',
             'Statistics',
             'Miscellaneous mathematics',
             'Programming',
             'Theoretical computer science',
             'Miscellaneous computer science',
             'Electrical engineering',
             '')
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

sorted_list = sorted(dict_list, key = lambda d: (subject_ordering(d['Subject']),
                                                 area_ordering(d['Area']),
                                                 d['Year'],
                                                 sort_semester(d['Semester']),
                                                 sort_ordinary(d['Ordinary'])))


## Build output

current_subject = None
current_area = None
output = []
indent = '  '

## Initial text

init_text = """//h2;Coursework
<p>
  The letter next to the course name indicates the grade I received for the course. A &lsquo;P&rsquo; indicates a pass. An asterisk indicates that I audited the course and did not receive a grade.
</p>"""
output.append(init_text)

# For TOC
# area_list = []
# area_id_list = []

for idx, d in enumerate(sorted_list):
    course = d['English']
    hidden = d['Hidden']

    if not course: # Or filter them out when sorting?
        continue

    if hidden == 'Yes':
        continue

    subject = d['Subject']
    area = d['Area']
    area_short = d['Area short']
    # area_id = area.replace(' ', '_')
    year = int(d['Year'])
    semester = d['Semester']
    institution = d['Institution']
    grade = d['Grade']
    grade_format = grade if d['Ordinary'] == 'Yes' else '*'
    if grade_format == "Pass":
        grade_format = "P"
    description = d['Content']

    if current_subject != subject:
        current_subject = subject
        output.append(f'//h3;{subject}')

    if current_area != area:
        current_area = area
        if area:
            output.append(f'//h4;{area}')
        # output.append(f'<h2 id="{area_id}">{area}</h2>')
        output.append('<ul class="course_list">')
        # # For TOC
        # area_list.append(area)
        # area_id_list.append(area_id)


    output.append(f'{indent}<li>')
    output.append(f'{2*indent}<div>')
    output.append(f'{3*indent}<div class="grade">{grade_format}</div>')
    output.append(f'{3*indent}<div class="course">{course}</div>')
    output.append(f'{2*indent}</div>')
    output.append(f'{2*indent}<div class="time_and_place">')
    output.append(f'{3*indent}<ul>')
    output.append(f'{4*indent}<li>{semester} {year}</li>')
    output.append(f'{4*indent}<li>{institution}</li>')
    output.append(f'{3*indent}</ul>')
    output.append(f'{2*indent}</div>')


    # output.append(f'{indent}<li style="--grade: \'{grade_format}\'">')
    # # output.append(f'{2*indent}<span class="course">{course}</span><span class="time">{semester} {year}</span>')
    # output.append(f'{2*indent}<div class="course">{course}</div>')
    # output.append(f'{2*indent}<div class="time_and_place">')
    # output.append(f'{3*indent}<span>{semester} {year}</span>')
    # output.append(f'{3*indent}<span style="padding: 0 3pt">&bull;</span>')
    # output.append(f'{3*indent}<span>{institution}</span>')
    # output.append(f'{2*indent}</div>')

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

# # Build TOC

# toc = []
# toc.append('<div id="toc">')
# toc.append(f'{indent}<h2>Contents</h2>')
# toc.append(f'{indent}<ol>')

# for i in range(len(area_list)):
#     toc.append(f'{2*indent}<li><a href="#{area_id_list[i]}" class="toclink">{area_list[i]}</a></li>')

# toc.append(f'{indent}</ol>')
# toc.append('</div>')

# toc = '\n'.join(toc)
# output = toc + '\n' + output

# Write output

with open('coursework_body.html', 'w', encoding='utf-8') as f:
    f.write(output)
