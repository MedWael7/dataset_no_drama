#!/usr/bin/env python3
"""
Simple script to generate 750k negative hotel reviews dataset
Split into multiple JSON files for GitHub upload
"""

import json
import random
import os
import math
from datetime import datetime

class HotelReviewDatasetGenerator:
    def __init__(self):
        # Comprehensive aspect mapping with synonyms and variations
        self.aspect_mappings = {
            "rooms": ["rooms", "room", "suite", "accommodation", "quarters", "small room", "tiny room", "cramped room", "compact room"],
            "bathrooms": ["bathrooms", "bathroom", "restroom", "wc", "toilet", "washroom", "lavatory"],
            "shower": ["shower", "showers", "bathtub", "bath", "tub"],
            "bed": ["bed", "beds", "mattress", "bedding", "sleeping area"],
            "carpet": ["carpet", "carpets", "flooring", "floor", "rug", "rugs"],
            "pillows": ["pillows", "pillow", "cushions", "headrest"],
            "blankets": ["blankets", "blanket", "covers", "bedding", "comforter", "duvet"],
            "wifi": ["wifi", "wi-fi", "internet", "wireless", "connection", "network"],
            "elevator": ["elevator", "elevators", "lift", "lifts"],
            "breakfast": ["breakfast", "morning meal", "buffet", "continental breakfast"],
            "restaurant": ["restaurant", "dining", "dining room", "eatery", "cafe"],
            "lobby": ["lobby", "reception area", "entrance", "foyer", "main hall"],
            "staff": ["staff", "employees", "personnel", "workers", "team", "crew"],
            "service": ["service", "customer service", "hospitality", "assistance"],
            "cleaning": ["cleaning", "housekeeping", "maintenance", "upkeep", "sanitation"],
            "air_conditioning": ["air conditioning", "air con", "ac", "cooling", "climate control", "hvac"],
            "bar": ["bar", "lounge", "pub", "cocktail bar", "drinks area"],
            "minibars": ["minibar", "mini bar", "in-room bar", "fridge"],
            "food": ["food", "meals", "cuisine", "dining", "menu"],
            "pizza": ["pizza", "pizzas", "italian food"],
            "drinks": ["drinks", "beverages", "cocktails", "alcohol"],
            "juice": ["juice", "juices", "fresh juice", "fruit juice"],
            "guide": ["guide", "tour guide", "concierge", "information"],
            "transport": ["transport", "transportation", "shuttle", "taxi", "transfer"],
            "price": ["price", "cost", "rate", "pricing", "fees"],
            "expensiveness": ["expensive", "overpriced", "costly", "pricey", "charges"],
            "kettle": ["kettle", "coffee maker", "tea maker", "hot water"],
            "pool": ["pool", "swimming pool", "spa", "jacuzzi", "hot tub"],
            "stairs": ["stairs", "staircase", "steps", "stairway"],
            "reception": ["reception", "front desk", "check-in", "desk", "counter"],
            "view": ["view", "scenery", "outlook", "window view", "vista"],
            "extra_charges": ["extra charges", "hidden fees", "additional costs", "surcharges"],
            "extra_fees": ["extra fees", "additional fees", "hidden charges", "supplements"],
            "water": ["water", "hot water", "water pressure", "plumbing"],
            "temperature": ["temperature", "heating", "warmth", "cold", "hot"],
            "tv": ["tv", "television", "tv set", "entertainment", "cable"],
            "gym": ["gym", "fitness center", "exercise room", "workout area"],
            "fitness": ["fitness", "fitness facilities", "exercise equipment", "weights"],
            "window": ["window", "windows", "glass", "view"],
            "smoke": ["smoke", "smoking", "cigarette smell", "odor"],
            "smell": ["smell", "odor", "scent", "aroma", "stench"],
            "hair": ["hair", "hairs", "dirty hair", "previous guest hair"],
            "breakfast": ["breakfast", "morning meal", "buffet", "continental breakfast"],
            "bugs": ["bugs", "insects", "pests", "cockroaches", "ants"],
            "coffee": ["coffee", "espresso", "cappuccino", "coffee machine"],
            "tea": ["tea", "herbal tea", "tea bags", "tea service"],
            "alcohol": ["alcohol", "wine", "beer", "spirits", "liquor"],
            "towels": ["towels", "towel", "bath towels", "linens"],
            "parking": ["parking", "parking lot", "valet", "garage"],
            "housekeeping": ["housekeeping", "room service", "cleaning service", "maid service"],
            "noise": ["noise", "loud", "sounds", "disturbance", "racket"]
        }
        
        # Problem templates for each aspect category - REALISTIC like actual booking.com reviews
        self.problem_templates = {
            "rooms": [
                "was very small", "was quite small for the price", "was really small", "was a bit small",
                "was smaller than expected", "was too small", "felt cramped", "not much space",
                "very basic compared to other hotels", "was old and dated", "needs updating",
                "was not what we asked for", "furniture felt crammed in", "no storage space",
                "was hot even when set at lowest temp", "was very cold", "needs a modern upgrade"
            ],
            "bathrooms": [
                "was quite small", "no privacy at all", "door doesn't close properly", "very small",
                "had no bath", "drain was not functioning well", "needs updating", "was old",
                "door doesn't lock", "very basic", "needs money spending on this",
                "could do with updating", "plumbing could do with updating"
            ],
            "shower": [
                "had poor water pressure", "lack of water pressure", "drain was blocked",
                "was too small", "plumbing could do with updating", "needs updating",
                "pressure was poor", "was very small", "drain not working properly"
            ],
            "bed": [
                "was not comfy", "was a bit hard", "was quite hard", "wasn't the most comfortable",
                "was two singles pushed together", "had a gap in the centre", "was small and bit hard",
                "was not comfortable", "was too small", "mattress was hard", "was uncomfortable"
            ],
            "carpet": [
                "was a bit tatty", "was very worn", "in the hallway was very worn", "was dirty",
                "was old and dirty", "needs replacing", "was worn through", "was stained"
            ],
            "pillows": [
                "were too small", "were not comfortable", "were quite hard", "were flat",
                "only one provided", "were old", "were uncomfortable"
            ],
            "blankets": [
                "were thin", "were not warm enough", "were old", "didn't cover the bed properly",
                "were uncomfortable", "were too small"
            ],
            "wifi": [
                "was very slow", "didn't work in the room", "sucks", "was poor",
                "no free wifi in the room", "not available in rooms", "was terrible",
                "keeps disconnecting", "signal was weak", "was unreliable"
            ],
            "elevator": [
                "was quite small", "was very small", "was slow", "only one working",
                "was out of order", "barely room for two people", "was too small"
            ],
            "breakfast": [
                "was expensive", "was disappointing", "was not very good", "was ok but not excellent",
                "could be included", "variety was poor", "quality was not good", "was overpriced",
                "room was quite small", "limited options", "same options every day"
            ],
            "restaurant": [
                "was ok but not excellent", "service made several mistakes", "was average",
                "food was ok for the price", "had slow service", "staff need to keep regular hours",
                "no food available after 4pm", "was closed when needed"
            ],
            "lobby": [
                "was quite small", "was old and dated", "needs updating", "was run down",
                "was crowded", "no seating available"
            ],
            "staff": [
                "was poor", "was rude and unfriendly", "was unhelpful", "couldn't find my booking",
                "was non cooperative", "had poor attitude", "ignored us", "was unfriendly",
                "manner was impolite", "one grumpy lady", "need better training", "was rude"
            ],
            "service": [
                "made several mistakes", "was poor", "was slow", "was disappointing",
                "could be better", "was not helpful", "needs improvement"
            ],
            "cleaning": [
                "was poor", "room wasn't cleaned", "missed areas", "was not thorough",
                "needs improvement", "housekeeping didn't come"
            ],
            "air_conditioning": [
                "didn't work", "was not good enough", "was too noisy", "couldn't control temperature",
                "was probably broken", "kept starting in the night", "was very drying",
                "couldn't make it stop", "remote didn't work", "wasn't working properly"
            ],
            "bar": [
                "no wine available", "was expensive", "room fridge not working", "limited selection",
                "9 pounds for a glass of wine", "overpriced drinks", "closed early"
            ],
            "minibars": [
                "not restocked daily", "was empty", "no minibar available", "didn't work",
                "no water available", "items were expensive"
            ],
            "food": [
                "was ok but not more than average", "choice was limited", "was disappointing",
                "quality was poor", "was overpriced", "no variety"
            ],
            "pizza": [
                "was average", "was overpriced", "took too long", "was disappointing"
            ],
            "drinks": [
                "were overpriced", "limited selection", "no wine in the bar", "were expensive"
            ],
            "juice": [
                "was limited", "only basic options", "was expensive", "not fresh"
            ],
            "guide": [
                "was not helpful", "didn't know the area", "was expensive", "poor service"
            ],
            "transport": [
                "taxi was expensive", "was a rip off", "driver didn't know directions",
                "was overpriced", "shuttle was unreliable"
            ],
            "price": [
                "was expensive", "poor value for money", "not worth what we paid",
                "was overpriced", "expensive for what you get"
            ],
            "expensiveness": [
                "everything was expensive", "was overpriced", "poor value", "too expensive"
            ],
            "kettle": [
                "no tea coffee making facilities", "was not working", "was old", "was broken"
            ],
            "pool": [
                "no swimming pool", "was too small", "was closed", "was not clean",
                "hours were limited", "was overcrowded"
            ],
            "stairs": [
                "were steep and narrow", "carpet was worn", "were difficult to access",
                "lighting was poor", "were not safe"
            ],
            "reception": [
                "staff couldn't find booking", "was slow", "couldn't help with early check in",
                "staff was unable to find my booking", "no one picked up phone",
                "computer system was down", "staff ignored us", "checkout was early"
            ],
            "view": [
                "no view from room", "was of a brick wall", "was not nice", "was disappointing",
                "was blocked", "faces main road", "was of parking lot", "room had no view"
            ],
            "extra_charges": [
                "parking was expensive", "hidden fees", "charged for everything",
                "deposit not refunded", "extra costs not mentioned"
            ],
            "extra_fees": [
                "safe box needs payment", "breakfast charged separately", "wifi costs extra",
                "everything costs extra", "hidden charges"
            ],
            "water": [
                "no hot water", "pressure was poor", "was brown", "tasted bad",
                "limited hot water", "kept running out"
            ],
            "temperature": [
                "room was very hot", "was too cold", "couldn't control", "heating didn't work",
                "was uncomfortable", "thermostat didn't work"
            ],
            "tv": [
                "no English channels", "was very small", "was old", "channels were limited",
                "didn't work properly", "was from the 1990s"
            ],
            "gym": [
                "was closed", "equipment was old", "was too small", "limited hours",
                "was not available", "needs updating"
            ],
            "fitness": [
                "equipment was broken", "was not available", "limited facilities",
                "needs updating", "was disappointing"
            ],
            "window": [
                "single glazed", "curtain was damaged", "couldn't open", "was broken",
                "cold air coming through", "needs double glazing"
            ],
            "smoke": [
                "smell in room", "from other rooms", "in hallways", "ventilation poor"
            ],
            "smell": [
                "was unpleasant", "from cooking", "musty odor", "needed better ventilation"
            ],
            "hair": [
                "in bathroom", "on towels", "in drain", "from previous guests"
            ],
            "breakfast": [
                "was expensive", "was disappointing", "limited variety", "quality was poor",
                "room was small", "waiting for tables", "same every day"
            ],
            "bugs": [
                "in the room", "in bathroom", "need pest control", "quite a problem"
            ],
            "coffee": [
                "no facilities in room", "was expensive", "quality was poor", "machine broken"
            ],
            "tea": [
                "no facilities in room", "was expensive", "limited options", "quality poor"
            ],
            "alcohol": [
                "was overpriced", "limited selection", "quality was poor", "bar closed early"
            ],
            "towels": [
                "were old", "were thin", "not enough provided", "were dirty",
                "needed replacing", "were small"
            ],
            "parking": [
                "was expensive", "no spaces available", "was far from hotel",
                "costs more than room", "difficult to find"
            ],
            "housekeeping": [
                "entered without permission", "didn't clean properly", "was poor",
                "didn't come daily", "missed areas"
            ],
            "noise": [
                "from next room", "from outside", "construction work nearby",
                "from main road", "thin walls", "poor soundproofing", "traffic noise",
                "from other guests", "woke us up early"
            ]
        }
        
        # Review structure templates - REALISTIC like actual booking.com reviews  
        self.review_structures = [
            "The {aspect} {problem}",
            "{aspect} {problem}",
            "The {aspect} was {problem}",
            "Really the only thing I can fault was the {aspect} it {problem}",
            "To be really picky the {aspect} {problem}",
            "Would have liked the {aspect} not {problem}",
            "I thought that the {aspect} {problem}",
            "The {aspect} {problem} but not a massive deal",
            "Choice of {aspect}",
            "No {aspect}",
            "{aspect} could be {problem}",
            "Extremely {problem} {aspect}",
            "Sound proofing is poor {aspect} {problem}",
            "Needs {problem} {aspect}",
            "I cannot believe {aspect} {problem}",
            "Calling {aspect} {problem}",
            "Dated {aspect} and {problem}",
            "Didn't realize but {aspect} {problem}",
            "The {aspect} {problem}",
            "Very peculiar {aspect} {problem}",
            "The {aspect} was quite {problem}",
            "Found the {aspect} {problem}",
            "Not a single bad thing except {aspect} {problem}",
            "For sure not {problem} {aspect}",
            "Just the {aspect} {problem}",
            "The first ever hotel with {aspect} {problem}",
            "The {aspect} {problem} well below standard",
            "11:00 is an early {aspect}",
            "Maybe the {aspect} {problem}",
            "Wi Fi {problem}",
            "This should not be {problem}",
            "The only problem we had was {aspect} {problem}",
            "expensive {aspect}",
            "The property is a bit dated with {aspect} {problem}",
            "Asked for {aspect} but got {problem}",
            "Every thing is fine except the {aspect} {problem}",
            "Aircon {problem}",
            "Small {aspect} only but not a big deal",
            "The staff at {aspect} {problem}",
            "BREAKFAST {problem}",
            "Rooms are not very well {problem}",
            "Room was a little {problem}",
            "The neighbourhood {problem}",
            "9 pounds for a {aspect}",
            "Very unfriendly {aspect} {problem}",
            "I still haven't got my {aspect} {problem}",
            "The room was {problem}",
            "Just round the back is {aspect} {problem}",
            "Rooms could be a bit {problem}",
            "For sure not a 4 star hotel the {aspect} {problem}",
            "The first ever hotel I have stayed in with {aspect} {problem}",
            "Just the bare essentials {aspect} {problem}",
            "No {aspect} {problem}",
            "Room was {problem}",
            "The room and {aspect} were {problem}",
            "The lift is quite {problem}",
            "Small {aspect}",
            "Our room was really {problem}",
            "The price of {aspect} {problem}",
            "Harassment on {aspect}",
            "location is a bit {problem}",
            "Small room Small {aspect}",
            "I thought that the {aspect} was a little {problem}",
            "1 {aspect} {problem}",
            "no {aspect} available in the room",
            "Bed was {problem}",
            "Quicker {aspect} {problem}",
            "Bed was a bit {problem}",
            "Small bathroom {aspect} {problem}",
            "One of the booked rooms was very {problem}",
            "Slow service for {aspect}",
            "The property is a bit {problem}",
            "Asked for a double bed but got {aspect} {problem}",
            "Two people on {aspect} {problem}",
            "The {aspect} quality was not good enough",
            "Every thing is fine except the {aspect} {problem}",
            "Small {aspect} only",
            "The staff at the {aspect} {problem}",
            "BREAKFAST NOT VERY {problem}",
            "Room was a little {problem}",
            "The {aspect} is very bad",
            "9 for a glass of {aspect}",
            "Very unfriendly {aspect} {problem}",
            "I still haven't got my {aspect} {problem}",
            "The room was {problem}",
            "Rooms could be a bit {problem}",
            "For sure not a 4 star {aspect} {problem}",
            "No {aspect} {problem}",
            "Just the bare essentials {aspect} {problem}",
            "No {aspect} {problem} facilities in room",
            "Room was {problem}",
            "The {aspect} was awful and {problem}",
            "The lift is quite {problem} Free {aspect} is very {problem}",
            "Small {aspect}",
            "Our room was really {problem}",
            "Bed was {problem} Hassle with {aspect}",
            "Small {aspect} {problem}",
            "The property is a bit {problem} with {aspect} {problem}",
            "Every thing is fine in this hotel except the {aspect} {problem}",
            "Reception {aspect} was {problem}",
            "Small {aspect} only but not a big deal",
            "The {aspect} was {problem}",
            "BREAKFAST {problem}",
            "Rooms are not very well {problem}",
            "The {aspect} is very {problem}"
        ]
    
    def generate_review_text(self, aspects, problems):
        """Generate natural review text like real booking.com reviews"""
        if len(aspects) == 1:
            structure = random.choice(self.review_structures)
            return structure.format(aspect=aspects[0], problem=problems[0])
        else:
            # For multiple aspects, create realistic multi-complaint reviews like real booking sites
            review_parts = []
            
            # Realistic connectors used in actual reviews
            connectors = [
                " ", " The ", " Also ", " Also the ", " ", " Really the only thing ",
                " To be really picky ", " ", " I thought that ", " ", " Would have liked ",
                " ", " No ", " ", " Maybe the ", " ", " Just the ", " "
            ]
            
            # Start with first complaint
            first_structure = random.choice(self.review_structures)
            first_part = first_structure.format(aspect=aspects[0], problem=problems[0])
            review_parts.append(first_part)
            
            # Add remaining complaints with realistic connectors
            for i in range(1, len(aspects)):
                connector = random.choice(connectors)
                # More realistic complaint structures
                complaint_structures = [
                    "{connector}{aspect} {problem}",
                    "{connector}the {aspect} {problem}",
                    "{connector}{aspect} was {problem}",
                    "{connector}{aspect} {problem} but not a big deal"
                ]
                structure = random.choice(complaint_structures)
                part = structure.format(connector=connector, aspect=aspects[i], problem=problems[i])
                review_parts.append(part)
            
            full_review = "".join(review_parts)
            
            # Add realistic but less dramatic endings occasionally
            realistic_endings = [
                " Will not go back here again",
                " but not a massive deal though",
                " Not a big deal but worth mentioning", 
                " Otherwise everything was fine",
                " Apart from that it was ok",
                ""  # Most reviews don't have endings
            ]
            
            if random.random() < 0.15:  # 15% chance of realistic ending
                full_review += random.choice(realistic_endings)
            
            return full_review
    
    def generate_balanced_dataset(self, total_reviews=750000):
        """Generate balanced dataset ensuring all aspects get fair representation"""
        reviews = []
        aspect_count = {key: 0 for key in self.aspect_mappings.keys()}
        target_per_aspect = total_reviews // len(self.aspect_mappings)
        
        print(f"Generating {total_reviews:,} reviews with balanced aspect distribution...")
        print(f"Target per aspect: {target_per_aspect:,}")
        
        for i in range(1, total_reviews + 1):
            # Find aspects that need more representation
            underrepresented = [key for key, count in aspect_count.items() 
                              if count < target_per_aspect]
            
            if underrepresented:
                # Force selection from underrepresented aspects
                aspect_keys = random.sample(underrepresented, 
                                          min(random.randint(1, 3), len(underrepresented)))
            else:
                # Normal random selection
                aspect_keys = random.sample(list(self.aspect_mappings.keys()), 
                                          random.randint(1, 3))
            
            # Update counters
            for key in aspect_keys:
                aspect_count[key] += 1
            
            # Generate review
            display_aspects = [random.choice(self.aspect_mappings[key]) for key in aspect_keys]
            problems = [random.choice(self.problem_templates[key]) for key in aspect_keys]
            
            review_text = self.generate_review_text(display_aspects, problems)
            
            # Ensure review doesn't exceed 60 tokens
            words = review_text.split()
            if len(words) > 60:
                review_text = " ".join(words[:60])
                if not review_text.endswith('.'):
                    review_text += "."
            
            review = {
                "review_id": i,
                "review_text": review_text,
                "aspects": display_aspects,
                "problems": problems
            }
            
            reviews.append(review)
            
            if i % 50000 == 0:
                print(f"Generated {i:,} reviews...")
        
        print("Final aspect distribution:")
        for key, count in sorted(aspect_count.items()):
            print(f"  {key}: {count:,}")
        
        return reviews
    
    def split_and_save_dataset(self, reviews, chunk_size=50000, output_dir="dataset_parts"):
        """Split dataset into parts and save as JSON files"""
        os.makedirs(output_dir, exist_ok=True)
        
        total_chunks = math.ceil(len(reviews) / chunk_size)
        file_paths = []
        
        print(f"\nSplitting {len(reviews):,} reviews into {total_chunks} files...")
        
        for i in range(total_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(reviews))
            chunk = reviews[start_idx:end_idx]
            
            filename = f"negative_hotel_reviews_part_{i+1:02d}_of_{total_chunks:02d}.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(chunk, f, indent=2, ensure_ascii=False)
            
            file_paths.append(filepath)
            print(f"  Saved {filename} with {len(chunk):,} reviews")
        
        return file_paths
    
    def generate_readme(self, total_reviews, num_files, output_dir="dataset_parts"):
        """Generate README file for the dataset"""
        readme_content = f"""# Negative Hotel Reviews Dataset

## Overview
This dataset contains {total_reviews:,} negative hotel reviews specifically designed for commercial AI training and analysis.

## Dataset Characteristics
- **Total Reviews**: {total_reviews:,}
- **Format**: JSON
- **Language**: English
- **Review Length**: Maximum 60 tokens per review
- **Balance**: Comprehensive coverage of all hotel aspects with synonyms

## Dataset Structure
Each review contains:
- `review_id`: Unique identifier
- `review_text`: The actual review text
- `aspects`: List of hotel aspects mentioned
- `problems`: List of specific problems identified

## Hotel Aspects Covered
The dataset covers all major hotel aspects with natural language variations:
- Accommodation: rooms, suites, quarters
- Facilities: bathrooms (wc, toilet), shower, pool, gym, fitness
- Amenities: wifi (wi-fi, internet), air conditioning (ac, air con), tv, minibar
- Service: staff, reception, housekeeping, cleaning
- Dining: restaurant, breakfast, bar, food, drinks
- Comfort: bed, pillows, blankets, carpet, towels
- Environment: noise, smell, temperature, view
- Value: price, extra charges, extra fees

## Files
The dataset is split into {num_files} parts for easy download and processing:
"""
        
        for i in range(1, num_files + 1):
            readme_content += f"- `negative_hotel_reviews_part_{i:02d}_of_{num_files:02d}.json`\n"
        
        readme_content += f"""
## Quality Assurance
- Balanced representation across all hotel aspects
- Natural language variations and synonyms
- Realistic negative review patterns
- Commercial-grade quality for AI training

## Usage
This dataset is designed for:
- Sentiment analysis training
- Aspect-based opinion mining
- Hotel service improvement analysis
- Natural language processing research

## Generated
Dataset generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total aspects covered: {len(self.aspect_mappings)}
"""
        
        readme_path = os.path.join(output_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return readme_path

def main():
    print("🏨 Hotel Review Dataset Generator")
    print("=" * 50)
    
    generator = HotelReviewDatasetGenerator()
    
    # Generate the dataset
    reviews = generator.generate_balanced_dataset(750000)
    
    # Split and save
    file_paths = generator.split_and_save_dataset(reviews, 50000, "dataset_parts")
    
    # Generate README
    readme_path = generator.generate_readme(len(reviews), len(file_paths), "dataset_parts")
    file_paths.append(readme_path)
    
    print(f"\n✅ Dataset generation completed!")
    print(f"📊 Generated {len(reviews):,} reviews")
    print(f"📁 Split into {len(file_paths)-1} JSON files")
    print(f"📝 Created README.md")
    print(f"💾 All files saved in 'dataset_parts' directory")
    print(f"\n🚀 Ready for GitHub upload!")

if __name__ == "__main__":
    main()