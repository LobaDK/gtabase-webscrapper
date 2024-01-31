import requests
import re
import random
from bs4 import BeautifulSoup

url = "https://www.gtabase.com/user/lobadk"

# Send a GET request to the URL
response = requests.get(url)

if response.ok:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Create a list of all the elements we want to scrape
    elements = soup.select('li.field-entry.my-property-location, li.field-entry.full-width.grid.cols-5.align-left .item-info, li.field-entry.full-width.subfields-block.unstyled .field-value .item-info')

    property_and_cars = {}
    current_location = None

    # If there are no elements, there are no cars or properties
    if len(elements) == 0:
        print("No cars or properties found.")
        input("\nPress Enter to exit...")
        exit()
    # Else, iterate over the elements
    else:
        for element in elements:
            # If the element has the class 'my-property-location' or 'subfields-block', it's a location
            if 'my-property-location' in element['class'] or 'subfields-block' in element['class']:
                # This is a location
                location_data = re.sub('\n+', '\n', element.text.replace('\r', '').replace('\t', '')).strip().split('\n')  # Remove duplciate newlines, and all carriage returns, and tabs, then split on newlines
                # If the first item contains a '$', we know it's the name of the location, and remove it's price
                if '$' in location_data[0]:
                    location_data = [location_data[0].split('$')[0]]
                # If there's only one item, it's the name of the location
                if len(location_data) == 1:
                    current_location = location_data[0]
                else:
                    current_location = location_data[1]
                property_and_cars[current_location] = []
            # Else, it's a car
            else:
                car = element.text.strip()
                if current_location is not None:
                    property_and_cars[current_location].append(car)

        # Now property_and_cars is a dictionary where the keys are the locations (apartment/garage)
        # and the values are lists of cars corresponding to each location

        # Rempve empty locations
        property_and_cars = {k: v for k, v in property_and_cars.items() if v}

        if 'Pegasus Vehicles Storage' in property_and_cars.keys():
            del property_and_cars['Pegasus Vehicles Storage']
        if 'Galaxy Super Yacht The Aquarius Yacht' in property_and_cars.keys():
            del property_and_cars['Galaxy Super Yacht The Aquarius Yacht']
        if 'Large Vehicle Property Kosatka Submarine' in property_and_cars.keys():
            del property_and_cars['Large Vehicle Property Kosatka Submarine']
        if 'Large Vehicle Property Acid Lab (The Freakshop)' in property_and_cars.keys():
            del property_and_cars['Large Vehicle Property Acid Lab (The Freakshop)']

        # Enter infinite loop
        while True:
            # Select a random location
            location = random.choice(list(property_and_cars.keys()))

            # Select a random car from that location
            car = random.choice(property_and_cars[location])

            # Print the result
            print(f"\nLocation: {location}\nCar: {car}")

            input("\nPress Enter to pick a new car, or Ctrl+C to exit...")
