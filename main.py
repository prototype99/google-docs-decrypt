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
    else:
        export_url = f"{url.rstrip('/')}/export?format=html" if "?" not in url else f"{url}&format=html"

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
            
            #if you're being asked to log in, you're probably trying to use a private doc
            if any(
                    marker in response.text.lower() for marker in [
                        "google-signin",
                        "log in"
                    ]
            ):
                print("Error: Document is private. Please share it with 'Anyone with the link'.")
                return
    except Exception as e:
        print(f"An error occurred during download: {e}")
        return

    # Parse table data
    try:
        # Read the table data from the HTML
        tables = pd.read_html(
            io.StringIO(
                response.text
            )
        )
        if not tables:
            print("Error: No table found in the document.")
            return

        #we only care about the first table & we don't need the header row
        df = tables[0].iloc[1:]
        df.columns = [
            'x',
            'char',
            'y'
        ]

        # Convert coordinates to integers
        df[['x', 'y']] = df[['x', 'y']].apply(pd.to_numeric, errors='coerce').astype(int)
        
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return

    # Initialize grid and fill it
    max_x, max_y = df['x'].max(), df['y'].max()
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
