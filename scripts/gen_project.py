from jinja2 import Environment, FileSystemLoader
import os


def read_makefile(makefile_path: str):
    CPU = None
    PName = None
    board = None
    sources = []
    includes = []
    fsources = False
    fincludes = False
    with open(makefile_path, 'r') as reader:
        for line in reader.readlines():
            if line.find('CPU =') != -1:
                CPU = line.split('CPU = -mcpu=')[1].split('\n')[0]

            if line.find('TARGET =') != -1:
                PName = line.split('TARGET = ')[1].split('\n')[0]

            if line.find('-DSTM32') != -1:
                board = line.split('-D')[1].split('\n')[0]

            if fsources:
                sources.append(line.split(' ')[0].split('\n')[0])
                if line.find('\\') == -1:
                    fsources = False

            if line.find('C_SOURCES = ') != -1:
                fsources = True

            if fincludes:
                includes.append(line.split(' ')[0].split('\n')[0][2:])
                if line.find('\\') == -1:
                    fincludes = False

            if line.find('C_INCLUDES = ') != -1:
                fincludes = True
    return PName, board, CPU, sources, includes


def generate_file(template_path: str, gen_path: str, context: dict):
    environment = Environment(loader=FileSystemLoader("templates/"))
    results_template = environment.get_template(template_path)
    with open(gen_path, "w") as results:
        results.write(results_template.render(context))
        print(f"... wrote {gen_path}")


if __name__ == '__main__':
    PName = input("Project name: ")
    try:
        os.mkdir(f'{PName}/build')
    except FileExistsError:
        print(f"build folder exist")
    PName, Board, CPU, Sources, Includes = read_makefile(
        '{PName}/Makefile')
    context = {
        'PName': PName,
        'Board': Board,
        'CPU': CPU,
        'Sources': Sources,
        'Includes': Includes
    }

    generate_file('c_cpp_properties.json.j2',
                  '.vscode/c_cpp_properties.json', context)

    generate_file('CMakeLists.txt.j2',
                  f'{PName}/CMakeLists.txt', context)

    generate_file('launch.json.j2',
                  '.vscode/launch.json', context)

    generate_file('tasks.json.j2',
                  '.vscode/tasks.json', context)
