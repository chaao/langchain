import os

current_path = os.path.dirname(os.path.abspath(__file__))
resource_path = os.path.join(current_path, 'resource')
output_path = os.path.join(current_path, 'output')


def resource(file_name):
    return os.path.join(resource_path, file_name)


def output(file_name):
    return os.path.join(output_path, file_name)
