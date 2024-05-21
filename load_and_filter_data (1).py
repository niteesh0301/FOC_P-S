import csv

input_file = r'C:\Users\gurra\Downloads\SalesKaggle3.csv'
output_file = r'C:\Users\gurra\Downloads\cleaned_SalesKaggle3.csv'

columns_to_remove = ['Order', 'File_Type','ReleaseNumber','MarketingType']

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames

    filtered_fieldnames = [i for i in fieldnames if i not in columns_to_remove]

    writer = csv.DictWriter(outfile, fieldnames=filtered_fieldnames)
    writer.writeheader()

    for row in reader:
        filtered_row = {fieldname: row[fieldname] for fieldname in filtered_fieldnames}
        writer.writerow(filtered_row)

print(f"Columns removed and filtered dataset saved to '{output_file}'.")


