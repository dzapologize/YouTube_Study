# conding=utf8
import os
import pysrt

g = os.walk(
    "/Users/cairang/Downloads/Udemy - Java Puzzles to Eliminate Code Fear 2021-5"
)

for path, dir_list, file_list in g:
    for file_name in file_list:
        if(file_name.endswith('en.srt')):
            print(os.path.join(path, file_name))


