from Data_manager import DataManager


def sku_nums(data_manager, strength_threshold):
    header = data_manager.data[0]
    strength_index = header.index('StrengthFactor')
    filtered_data = [row for row in data_manager.data[1:] if float(row[strength_index]) > strength_threshold]
    sku_numbers = [int(row[header.index('SKU_number')]) for row in filtered_data]
    return sku_numbers


if __name__ == "__main__":
    data_manager = DataManager(r'C:\Users\gurra\Downloads\cleaned_SalesKaggle3.csv')
    strength_threshold = 1000.0  # Use a float threshold
    sku_numbers = sku_nums(data_manager, strength_threshold)
    print("SKU numbers with StrengthFactor greater than {}:".format(strength_threshold))
    print(sku_numbers)