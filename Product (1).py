class Product:
    def __init__(self, csv_line):
        values = csv_line.strip().split(',')

        self.Order = int(values[0])
        self.File_Type = values[1]
        self.SKU_number = int(values[2])
        self.SoldFlag = int(values[3])
        self.SoldCount = int(values[4])
        self.MarketingType = values[5]
        self.ReleaseNumber = int(values[6])
        self.New_Release_Flag = int(values[7])
        self.StrengthFactor = int(values[8])
        self.PriceReg = float(values[9])
        self.ReleaseYear = int(values[10])
        self.ItemCount = int(values[11])
        self.LowUserPrice = float(values[12])
        self.LowNetPrice = float(values[13])

    def __str__(self):
        return f"SKU: {self.SKU_number}, Sold: {self.SoldFlag}, Price: {self.PriceReg}"

