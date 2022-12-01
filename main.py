import os
import sys
from datetime import datetime
from glob import glob
from re import split

from numpy import asarray, savetxt


class iGrav:
    def get_all_tfs(self, input_folder):
        paths_list = glob(input_folder + "/**/*.tsf", recursive=True)
        if len(paths_list) <= 0:
            print("There's no .tsf file")
            sys.exit()
        else:
            return paths_list

    def get_content(self, path):
        with open(path, "r") as file:
            content = file.readlines()
            for i, line in enumerate(content):
                if "[DATA]" in line:
                    start_idx = i + 1
                    while len(content[start_idx]) <= 1:
                        start_idx += 1
                    return content[start_idx:]

    def process(self, file_path, output_path):
        output_path = self.get_output_path(file_path, output_path)
        content = self.get_content(file_path)
        last_dt = None
        for line in content:
            data = self.data_row_validator(line)
            if data != None:
                date = self.format_datetime(data[0])
                columns = data[1:]
                if last_dt is None or (last_dt is not None and (last_dt - date).total_seconds() <= -1):
                    last_dt = date
                    self.append_row_in_file([date, *columns], output_path)

    def data_row_validator(self, row):
        if "\x00" not in row:
            data = split(r"\s{2,}", row.strip())
            if data[0] != "" and data[0] != None:
                try:
                    return data
                except Exception as e:
                    print(f"{e} | [data_row_validator]: Date formatting error")
        return None

    def append_row_in_file(self, data, output_file):
        output = asarray([[str(item) for item in data]])
        with open(output_file, "a") as file:
            savetxt(file, output, fmt="%s", delimiter=",", newline="\n")

    def format_datetime(self, string):
        date = string.split(" ")
        return datetime.strptime(f"{'-'.join(date[:3])} {':'.join(date[3:])}", "%Y-%m-%d %H:%M:%S")

    def get_output_path(self, input_path, output_path):
        output = output_path
        if not output.endswith(os.path.sep):
            output += os.path.sep
        file_name = os.path.basename(input_path).split(".")[0]
        return f"{output}/{file_name}.csv"


def main():
    igrav = iGrav()
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    if os.path.exists(input_path) and os.path.exists(output_path):
        file_list = igrav.get_all_tfs(input_path)
        for path in file_list:
            igrav.process(path, output_path)
    else:
        print("[Error]: Input or Output path doesn't exist!")


if __name__ == "__main__":
    main()
