import re
import sys

def cl_to_py(cobralang_code):
    translations = [
        (r'\bdefine\b', 'def'),
        (r'\boutput\s+"(.*?)"', r'print("\1")'),
        (r'\boutput\s+(.*)', r'print(\1)'),
        (r'\botherwise\b', 'else:'),
        (r'\belse if\b', 'elif'),
        (r'\brepeat (\w+) from (\d+) to (\d+):', r'for \1 in range(\2, \3 + 1):'),
        (r'\bloop while\b', 'while'),
        (r'\bexit\b', 'break'),
        (r'\bskip\b', 'continue'),
        (r'\bgive\b', 'return'),
        (r'\bis greater than\b', '>'),
        (r'\bis less than\b', '<'),
        (r'\bis equal to\b', '=='),
        (r'\bis not equal to\b', '!='),
        (r'\bis at least\b', '>='),
        (r'\bis at most\b', '<='),
        (r'\bwithin\b', 'in'),
        (r'\badd\b', '+'),
        (r'\bsubtract\b', '-'),
        (r'\bmultiply\b', '*'),
        (r'\bdivide\b', '/'),
        (r'\binteger divide\b', '//'),
        (r'\bmodulus\b', '%'),
        (r'\bpower\b', '**'),
        (r'\bbecomes\b', '='),
        (r'\btrue\b', 'True'),
        (r'\bfalse\b', 'False'),
        (r'\bnothing\b', 'None'),
    ]

    lines = cobralang_code.splitlines()
    translated_lines = []

    for line in lines:
        translated_line = line
        for pattern, replacement in translations:
            translated_line = re.sub(pattern, replacement, translated_line)
        translated_lines.append(translated_line)

    return '\n'.join(translated_lines)

def translate(file_path, debug=False):
    with open(file_path, 'r') as file:
        cobralang_code = file.read()

    translated_code = cl_to_py(cobralang_code)
    if debug:
        print("Translated Python Code:")
        print(translated_code)
    exec(translated_code)

if __name__ == "__main__":
    try:
        translate(sys.argv[1])
    except:
        sys.exit("Usage: python transl.py <file_name>")