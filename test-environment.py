from generate_sheet import *

# A basic main function to test things
if __name__ ==  "__main__":

    sheet_info = {
        "name": "John Doe",
        "grade": 6,
        "topics": {"multiplication": 1,
                   "division": 5,
                   #"fractions-add": 2,
                   #"fractions-multiply": 1,
                   }
    }

    # Primary function to generate pdf's
    generate_sheet(sheet_info)