from generate_sheet import *


# A basic main function to test things
if __name__ ==  "__main__":

    sheet_info = {
        "name": "Jaime Selwyn",
        "grade": 6,
        "topics": [(Multiply, 8),
                   (Divide, 8),
                   (FractionAdd, 8),
                   (FractionSubtract, 8),
                   (FractionMultiply, 8)
                   ]
    }

    # Primary function to generate PDFs
    generate_sheet(sheet_info)