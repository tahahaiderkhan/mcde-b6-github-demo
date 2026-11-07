# Task 03 | Recursive JSON Path Explorer

def find_paths(data, target):

    result = []

    def search(value, path):

        if type(value) == dict:

            for key in value:
                new_path = key if path == "" else path + "." + key
                search(value[key], new_path)

        elif type(value) == list:

            for i in range(len(value)):
                new_path = path + "[" + str(i) + "]"
                search(value[i], new_path)

        else:

            if type(value) == type(target) and value == target:
                result.append(path)

    search(data, "")

    return result


data = {
    "a": [
        {"x": 5},
        5
    ],
    "b": {
        "y": 5
    }
}

print(find_paths(data, 5))
