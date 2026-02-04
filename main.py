# the software is given a Google Doc that contains a list of Unicode characters and their positions in a 2D grid. it must write a function that takes in the URL for such a Google Doc as an argument, retrieves and parse the data in the document, and prints= the grid of characters.
#
#     The document specifies the Unicode characters in the grid, along with the x- and y-coordinates of each character.
#
#     The minimum possible value of these coordinates is 0. There is no maximum possible value, so the grid can be arbitrarily large.
#
#     Any positions in the grid that do not have a specified character should be filled with a space character.
#
# Note that the coordinates (0, 0) will always correspond to the bottom left corner of the grid as in this example, so make sure to understand in which directions the x- and y-coordinates increase.
#
#     external libraries can be used.
#
#     there should be one function that:
#
#     1. Takes in one argument, which is a string containing the URL for the Google Doc with the input data, AND
#
#     2. When called, prints the grid of characters specified by the input data, displaying a graphic of correctly oriented uppercase letters.

# more performant than requests
import niquests
 
def download_file(url):
    #open up a session
    with niquests.Session() as s:
        #attempt a download
        response = s.get(url)
        #status code 200 is successful
        #only return the text if the status code is 200
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to download. Status code: {response.status_code}")
            return None

if __name__ == '__main__':
    #test0
    download_file("https://docs.google.com/document/u/0/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/export?format=csv")
