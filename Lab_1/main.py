import os
import tempfile


def external_merge_sort(input_file_path, output_file_path, buffer_size=1000):
    sorted_runs = create_sorted_runs(input_file_path, buffer_size)

    merge_runs(sorted_runs, output_file_path, buffer_size)


def create_sorted_runs(input_file_path, buffer_size):
    sorted_runs = []

    with open(input_file_path, 'r') as input_file:
        while True:
            chunk = input_file.read(buffer_size)
            if not chunk:
                break

            run = sorted(map(int, chunk.split()))
            sorted_runs.append(run)

    return sorted_runs


def merge_runs(sorted_runs, output_file_path, buffer_size):
    with open(output_file_path, 'w') as output_file:
        while len(sorted_runs) > 1:
            new_sorted_runs = []

            for i in range(0, len(sorted_runs), 2):
                if i + 1 < len(sorted_runs):
                    merged_run = merge(sorted_runs[i], sorted_runs[i + 1])
                    new_sorted_runs.append(merged_run)
                else:
                    new_sorted_runs.append(sorted_runs[i])

            sorted_runs = new_sorted_runs

        output_file.write(' '.join(map(str, sorted_runs[0])))


def merge(run1, run2):
    merged_run = []
    i = j = 0

    while i < len(run1) and j < len(run2):
        if run1[i] < run2[j]:
            merged_run.append(run1[i])
            i += 1
        else:
            merged_run.append(run2[j])
            j += 1

    merged_run.extend(run1[i:])
    merged_run.extend(run2[j:])

    return merged_run


array_size = 10000000
random_array = ' '.join(map(str, [i for i in range(array_size)]))
input_file_path = 'input_file.txt'

with open(input_file_path, 'w') as input_file:
    input_file.write(random_array)

output_file_path = 'output_file.txt'
external_merge_sort(input_file_path, output_file_path)

print(f'Sorting completed. Output file: {output_file_path}')
