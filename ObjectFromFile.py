from Object import Object

def GetObjectFromFile(filePath, color):
    vertexes = []
    name = filePath.split('/')[-1].split('.')[0]
    with open(filePath, 'r') as file:
        for line in file:
            if (line.startswith('v ')):
                split = line.split(' ')[1:]
                if len(split) > 2: return None

                x, y = split[0], split[1]
                vertexes.append((float(x), float(y)))
    
    return Object(name, vertexes, [], color)