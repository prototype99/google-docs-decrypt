import niquests
import pandas as pd
import io

def gdoc_uncrypt(url):
    """
    Downloads a Google Doc,
    parses the table data (x, char, y),
    prints the resulting grid.
    """
    #clean url
    if "/pub" in url:
        #turns out /pub needs no export parameter
        export_url = url
    elif "/edit" in url:
        #TODO: test this
        #i think /edit needs the export parameter
        export_url = url.split("/edit")[0] + "/export?format=html"
    #even less sure about these bits, but will include them for completeness
    elif "?" in url:
        export_url = url + "&format=html"
    else:
        export_url = url + "/export?format=html"

    #now the real action begins
    try:
        #open up a session
        with niquests.Session() as s:
            #attempt to download the document
            response = s.get(
                export_url,
                #it's google, response should be fast
                timeout=10
            )
            #200 is the success code for http requests
            if response.status_code != 200:
                print(f"Error: Could not download document. Status code: {response.status_code}")
                return
            
            html_content = response.text
            #smol deduplication
            html_content_lower = html_content.lower()
            
            #if you're being asked to log in, you're probably trying to use a private doc'
            if "google-signin" in html_content_lower or "log in" in html_content_lower:
                print("Error: Document is private. Please share it with 'Anyone with the link'.")
                return
    except Exception as e:
        print(f"An error occurred during download: {e}")
        return

    #use the popular pandas library to parse the table data
    try:
        # this gets all tables in the document
        tables = pd.read_html(io.StringIO(html_content))
        # we only care about tables
        if not tables:
            print("Error: No table found in the document.")
            return

        # we only care about the first table
        df = tables[0]

        # We expect 3 columns, doc is malformed otherwise
        if df.shape[1] < 3:
            print("Error: Table does not have enough columns (expected at least 3).")
            return
            
        # the header row is always the first row based on provided examples
        header_row_index = 0

        df.columns = df.iloc[header_row_index]
        df = df.drop(
            df.index[:header_row_index + 1]
        )

            
        #set column names, based on given examples order never changes
        df.columns = [
            'x',
            'char',
            'y'
        ]

        # Convert x & y to integers
        df['x'] = pd.to_numeric(df['x'], errors='coerce')
        df['y'] = pd.to_numeric(df['y'], errors='coerce')
        df['x'] = df['x'].astype(int)
        df['y'] = df['y'].astype(int)
        
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return

    # prepare output
    if df.empty:
        print("Error: No valid data found in the table.")
        return

    #size can vary
    max_x = df['x'].max()
    max_y = df['y'].max()
    
    # Initialize grid with spaces
    # Grid is list of rows, each row is a list of characters
    # Height is max_y + 1, Width is max_x + 1
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # Fill the grid
    for _, row in df.iterrows():
        # Coordinates (0,0) is bottom-left.
        # In our grid list, row 0 will be the top row, so we need to flip y
        # top row index = max_y, bottom row index = 0
        grid[row['y']][row['x']] = row['char']

    # Since 0,0 is bottom-left, y increases UPWARDS.
    # We should print from max_y down to 0.
    for y in range(
            max_y,
            -1,
            -1
    ):
        print(
            "".join(
                grid[y]
            )
        )

if __name__ == '__main__':
    # Example URL from the user's file
    gdoc_uncrypt("https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub")
