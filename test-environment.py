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
                   #"fractions-add": 2,
                   #"fractions-multiply": 1,
                   ]
    }

    # Primary function to generate pdf's
    generate_sheet(sheet_info)