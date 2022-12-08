import os
import sys
from datetime import datetime
from glob import glob
from re import split

from numpy import asarray, savetxt


class iGrav:
    # find all the .tsf inside the input directory (even in the sub directory)
    def get_all_tfs(self, input_folder):
        paths_list = glob(input_folder + "/**/*.tsf", recursive=True)
        if len(paths_list) <= 0:
            print("[ERROR]: There's no .tsf file")
            sys.exit()
        else:
            return paths_list

    # from a .tsf file get the header with channels and units measured by the device
    def get_header(self, path):
        with open(path, "r") as file:
            header = []
            content = file.readlines()
            for i, line in enumerate(content):
                if "[CHANNELS]" in line:  # get all the channels that the device measure
                    start_idx = i + 1
                    end_idx = start_idx
                    while len(content[end_idx]) > 1:
                        channel = split(r":", content[end_idx].strip())[-1]
                        end_idx += 1
                        header.append(channel)
                if "[UNITS]" in line:  # get measure units and add to the header
                    counter = 0
                    header_len = len(header)
                    start_idx = i + 1
                    end_idx = start_idx
                    while len(content[end_idx]) > 1 and counter < header_len:
                        unit = content[end_idx].strip()
                        header[counter] = f"{header[counter]} ({unit})"
                        counter += 1
                        end_idx += 1
            timestamp = header[-1]
            header.pop(-1)
            header.insert(0, timestamp)

            return header

    # from a .tsf file get only the content without the header
    def get_content(self, path):
        with open(path, "r") as file:
            content = file.readlines()
            for i, line in enumerate(content):
                if "[DATA]" in line:
                    start_idx = i + 1
                    while len(content[start_idx]) <= 1:
                        start_idx += 1
                    return content[start_idx:]

    # process the file and write the content in CSV format in the output file
    def process(self, file_path, output_path):
        output_path = self.get_output_path(file_path, output_path)
        header = self.get_header(file_path)
        self.append_row_in_file(header, output_path)  # add header in the output csv file
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

    # validate each content line and remove the NaN row or the row that dont have a correct datetime
    def data_row_validator(self, row):
        if "\x00" not in row:
            data = split(r"\s{2,}", row.strip())
            if data[0] != "" and data[0] != None:
                try:
                    return data
                except Exception as e:
                    print(f"[ERROR]: Error on formatting date | {e}")
        return None

    # append a array in a file using CSV format with numpy
    def append_row_in_file(self, data, output_file):
        output = asarray([[str(item) for item in data]])
        with open(output_file, "a") as file:
            savetxt(file, output, fmt="%s", delimiter=",", newline="\n")

    #  reformat the datetime in YYYY-MM-DD HH:mm:ss
    def format_datetime(self, string):
        date = string.split(" ")
        return datetime.strptime(f"{'-'.join(date[:3])} {':'.join(date[3:])}", "%Y-%m-%d %H:%M:%S")

    # from the input path and the output path generate the new CSV file path (get only the filename from the input path)
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
        print("[ERROR]: Input or Output path doesn't exist!")


if __name__ == "__main__":
    main()
