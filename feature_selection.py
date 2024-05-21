import json


class DataManager:
    def __init__(self, csv_file):
        self.data = []
        self.load_data(csv_file)

    def load_data(self, csv_file):
        with open(csv_file, 'r', newline='') as file:
            lines = file.readlines()
            header = lines[0].strip().split(',')
            self.data.append(header)
            for line in lines[1:]:
                self.data.append(line.strip().split(','))

    def display_table(self):
        for row in self.data:
            print("\t".join(row))

    def sort_data(self, column_name):
        header = self.data[0]
        data = self.data[1:]
        column_index = header.index(column_name)
        data.sort(key=lambda x: x[column_index])
        self.data = [header] + data

    def filter_data(self, column_name, condition):
        header = self.data[0]
        data = self.data[1:]
        column_index = header.index(column_name)
        filtered_data = [header] + [row for row in data if row[column_index] == condition]
        self.data = filtered_data

    def save_to_json(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)


if __name__ == "__main__":
    data_manager = DataManager(r'C:\Users\gurra\Downloads\cleaned_SalesKaggle3.csv')

    print("Original Data:")
    data_manager.display_table()

    data_manager.sort_by_column('StrengthFactor')
    print("\nData Sorted by StrengthFactor:")
    data_manager.display_table()

    data_manager.filter_by_condition('SoldFlag', '1')
    print("\nData Filtered by SoldFlag = 1:")
    data_manager.display_table()
