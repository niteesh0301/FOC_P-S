from Data_manager import DataManager
import json
import pickle

if __name__ == "__main__":
    data_manager = DataManager(r'C:\Users\gurra\Downloads\cleaned_SalesKaggle3.csv')

    # Save filtered and sorted data to JSON
    data_manager.filter_data('SoldFlag', '1')
    data_manager.save_to_json('filtered_data.json')
    data_manager.sort_data('StrengthFactor')
    data_manager.save_to_json('sorted_data.json')

    # Load saved JSON data
    with open('filtered_data.json', 'r') as json_file:
        loaded_data = json.load(json_file)
        # print("Loaded JSON Data:")
        # print(loaded_data)

    # Create and save a Product object using pickle
    product = {'SKU_number': 12345, 'SoldFlag': 1, 'StrengthFactor': 1500.0, 'PriceReg': 49.99}
    with open('product.pkl', 'wb') as pickle_file:
        pickle.dump(product, pickle_file)

    # Load and display the saved Product object
    with open('product.pkl', 'rb') as pickle_file:
        loaded_product = pickle.load(pickle_file)
        # print("Loaded Product:")
        # print(loaded_product)
