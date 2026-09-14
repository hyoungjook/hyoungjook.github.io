import json

# Replace Html Syntax
def _rhs(str):
    return str.replace('<strong>', '\\textbf{').replace('</strong>', '}') \
              .replace('<i>', '\\textit{').replace('</i>', '}') \
              .replace('<a href=\"', '\\href{').replace('\">', '}{').replace('</a>', '}')

# Remove Suffix Newline
def _rsn(str):
    if not str.endswith('\\newline\n'):
        return str
    return str[:-9] + '\n'

def generate_paragraph_section(section):
    latex_content = ""
    for item in section['items']:
        latex_content += _rhs(item)
        latex_content += '\\newline\n'
    return latex_content

def generate_organization_section(section):
    latex_content = '\\resumeSubHeadingListStart\n'
    for item in section['items']:
        latex_content += '\\resumeSubheading' + \
            '{\\href{' + item['organization_link'] + '}' + \
            '{' + item['organization'] + '}'
        if 'organization2' in item:
            latex_content += ' {\\normalfont \\&} \\href{' + item['organization2_link'] + '}' + \
                '{' + item['organization2'] + '}'
        latex_content += '}{' + item['location'] + '}{' + item['years'] + '}\n' + \
            '{' + item['job_title'] + '\\newline\n'
        if 'advisor' in item:
            latex_content += 'Advisor: \\href{' + item['advisor_link'] + '}{' + item['advisor'] + '}'
            if 'workedwith' in item:
                latex_content += '; closely worked with \\href{' + item['workedwith_link'] + '}{' + item['workedwith'] + '}'
            latex_content += ' \\newline\n'
        if 'details' in item:
            for detail in item['details']:
                latex_content += _rhs(detail) + '\\newline\n'
        if 'projects' in item:
            latex_content += '\\vspace{-15pt}\n\\begin{itemize}\n'
            for project in item['projects']:
                latex_content += '\\vspace{-1pt}\n'
                latex_content += '\\item {' + _rhs(project) + '}\n'
            latex_content += '\\end{itemize}\n'
        latex_content = _rsn(latex_content)
        latex_content += '}\n'
    latex_content += '\\resumeSubHeadingListEnd\n'
    return latex_content

def generate_publication_section(section):
    latex_content = '\\resumeSubHeadingListStart\n'
    for item in section['items']:
        latex_content += '\\resumeSubheadingItem{\n' + \
            _rhs(item['authors']) + '\\newline\n' + \
            '\\href{' + item['pub_link'] + '}{\\textbf{' + item['pub_title'] + '}} \\newline\n' + \
            '\\textit{' + item['journal'] + '}, ' + item['year']
        if 'etc' in item:
            latex_content += ' (' + _rhs(item['etc']) + ')'
        if 'slides' in item:
            latex_content += ' \\href{' + item['slides'] + '}{[Slides]}'
        if 'poster' in item:
            latex_content += ' \\href{' + item['poster'] + '}{[Poster]}'
        if 'blog' in item:
            latex_content += ' \\href{' + item['blog'] + '}{[Blog]}'
        latex_content += '}\n'
    latex_content += '\\resumeSubHeadingListEnd\n'
    return latex_content

def generate_simple_section(section):
    latex_content = '\\resumeSubHeadingListStart\n'
    for item in section['items']:
        if 'years' in item:
            latex_content += '\\resumeSubheadingSimple{' + _rhs(item['title']) + '}{' + item['years'] + '}\n'
        else:
            latex_content += '\\resumeSubheadingVerySimple{' + _rhs(item['title']) + '}'
    latex_content += '\\resumeSubHeadingListEnd\n'
    return latex_content

def generate_latex_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    latex_content = ""
    for section in data['sections']:
        if not section['show_in_cv']:
            continue
        latex_content += '\\section{' + section['title'] + '}\n'
        
        section_format = section['format']
        match section_format:
            case 'paragraph':
                latex_content += generate_paragraph_section(section)
            case 'organization':
                latex_content += generate_organization_section(section)
            case 'publication':
                latex_content += generate_publication_section(section)
            case 'simple':
                latex_content += generate_simple_section(section)
            case _:
                exit(1)
        
        latex_content += '\\vspace{-10pt}\n\n'
    
    return latex_content

def main():
    json_file = 'info/me.json'
    latex_output = generate_latex_from_json(json_file)
    
    with open('cv/info.tex', 'w') as f:
        f.write(latex_output)

if __name__ == "__main__":
    main()
