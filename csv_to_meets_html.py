import csv
import os
import re
import random

def csv_to_html(csv_filename, output_folder):
    # Derive the HTML filename by replacing the CSV extension with '.html' in the meets folder.
    html_filename = os.path.join(output_folder, os.path.splitext(os.path.basename(csv_filename))[0] + '.html')

    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        # Ensure there are at least 5 rows for valid HTML generation.
        if len(rows) < 5:
            print("CSV file must have at least 5 rows.")
            return

        # Extract values from the first five rows.
        link_text = rows[0][0]
        h2_text = rows[1][0]
        link_url = rows[2][0]
        summary_text = rows[3][0]

        # Dictionary to map athlete names to their IDs for linking
        athletes_dict = {}
        
        # Start initializing HTML content.
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{link_text}</title>
<link rel="stylesheet" href="../css/reset.css">
<link rel="stylesheet" href="../css/style.css">
</head>
   <body>
   <a href="#main" id="skip">Skip to Main Content</a>
   <nav>
        <a href="../index.html">Home Page</a>
        <a href="#summary">Summary</a>
        <a href="#team-results">Team Results</a>
        <a href="#individual-results">Individual Results</a>
        <a href="#gallery">Gallery</a>
   </nav>
   <header>
      <!--Meet Info -->
        <h1 id="meettitle"><a href="{link_url}">{link_text}</a></h1>
        <h2 id="meetdate">{h2_text}</h2>
</header>
   <main id="main">
    <section class="summary" id="summary">
      <h2>Race Summary</h2>
      {summary_text}
    </section>
"""

        # Start container for team results
        html_content += """<section id="team-results">\n
        <h2>Team Results</h2>"""

        # Process the remaining rows (after the first five)
        html_content += """<table>\n"""
        table_start = True

        for row in rows[4:]:
            # For rows that are 3 columns wide, add to the team places list
            if len(row) == 3:
                if row[0] == "Place":
                    html_content += f"<tr><th>{row[0]}</th><th>{row[1]}</th><th>{row[2]}</th></tr>\n"
                else:
                  # Replace place 1, 2, and 3 with the appropriate classes
                    place = int(row[0])
                    if place == 1:
                        place_html = '<td class="first-place"></td>'
                    elif place == 2:
                        place_html = '<td class="second-place"></td>'
                    elif place == 3:
                        place_html = '<td class="third-place"></td>'
                    else:
                        place_html = f'<td>{row[0]}</td>'

                    html_content += f"<tr>{place_html}<td>{row[1]}</td><td>{row[2]}</td></tr>\n"

            # For rows that are 8 columns wide and contain 'Ann Arbor Skyline' in column 6
            elif len(row) == 8 and row[5].strip().lower() == 'ann arbor skyline':
                if table_start == True:
                    table_start = False
                    html_content += "</table>\n"
                    html_content += """</section>\n
                    <section id="individual-results">\n
                    <h2>Individual Results</h2>"""

                place = row[0].replace('.', ' ')  # Remove dot from the place number
                grade = row[1]
                name = row[2]
                time = row[4]
                profile_pic = row[7]

                # Use the athlete's name as the ID
                athlete_id = name.replace(" ", "_")

                # Add the athlete details to the dictionary
                athletes_dict[name] = athlete_id

                # Add the athlete div with the ID
                html_content += f"""
<div class="athlete" id="{athlete_id}">
<figure> 
    <img src="../images/profiles/{profile_pic}" width="200" alt="Profile picture of {name}"> 
    <figcaption>{name}</figcaption>
</figure>
<dl>
    <dt>Place</dt><dd> {place}</dd>
    <dt>Time</dt><dd> {time}</dd>
    <dt>Grade</dt><dd> {grade}</dd>
</dl>
</div>
"""

        # Create athlete links within the summary text and spans with class "athlete"
        for athlete, athlete_id in athletes_dict.items():
            athlete_link = f'<a href="#{athlete_id}">{athlete}</a>'
            summary_text = re.sub(rf'\b{athlete}\b', athlete_link, summary_text)
            summary_text = re.sub(rf'<span class=["\']athlete["\']>{athlete}</span>', athlete_link, summary_text)

        # Update the summary section with the linked text
        html_content = html_content.replace("{summary_text}", summary_text)

        html_content += """</section>\n
        <section id="gallery">
        <h2>Gallery</h2>
        """

        html_content += create_meet_image_gallery(link_url)
        # Close the HTML document
        html_content += """
   </section>
   </main>   
   <footer>
                     <p>
                     Skyline High School<br>
                     <address>
                     2552 North Maple Road<br>
                     Ann Arbor, MI 48103<br><br>
                    </address>
                     <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
                    Follow us on Instagram <a href="https://www.instagram.com/a2skylinexc/" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a> 
                     </footer>
                     <script src="../js/imagePlaceholder.js"></script>
        </body>
</html>
"""
        html_content = re.sub(r'<time>', '<span class="time">', html_content)
        html_content = re.sub(r'</time>', '</span>', html_content)

        # Save HTML content to a file in the meets folder
        with open(html_filename, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_content)

        print(f"HTML file '{html_filename}' created successfully.")

def process_meet_files():
    # Set the meets folder path
    meets_folder = os.path.join(os.getcwd(), "meets")
    
    # Search for all CSV files in the meets folder
    csv_files = [f for f in os.listdir(meets_folder) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in folder: {meets_folder}")
        return

    # Process each CSV file in the meets folder
    for csv_file in csv_files:
        csv_file_path = os.path.join(meets_folder, csv_file)
        csv_to_html(csv_file_path, meets_folder)

# Step 1: Extract the meet ID from the URL
def extract_meet_id(url):
    # Regex to extract the meet ID, which is the number right after '/meet/'
    match = re.search(r"/meet/(\d+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Meet ID not found in URL.")

# Step 2: Select 12 random photos from the folder
def select_random_photos(folder_path, num_photos=25):
    # List all files in the folder
    all_files = os.listdir(folder_path)
    # Filter out non-image files if necessary (assuming .jpg, .png, etc.)
    image_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    # Ensure we have enough images to select
    if len(image_files) < num_photos:
        return ""
    
    # Select 12 random images
    return random.sample(image_files, num_photos)

# Step 3: Generate HTML image tags
def generate_image_tags(image_files, folder_path):
    img_tags = []
    for img in image_files:
        img_path = os.path.join(folder_path, img)
        img_tags.append(f'<img src="../{img_path}" width = "200" alt="">')
    return "\n".join(img_tags)

# Putting it all together
def create_meet_image_gallery(url):
    meet_id = extract_meet_id(url)
    # Define the folder path for images based on the meet ID
    folder_path = f'images/{meet_id}/'
    print(meet_id)
    
    if not os.path.exists(folder_path):
        return ""
    
    # Select 12 random photos
    selected_photos = select_random_photos(folder_path)
    
    # Generate image tags
    html_image_tags = generate_image_tags(selected_photos, folder_path)
    
    return html_image_tags

# Example usage
url = "https://www.athletic.net/CrossCountry/meet/235827/results/943367"
html_gallery = create_meet_image_gallery(url)
print(html_gallery)

if __name__ == "__main__":
    # Check if meets folder exists
    meets_folder = os.path.join(os.getcwd(), "meets")
    if not os.path.exists(meets_folder):
        print(f"Folder '{meets_folder}' does not exist.")
    else:
        process_meet_files()