import toml

def get_requirements_list(): 
    requirements = []
    data = open("./requirements.txt", "r").read()
    lines = data.split("\n")
    deps = []
    for i in range(len(lines)):
        line = lines[i]
        if line == "": 
            continue
        tokens = line.split("==")
        newline = tokens[0] + " == " + tokens[1]
        deps.append(newline)
    return deps

data = toml.load("pyproject.dev.toml")
data['project']['dependencies'] = get_requirements_list() 

contents = toml.dumps(data)

open("pyproject.toml", "w").write(contents)