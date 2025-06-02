import json
import random
import os
from typing import List, Dict, Tuple
import uuid
from datetime import datetime
import math

class HotelReviewDatasetGenerator:
    def __init__(self):
        # Comprehensive aspect mapping with synonyms and variations
        self.aspect_mappings = {
            "rooms": ["rooms", "room", "suite", "accommodation", "quarters"],
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
            "bugs": ["bugs", "insects", "pests", "cockroaches", "ants"],
            "coffee": ["coffee", "espresso", "cappuccino", "coffee machine"],
            "tea": ["tea", "herbal tea", "tea bags", "tea service"],
            "alcohol": ["alcohol", "wine", "beer", "spirits", "liquor"],
            "towels": ["towels", "towel", "bath towels", "linens"],
            "parking": ["parking", "parking lot", "valet", "garage"],
            "housekeeping": ["housekeeping", "room service", "cleaning service", "maid service"],
            "noise": ["noise", "loud", "sounds", "disturbance", "racket"]
        }
        
        # Problem templates for each aspect category
        self.problem_templates = {
            "rooms": [
                "cramped and uncomfortable space",
                "outdated and shabby decor",
                "broken furniture and fixtures",
                "poor lighting throughout",
                "musty and unpleasant atmosphere",
                "dirty and unkempt condition",
                "inadequate storage space",
                "damaged walls and surfaces"
            ],
            "bathrooms": [
                "moldy and dirty surfaces",
                "broken fixtures and fittings",
                "clogged drains and poor drainage",
                "cracked tiles and grout",
                "leaking pipes and water damage",
                "inadequate ventilation",
                "dirty and stained surfaces",
                "missing or broken accessories"
            ],
            "shower": [
                "poor water pressure",
                "inconsistent water temperature",
                "leaking and flooding issues",
                "moldy and dirty shower head",
                "broken or missing shower door",
                "slippery and unsafe floor",
                "rusty and corroded fixtures",
                "inadequate drainage"
            ],
            "bed": [
                "uncomfortable and lumpy mattress",
                "broken or squeaky frame",
                "stained and dirty sheets",
                "inadequate size for guests",
                "poor support and sagging",
                "noisy springs and creaking",
                "worn out and old bedding",
                "uncomfortable sleeping surface"
            ],
            "carpet": [
                "stained and dirty throughout",
                "worn out and frayed edges",
                "strong odors and smells",
                "loose and unsafe areas",
                "poor quality and cheap material",
                "visible wear and tear",
                "sticky and unclean surface",
                "damaged and torn sections"
            ],
            "pillows": [
                "flat and uncomfortable support",
                "dirty and stained covers",
                "lumpy and uneven filling",
                "strong odors and smells",
                "inadequate number provided",
                "poor quality and cheap material",
                "worn out and old condition",
                "uncomfortable and unsupportive"
            ],
            "blankets": [
                "thin and inadequate warmth",
                "dirty and stained condition",
                "torn and damaged fabric",
                "strong odors and smells",
                "inadequate size and coverage",
                "poor quality and cheap material",
                "worn out and old appearance",
                "uncomfortable and scratchy texture"
            ],
            "wifi": [
                "extremely slow connection speed",
                "frequent disconnections and outages",
                "poor signal strength throughout",
                "complicated login process",
                "limited data allowance",
                "unreliable and inconsistent service",
                "expensive additional charges",
                "technical issues and problems"
            ],
            "elevator": [
                "frequent breakdowns and malfunctions",
                "extremely slow and inefficient",
                "strange noises and vibrations",
                "dirty and unkempt interior",
                "broken buttons and controls",
                "poor lighting and atmosphere",
                "overcrowded and uncomfortable",
                "safety concerns and issues"
            ],
            "breakfast": [
                "limited and poor quality options",
                "cold and unappetizing food",
                "long queues and waiting times",
                "dirty and unsanitary conditions",
                "expensive additional charges",
                "poor variety and selection",
                "stale and old food items",
                "inadequate seating and space"
            ],
            "restaurant": [
                "poor quality and tasteless food",
                "extremely slow service",
                "dirty and unsanitary conditions",
                "overpriced and expensive menu",
                "rude and unprofessional staff",
                "limited menu options",
                "long waiting times",
                "cold and unappetizing meals"
            ],
            "lobby": [
                "dirty and unkempt appearance",
                "uncomfortable and worn furniture",
                "poor lighting and atmosphere",
                "crowded and chaotic environment",
                "outdated and shabby decor",
                "strong odors and smells",
                "inadequate seating areas",
                "poor maintenance and upkeep"
            ],
            "staff": [
                "rude and unprofessional behavior",
                "unhelpful and dismissive attitude",
                "poor communication skills",
                "slow response to requests",
                "inadequate knowledge and training",
                "argumentative and defensive",
                "unavailable when needed",
                "discriminatory treatment of guests"
            ],
            "service": [
                "extremely poor customer service",
                "slow response to complaints",
                "unprofessional and rude treatment",
                "inadequate problem resolution",
                "poor communication and follow-up",
                "dismissive attitude toward concerns",
                "lack of attention to detail",
                "disappointing overall experience"
            ],
            "cleaning": [
                "poor and inadequate cleaning standards",
                "dirty and unsanitary conditions",
                "missed areas and surfaces",
                "strong chemical odors",
                "inadequate frequency of service",
                "careless and rushed job",
                "dirty cleaning equipment used",
                "unprofessional cleaning staff"
            ],
            "air_conditioning": [
                "not working or broken",
                "extremely loud and noisy operation",
                "poor temperature control",
                "musty and unpleasant odors",
                "inadequate cooling capacity",
                "frequent breakdowns and issues",
                "dirty and clogged filters",
                "poor air circulation"
            ],
            "bar": [
                "overpriced and expensive drinks",
                "poor quality and watered down cocktails",
                "slow and inefficient service",
                "limited selection and options",
                "dirty and unsanitary conditions",
                "rude and unprofessional bartenders",
                "crowded and uncomfortable atmosphere",
                "poor quality and stale ingredients"
            ],
            "minibars": [
                "extremely overpriced items",
                "broken or not working",
                "limited and poor selection",
                "warm and not cooling properly",
                "dirty and unsanitary interior",
                "expired and stale products",
                "hidden charges and fees",
                "inadequate restocking service"
            ],
            "food": [
                "poor quality and tasteless meals",
                "cold and unappetizing presentation",
                "limited and poor variety",
                "overpriced and expensive options",
                "stale and old ingredients",
                "poor preparation and cooking",
                "unsanitary and dirty conditions",
                "disappointing overall quality"
            ],
            "pizza": [
                "cold and unappetizing slices",
                "poor quality and cheap toppings",
                "overpriced and expensive",
                "burnt and overcooked crust",
                "stale and old ingredients",
                "poor preparation and presentation",
                "limited variety and options",
                "disappointing taste and quality"
            ],
            "drinks": [
                "overpriced and expensive",
                "poor quality and watered down",
                "limited selection and variety",
                "warm and not properly chilled",
                "stale and old ingredients",
                "slow service and long waits",
                "dirty glasses and containers",
                "disappointing overall quality"
            ],
            "juice": [
                "artificial and poor taste",
                "overpriced and expensive",
                "not fresh and stale",
                "limited variety and options",
                "watered down and diluted",
                "warm and not properly chilled",
                "poor quality and cheap",
                "disappointing and unappetizing"
            ],
            "guide": [
                "inadequate knowledge and information",
                "poor communication skills",
                "unhelpful and dismissive attitude",
                "expensive and overpriced services",
                "unreliable and unpunctual",
                "poor organization and planning",
                "rude and unprofessional behavior",
                "disappointing overall experience"
            ],
            "transport": [
                "unreliable and delayed service",
                "overpriced and expensive",
                "uncomfortable and cramped vehicles",
                "poor condition and maintenance",
                "rude and unprofessional drivers",
                "inadequate scheduling and frequency",
                "dirty and unsanitary conditions",
                "disappointing overall experience"
            ],
            "price": [
                "extremely overpriced for quality",
                "hidden fees and charges",
                "poor value for money",
                "expensive additional costs",
                "unreasonable and excessive rates",
                "misleading and deceptive pricing",
                "unexpected surcharges and fees",
                "disappointing overall value"
            ],
            "expensiveness": [
                "ridiculously overpriced everything",
                "excessive charges for basic services",
                "poor value for money spent",
                "unreasonable and inflated prices",
                "expensive with poor quality",
                "costly with disappointing results",
                "overcharged for substandard service",
                "pricey with terrible experience"
            ],
            "kettle": [
                "broken and not working",
                "dirty and unsanitary condition",
                "missing or inadequate supplies",
                "poor quality and cheap",
                "electrical issues and problems",
                "inadequate capacity and size",
                "difficult to use and operate",
                "rusty and corroded appearance"
            ],
            "pool": [
                "dirty and unsanitary water",
                "closed or not available",
                "overcrowded and uncomfortable",
                "poor maintenance and upkeep",
                "broken equipment and facilities",
                "unsafe and hazardous conditions",
                "inadequate size and depth",
                "strong chemical odors"
            ],
            "stairs": [
                "dirty and poorly maintained",
                "unsafe and hazardous conditions",
                "poor lighting and visibility",
                "worn out and damaged steps",
                "inadequate handrails and support",
                "crowded and difficult access",
                "strong odors and smells",
                "poor overall condition"
            ],
            "reception": [
                "extremely slow check-in process",
                "rude and unprofessional staff",
                "long queues and waiting times",
                "poor communication and service",
                "inadequate information provided",
                "dismissive attitude toward guests",
                "disorganized and chaotic",
                "disappointing first impression"
            ],
            "view": [
                "obstructed and disappointing",
                "construction and noise outside",
                "dirty windows and poor visibility",
                "misleading and deceptive advertising",
                "ugly and unpleasant scenery",
                "blocked by other buildings",
                "poor quality and uninspiring",
                "not as advertised or promised"
            ],
            "extra_charges": [
                "unexpected and hidden fees",
                "excessive and unreasonable costs",
                "misleading and deceptive billing",
                "charged for basic amenities",
                "expensive additional services",
                "unfair and unjustified charges",
                "poor value for extra cost",
                "disappointing surprise expenses"
            ],
            "extra_fees": [
                "hidden and unexpected costs",
                "excessive and unreasonable charges",
                "misleading billing practices",
                "expensive additional services",
                "unfair and unjustified fees",
                "poor transparency and disclosure",
                "surprising and disappointing costs",
                "overcharged for basic services"
            ],
            "water": [
                "poor pressure and flow",
                "inconsistent temperature control",
                "dirty and contaminated supply",
                "frequent outages and interruptions",
                "strange taste and odor",
                "inadequate hot water supply",
                "rusty and discolored water",
                "poor quality and safety"
            ],
            "temperature": [
                "too hot and uncomfortable",
                "too cold and freezing",
                "inconsistent and fluctuating",
                "poor control and regulation",
                "inadequate heating and cooling",
                "uncomfortable room climate",
                "extreme and unbearable conditions",
                "poor ventilation and circulation"
            ],
            "tv": [
                "not working or broken",
                "poor picture and sound quality",
                "limited channels and options",
                "outdated and old equipment",
                "difficult to operate and use",
                "poor reception and signal",
                "small screen and inadequate size",
                "missing remote control"
            ],
            "gym": [
                "closed or not available",
                "poor quality and broken equipment",
                "dirty and unsanitary conditions",
                "overcrowded and uncomfortable",
                "inadequate facilities and space",
                "poor maintenance and upkeep",
                "limited hours and access",
                "disappointing overall condition"
            ],
            "fitness": [
                "broken and malfunctioning equipment",
                "dirty and unsanitary facilities",
                "overcrowded and uncomfortable",
                "poor quality and outdated machines",
                "inadequate variety and options",
                "poor maintenance and service",
                "limited access and availability",
                "disappointing overall experience"
            ],
            "window": [
                "dirty and smudged glass",
                "broken or damaged frames",
                "poor insulation and drafts",
                "difficult to open and close",
                "inadequate size and lighting",
                "poor quality and cheap materials",
                "blocked or obstructed view",
                "safety concerns and issues"
            ],
            "smoke": [
                "strong cigarette odor throughout",
                "poor ventilation and circulation",
                "designated smoking areas dirty",
                "smoke infiltrating non-smoking rooms",
                "inadequate air purification",
                "stale and unpleasant atmosphere",
                "health concerns and discomfort",
                "poor enforcement of policies"
            ],
            "smell": [
                "strong and unpleasant odors",
                "musty and stale atmosphere",
                "chemical and cleaning smells",
                "poor ventilation and circulation",
                "sewage and drainage odors",
                "food and cooking smells",
                "cigarette and smoke odors",
                "overall unpleasant environment"
            ],
            "hair": [
                "previous guests hair everywhere",
                "dirty and unsanitary conditions",
                "poor cleaning and housekeeping",
                "hair in bathroom and shower",
                "disgusting and unhygienic",
                "inadequate cleaning standards",
                "hair on bedding and furniture",
                "gross and unacceptable condition"
            ],
            "bugs": [
                "cockroaches and insects present",
                "bed bugs and pest infestation",
                "poor pest control and management",
                "unsanitary and dirty conditions",
                "health hazards and concerns",
                "disgusting and unacceptable",
                "inadequate cleaning and maintenance",
                "unsafe and unhygienic environment"
            ],
            "coffee": [
                "poor quality and terrible taste",
                "cold and unappetizing",
                "expensive and overpriced",
                "limited variety and options",
                "stale and old coffee",
                "poor preparation and service",
                "weak and watered down",
                "disappointing overall quality"
            ],
            "tea": [
                "poor quality and cheap tea bags",
                "limited variety and selection",
                "stale and old tea",
                "inadequate preparation supplies",
                "poor taste and quality",
                "expensive and overpriced",
                "cold and unappetizing",
                "disappointing overall experience"
            ],
            "alcohol": [
                "overpriced and expensive drinks",
                "poor quality and watered down",
                "limited selection and variety",
                "slow service and long waits",
                "poor bartending and preparation",
                "stale and old ingredients",
                "disappointing overall quality",
                "expensive with poor value"
            ],
            "towels": [
                "dirty and stained condition",
                "thin and poor quality",
                "inadequate number provided",
                "rough and uncomfortable texture",
                "old and worn out appearance",
                "strong odors and smells",
                "poor absorbency and quality",
                "unhygienic and unsanitary"
            ],
            "parking": [
                "extremely expensive and overpriced",
                "inadequate spaces and availability",
                "poor security and safety",
                "difficult access and navigation",
                "dirty and poorly maintained",
                "far from hotel entrance",
                "unclear pricing and policies",
                "disappointing overall experience"
            ],
            "housekeeping": [
                "poor cleaning and maintenance",
                "missed areas and surfaces",
                "rude and unprofessional staff",
                "inadequate frequency of service",
                "careless and rushed cleaning",
                "dirty equipment and supplies",
                "poor attention to detail",
                "disappointing overall standards"
            ],
            "noise": [
                "extremely loud and disruptive",
                "construction and traffic noise",
                "thin walls and poor insulation",
                "noisy neighbors and guests",
                "loud air conditioning and equipment",
                "street noise and disturbances",
                "poor soundproofing throughout",
                "uncomfortable and disturbing"
            ]
        }
        
        # Review structure templates for variety
        self.review_structures = [
            "The {aspect} was {problem}",
            "{aspect} had {problem}",
            "Poor {aspect} with {problem}",
            "Terrible {aspect} - {problem}",
            "Disappointed with {aspect} that had {problem}",
            "{aspect} was disappointing with {problem}",
            "Awful {aspect} suffering from {problem}",
            "The {aspect} experienced {problem}",
            "Unacceptable {aspect} with {problem}",
            "Bad {aspect} featuring {problem}",
            "{aspect} in poor condition with {problem}",
            "Horrible {aspect} plagued by {problem}",
            "The {aspect} was terrible due to {problem}",
            "{aspect} completely ruined by {problem}",
            "Disgusting {aspect} with obvious {problem}",
            "Shocking {aspect} that showed {problem}",
            "Appalling {aspect} marked by {problem}",
            "Dreadful {aspect} contaminated with {problem}",
            "Pathetic {aspect} destroyed by {problem}",
            "Repulsive {aspect} overwhelmed by {problem}"
        ]
        
    def get_random_aspects(self, min_aspects=1, max_aspects=3):
        """Get random aspects ensuring variety"""
        aspect_keys = list(self.aspect_mappings.keys())
        num_aspects = random.randint(min_aspects, max_aspects)
        selected_aspects = random.sample(aspect_keys, num_aspects)
        
        result_aspects = []
        for aspect_key in selected_aspects:
            # Choose random synonym for each aspect
            synonym = random.choice(self.aspect_mappings[aspect_key])
            result_aspects.append(synonym)
        
        return selected_aspects, result_aspects
    
    def get_problems_for_aspects(self, aspect_keys):
        """Get corresponding problems for selected aspects"""
        problems = []
        for aspect_key in aspect_keys:
            if aspect_key in self.problem_templates:
                problem = random.choice(self.problem_templates[aspect_key])
                problems.append(problem)
        return problems
    
    def generate_review_text(self, aspects, problems):
        """Generate natural review text"""
        if len(aspects) == 1:
            structure = random.choice(self.review_structures)
            return structure.format(aspect=aspects[0], problem=problems[0])
        else:
            # For multiple aspects, create more complex reviews
            review_parts = []
            for i, (aspect, problem) in enumerate(zip(aspects, problems)):
                if i == 0:
                    structure = random.choice(self.review_structures)
                    part = structure.format(aspect=aspect, problem=problem)
                else:
                    connectors = [" and ", " while ", " plus ", " also "]
                    connector = random.choice(connectors)
                    part = f"{connector}{aspect} with {problem}"
                review_parts.append(part)
            
            return "".join(review_parts)
    
    def generate_single_review(self, review_id):
        """Generate a single review"""
        aspect_keys, display_aspects = self.get_random_aspects()
        problems = self.get_problems_for_aspects(aspect_keys)
        
        review_text = self.generate_review_text(display_aspects, problems)
        
        # Ensure review doesn't exceed 60 tokens (approximate)
        words = review_text.split()
        if len(words) > 60:
            review_text = " ".join(words[:60])
            # Ensure it ends properly
            if not review_text.endswith('.'):
                review_text += "."
        
        return {
            "review_id": review_id,
            "review_text": review_text,
            "aspects": display_aspects,
            "problems": problems
        }
    
    def generate_balanced_dataset(self, total_reviews=750000):
        """Generate balanced dataset ensuring all aspects get fair representation"""
        reviews = []
        aspect_count = {key: 0 for key in self.aspect_mappings.keys()}
        target_per_aspect = total_reviews // len(self.aspect_mappings)
        
        print(f"Generating {total_reviews} reviews with balanced aspect distribution...")
        print(f"Target per aspect: {target_per_aspect}")
        
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
                print(f"Generated {i} reviews...")
        
        print("Final aspect distribution:")
        for key, count in aspect_count.items():
            print(f"{key}: {count}")
        
        return reviews
    
    def split_and_save_dataset(self, reviews, chunk_size=50000, output_dir="dataset_parts"):
        """Split dataset into parts and save as JSON files"""
        os.makedirs(output_dir, exist_ok=True)
        
        total_chunks = math.ceil(len(reviews) / chunk_size)
        file_paths = []
        
        for i in range(total_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(reviews))
            chunk = reviews[start_idx:end_idx]
            
            filename = f"negative_hotel_reviews_part_{i+1:02d}_of_{total_chunks:02d}.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(chunk, f, indent=2, ensure_ascii=False)
            
            file_paths.append(filepath)
            print(f"Saved {filename} with {len(chunk)} reviews")
        
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
