import json

# Load the JSON file
file_path = 'C:/Users/sarah/Documents/GinkoGreenAI/data/YTB/history/watch-history.json'
with open(file_path, 'r', encoding='utf-8') as file:
  data = json.load(file)

# Filter out blocks with header "YouTube Music"
filtered_data = [entry for entry in data if entry.get('header') == "YouTube Music"]

# Save the filtered data back to a new JSON file
output_path = 'C:/Users/sarah/Documents/GinkoGreenAI/data/YTB/history/filtered-watch-history.json'
with open(output_path, 'w', encoding='utf-8') as output_file:
  json.dump(filtered_data, output_file, ensure_ascii=False, indent=4)

#   Issues with YouTube Music
# YouTube Music has no way to export your history. The only way you can is by going to takeout.google.com and exporting your comined Youtube AND YouTube Music data. Luckily, all YouTube Music entries are flagged with a header, so the file is easy to parse.

# Given that YouTube Music is just a fancy UI for watching YouTube Videos, not all of the entries are actual songs, this means I couldn't include all YTM results, as random one-off remixes and other songs uploaded by single people would be included. 
# I found that every song officially published was published under the "Artist Name - Topic" format (Ex: Kanye West - Topic) the inputted file is filtered to only include songs from these topic artists, meaning they all are "official" songs.