import instaloader
import json
import schedule
import time
from datetime import datetime, timedelta

# Initialize Instaloader
L = instaloader.Instaloader()
# Load the saved session (replace 'your_username' with your Instagram username)
L.load_session_from_file('official.meetz')

# profiles go here
profiles = ["houston_carmeets", "coffeeandcars"]

# Define the time range (1 days ago)
days_to_scrape = 1
cutoff_date = datetime.now() - timedelta(days=days_to_scrape)

# Data storage for map markers
posts_data = []

# Iterate through each profile
def scrape_profiles():
    for username in profiles: 
        print(f"Fetching posts from: {username}")
        profile = instaloader.Profile.from_username(L.context, username)

        # Get the timestamp of the last post pulled for each profile
        timestamp_file = f"last_timestamp_{username}.txt"
        try:
            with open(timestamp_file, "r") as file: 
                last_timestamp = datetime.fromisoformat(file.read().strip())
        except FileNotFoundError:
            last_timestamp = datetime.min # Pull everything if no timestamp is stored

        # Fetch the latest posts for the current profile
        for post in profile.get_posts():
            if len(posts_data) >= 3: # Example: limit to 3 post per profile for testing
                break

                
            if post.date >= cutoff_date:
                    if post.date > last_timestamp: 
                        try:
                            location = post.location.name if post.location else "Unknown"
                        except KeyError:
                            location = "Unknown"

                    # Extract details you want
                    post_data = {
                        "username": username,
                        "date": post.date.isoformat(),
                        "caption": post.caption,
                        "location": location
                    }
                    posts_data.append(post_data)

                    print(f"Post from {username} on {post.date}: {post.caption}, Location: {location}")

                    # Save the timestamp of the latest post processed
                    with open(timestamp_file, "w") as file:
                        file.write(post.date.isoformat())
        
            # Sleep between profiles to avoid rate limiting
            time.sleep(60)
            
        # Write posts data to a JSON file for later use in mapping 
        with open('posts_data.json', 'w') as json_file:
            json.dump(posts_data, json_file, indent=4)

# Run the scraping function right now 
scrape_profiles()

#  Schedule the scrape funtion to run daily at a specific time
def schedule_scraping():
    schedule.every().day.at("10:00").do(scrape_profiles) # Set to run at 10:00am

    while True:
        schedule.run_pending()
        time.sleep(1) # Sleep to avoid busy waiting
        
# Start the scheduling
if __name__ == "__main__":
    # schedule_scraping()

    pass

        

