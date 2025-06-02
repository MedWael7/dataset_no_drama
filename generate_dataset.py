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
        
        # Problem templates for each aspect category - realistic like booking.com/tripadvisor
        self.problem_templates = {
            "rooms": [
                "extremely small and cramped", "tiny with no space to move around", "so small you can barely fit luggage",
                "claustrophobic and uncomfortable", "much smaller than advertised", "like a closet not a room",
                "outdated furniture and decor", "musty smell that won't go away", "dark with terrible lighting",
                "no storage space whatsoever", "walls paper-thin you hear everything", "dirty and poorly maintained",
                "broken furniture everywhere", "stains on walls and ceiling", "feels like a prison cell"
            ],
            "bathrooms": [
                "shower head broken and leaking everywhere", "moldy tiles and disgusting grout", "toilet wouldn't flush properly",
                "no hot water at all", "drain clogged and water backing up", "missing tiles and cracked surfaces",
                "door doesn't lock or close properly", "ventilation broken so always humid", "hair from previous guests everywhere",
                "dirty towels that smell terrible", "no soap or toiletries provided", "floor always wet and slippery"
            ],
            "shower": [
                "water pressure so weak it's useless", "scalding hot then freezing cold", "shower door completely broken",
                "drain blocked so water floods bathroom", "shower head covered in mold", "no hot water after 5pm",
                "ceiling leaking during shower", "slippery floor almost fell down", "rust stains everywhere",
                "curtain moldy and disgusting", "takes forever to get warm water", "water smells like sewage"
            ],
            "bed": [
                "mattress so old and lumpy couldn't sleep", "springs poking through everywhere", "sheets hadn't been changed dirty",
                "bed so small two people don't fit", "squeaks loudly every time you move", "pillow flat as a pancake",
                "bedding smells like cigarettes", "mattress stained and disgusting", "bed frame broken and wobbly",
                "blankets thin and useless", "found hair and crumbs in sheets", "hardest mattress ever slept on"
            ],
            "carpet": [
                "stained with God knows what", "sticky and gross to walk on", "smells terrible like old food",
                "worn out with holes everywhere", "dirty and hasn't been cleaned in years", "loose and dangerous trip hazard",
                "pet hair all over despite no pets allowed", "burn marks and cigarette stains", "wet in corners and moldy"
            ],
            "pillows": [
                "flat and completely useless", "smells like someone else's head", "covered in stains",
                "so hard it hurt my neck", "only one tiny pillow provided", "lumpy and uncomfortable",
                "pillowcase dirty and hadn't been washed", "feathers poking through fabric", "way too small for bed"
            ],
            "blankets": [
                "thin as paper no warmth at all", "dirty with mysterious stains", "smells like cigarettes and mold",
                "torn and falling apart", "too small doesn't cover the bed", "scratchy and uncomfortable",
                "hadn't been washed in forever", "holes throughout the fabric", "freezing cold all night"
            ],
            "wifi": [
                "doesn't work at all complete waste", "so slow couldn't load anything", "keeps disconnecting every 5 minutes",
                "password doesn't work nobody knows it", "only works in lobby not rooms", "charged extra for terrible connection",
                "signal so weak can't connect", "blocked all streaming services", "limited to 1 hour per day ridiculous"
            ],
            "elevator": [
                "broken down for entire stay", "takes forever to arrive", "makes scary noises and shakes",
                "stops working after 10pm", "dirty and smells terrible", "buttons don't work properly",
                "gets stuck between floors", "too small for luggage", "lighting flickering and scary"
            ],
            "breakfast": [
                "cold eggs and burnt toast", "ran out of everything by 8am", "terrible coffee tastes like water",
                "same boring food every single day", "long queues and rude staff", "dirty plates and utensils",
                "overpriced for what you get", "flies buzzing around food", "everything stale and old"
            ],
            "restaurant": [
                "food took 2 hours to arrive", "overpriced and tastes awful", "rude waiters who ignore you",
                "kitchen clearly dirty and unsanitary", "limited menu with no good options", "cold food served on dirty plates",
                "ran out of half the menu items", "charged extra for everything", "worst meal of my life"
            ],
            "lobby": [
                "dirty and run down appearance", "broken furniture and torn seats", "smells like old carpet and mold",
                "no air conditioning sweltering hot", "crowded with nowhere to sit", "staff ignoring everyone waiting",
                "outdated and depressing atmosphere", "noisy and chaotic all the time", "dark with terrible lighting"
            ],
            "staff": [
                "rude and completely unhelpful", "act like guests are bothering them", "don't speak English properly",
                "never available when you need help", "promised things then never followed through", "argumentative when complained",
                "clearly don't care about guest experience", "gave wrong information repeatedly", "discriminated against us obviously"
            ],
            "service": [
                "worst customer service ever experienced", "nobody cares about guest problems", "took days to fix simple issues",
                "promised call back never happened", "rude responses to valid complaints", "charge for everything including basic service",
                "unprofessional attitude throughout stay", "felt like we were inconveniencing them", "no follow up on any requests"
            ],
            "cleaning": [
                "room obviously hadn't been cleaned", "towels dirty and smelly", "bathroom disgusting with hair everywhere",
                "trash not emptied for days", "bed sheets clearly used by previous guest", "dust and dirt all over surfaces",
                "housekeeping never showed up", "cleaning supplies smell toxic", "missed obvious stains and mess"
            ],
            "air_conditioning": [
                "doesn't work stuck sweating all night", "makes horrible loud noise", "only blows hot air",
                "remote control broken can't adjust", "leaking water all over floor", "turns off randomly during night",
                "freezing cold can't turn it down", "smells moldy when turned on", "unit falling out of wall"
            ],
            "bar": [
                "overpriced drinks taste watered down", "bartender rude and slow", "dirty glasses with lipstick stains",
                "limited selection of cheap alcohol", "closed early without notice", "loud music you can't talk",
                "sticky bar and dirty stools", "charged wrong amount several times", "worst cocktails ever tasted"
            ],
            "minibars": [
                "doesn't work items warm", "ridiculously overpriced everything", "empty or broken items inside",
                "charged for items we didn't take", "key doesn't work can't open", "moldy food inside expired products",
                "no refund for broken minibar", "restocked with warm drinks", "locked and nobody has key"
            ],
            "food": [
                "terrible quality tastes like cardboard", "clearly reheated frozen meals", "cold when served disgusting",
                "overpriced for poor quality", "limited options all taste same", "food poisoning after eating here",
                "clearly been sitting out too long", "no vegetarian options available", "worst food ever eaten"
            ],
            "pizza": [
                "cold and soggy crust", "toppings clearly old and cheap", "took over an hour to deliver",
                "burnt bottom raw top", "sauce tastes like ketchup", "cheese plastic and fake",
                "smallest pizza ever seen for price", "delivered to wrong room twice", "inedible threw it away"
            ],
            "drinks": [
                "watered down and tasteless", "warm beer and flat soda", "limited selection only cheap brands",
                "overcharged for everything", "rude service when ordering", "glasses dirty with fingerprints",
                "took forever to get drinks", "wrong order multiple times", "charged for drinks we didn't order"
            ],
            "juice": [
                "clearly from concentrate tastes artificial", "warm and not refrigerated", "limited to only apple juice",
                "overpriced small portions", "expired and tasted sour", "pulp and chunks floating around",
                "served in dirty glasses", "ran out early in morning", "mixed with water tastes terrible"
            ],
            "guide": [
                "didn't know basic information about area", "rude and impatient with questions", "clearly just wanted money",
                "showed up late and unprepared", "poor English couldn't understand", "rushed through everything quickly",
                "overcharged for terrible tour", "took us to wrong places", "cancelled last minute no refund"
            ],
            "transport": [
                "shuttle never showed up", "dirty van with broken seats", "driver rude and unsafe", 
                "overcharged for short distance", "no air conditioning sweltering hot", "took forever unreliable schedule",
                "van broke down left us stranded", "charged extra hidden fees", "worst transportation experience ever"
            ],
            "price": [
                "ridiculously overpriced for what you get", "hidden fees added at checkout", "charged double what was advertised",
                "not worth half the price paid", "found cheaper better hotels nearby", "felt completely ripped off",
                "surprise charges on final bill", "poor value for money spent", "expensive everything including basic amenities"
            ],
            "expensiveness": [
                "everything costs fortune here", "charged for wifi air conditioning everything", "most expensive terrible hotel ever",
                "nickel and dimed for every little thing", "poor quality for premium prices", "tourist trap pricing scheme",
                "rip off avoid at all costs", "overpriced mediocre experience", "expensive disappointing waste of money"
            ],
            "kettle": [
                "doesn't work completely broken", "dirty with lime scale buildup", "no coffee or tea provided",
                "takes forever to boil water", "plastic taste in all water", "cord too short can't reach outlet",
                "leaks water all over counter", "old and rusty inside", "missing parts doesn't function"
            ],
            "pool": [
                "closed for renovation without notice", "dirty water with floating debris", "overcrowded with screaming kids",
                "no lifeguard on duty unsafe", "chlorine smell overwhelming", "slippery deck almost fell",
                "too cold to swim in", "broken tiles cut my foot", "hours limited only open few hours"
            ],
            "stairs": [
                "poorly lit dangerous at night", "carpet loose and trip hazard", "broken handrail almost fell",
                "dirty with stains and garbage", "steep and difficult to climb", "echo chamber every sound amplified",
                "smells like urine and cigarettes", "paint peeling and looks terrible", "no elevator alternative only stairs"
            ],
            "reception": [
                "long queue waited hour to check in", "staff rude and unhelpful attitude", "lost our reservation completely",
                "charged wrong amount argued with us", "gave wrong room keys twice", "no English speaking staff available",
                "computer system down couldn't help", "ignored us while helping other guests", "worst first impression ever"
            ],
            "view": [
                "faces brick wall not ocean advertised", "construction site with constant noise", "garbage dumpster right outside window",
                "completely blocked by other building", "dirty windows can't see anything", "false advertising in photos",
                "parking lot view not cityscape promised", "air conditioning units blocking entire view", "terrible disappointing outlook"
            ],
            "extra_charges": [
                "surprise fees not mentioned anywhere", "charged for basic amenities like towels", "resort fee added without explanation",
                "parking costs more than room", "wifi internet access costs extra", "cleaning fee charged even though dirty",
                "service charges added to everything", "tourist tax not mentioned when booking", "nickel and dimed constantly"
            ],
            "extra_fees": [
                "hidden charges discovered at checkout", "charged for using safe in room", "additional person fee for child",
                "early checkin late checkout fees", "baggage storage costs money", "pool towel rental fees ridiculous",
                "breakfast charged separately not included", "air conditioning usage fee added", "telephone calls charged premium rates"
            ],
            "water": [
                "no hot water entire stay", "pressure so weak can't shower", "tastes terrible like chlorine",
                "brown rusty color coming out", "turns cold after 2 minutes", "shut off randomly during shower",
                "leaking faucets constant dripping noise", "smells like sewage when first turned on", "limited hours hot water only morning"
            ],
            "temperature": [
                "freezing cold couldn't get warm", "sweltering hot no air conditioning", "thermostat broken can't control",
                "heating doesn't work at all", "too hot during day too cold night", "no fan or circulation",
                "windows don't open stuffy air", "drafty cold air coming through gaps", "uncomfortable temperature entire stay"
            ],
            "tv": [
                "doesn't work black screen", "only 3 channels all static", "remote control missing batteries dead",
                "tiny screen from 1990s", "no cable satellite basic channels only", "volume stuck on loud",
                "screen cracked can't see properly", "turns off randomly during shows", "no english channels available"
            ],
            "gym": [
                "closed without notice sign on door", "equipment broken and dangerous", "dirty towels and equipment",
                "too small only 2 machines", "no air conditioning sweltering hot", "limited hours only open mornings",
                "machines don't work properly", "no water fountain or amenities", "smells terrible like sweat"
            ],
            "fitness": [
                "equipment old and broken down", "weights missing and scattered", "machines don't work properly",
                "dirty and unsanitary conditions", "no cleaning supplies or towels", "overcrowded can't use anything",
                "poor ventilation smells horrible", "unsafe equipment falling apart", "limited selection outdated machines"
            ],
            "window": [
                "doesn't open stuck shut", "broken glass and cracks", "dirty can't see through",
                "no screen bugs flying in", "faces noisy street no sleep", "blinds broken won't close",
                "drafty cold air coming through", "paint peeling around frame", "too small for room size"
            ],
            "smoke": [
                "reeks of cigarettes despite non smoking", "smoke alarm going off constantly", "previous guests smoked heavily smell embedded",
                "designated smoking area right outside window", "ventilation poor smoke lingers", "ashtrays dirty and overflowing",
                "smoke smell in hallways elevators", "no smoking policy not enforced", "had to change rooms because smoke"
            ],
            "smell": [
                "musty moldy odor throughout", "sewage smell in bathroom", "chemical cleaning smell overwhelming",
                "previous guests cooking smell lingering", "garbage smell from dumpster outside", "wet carpet smell gross",
                "cigarette smoke embedded everywhere", "pet odor despite no pets policy", "unidentifiable bad smell can't get rid"
            ],
            "hair": [
                "previous guest hair all over bathroom", "hair in bed sheets disgusting", "clogged drain with hair",
                "hair on towels and washcloths", "bathroom floor covered in hair", "hair stuck to shower walls",
                "found hair in supposedly clean linens", "housekeeping obviously didn't clean hair everywhere", "gross hair in sink and tub"
            ],
            "bugs": [
                "cockroaches running across floor", "ants all over bathroom counter", "bed bugs bit us all night",
                "flies in room food area", "spiders in corners and ceiling", "moths flying around lights",
                "beetles crawling out of drain", "pest control obviously needed", "insects everywhere disgusting conditions"
            ],
            "coffee": [
                "tastes like dirty water", "machine broken doesn't work", "instant coffee only terrible quality",
                "cold and undrinkable", "limited to one cup per day", "charged extra for decent coffee",
                "old grounds reused tastes awful", "no cream sugar or supplies", "worst coffee ever tasted"
            ],
            "tea": [
                "cheap tea bags taste like cardboard", "no variety only basic black tea", "no hot water for tea",
                "tea bags old and stale", "no honey sugar or milk provided", "charged extra for tea service",
                "lukewarm water not hot enough", "limited selection poor quality", "tea tastes terrible avoid"
            ],
            "alcohol": [
                "watered down drinks taste terrible", "overpriced for poor quality", "limited selection cheap brands only",
                "bartender doesn't know how make drinks", "charged premium for well drinks", "warm beer not cold",
                "fake alcohol tastes artificial", "ran out of everything good early", "worst drinks ever tasted"
            ],
            "towels": [
                "dirty with stains and smells", "thin and scratchy like sandpaper", "not enough towels provided",
                "holes and tears throughout", "previous guest hair all over", "musty smell like mildew",
                "changed once during week stay", "tiny hand towels only", "gray and dingy not white"
            ],
            "parking": [
                "costs more than room ridiculous", "no spaces available ever", "far walk with heavy luggage",
                "unsafe area car broken into", "tight spaces damaged car door", "not secure anyone can access",
                "additional charges not mentioned", "valet damaged car no responsibility", "worst parking experience ever"
            ],
            "housekeeping": [
                "never cleaned room entire stay", "staff rude and dismissive", "missed obvious dirt and stains",
                "took tips but didn't clean properly", "broke items didn't replace", "entered room without permission",
                "lazy job skipped most cleaning", "used dirty rags made things worse", "worst housekeeping service ever"
            ],
            "noise": [
                "paper thin walls hear everything", "construction starting at 6am", "loud music until 3am",
                "traffic noise all night no sleep", "neighbors arguing screaming", "plumbing pipes loud banging",
                "air conditioning rattling noise", "hallway noise echoing into room", "couldn't sleep entire stay"
            ]
        }
        
        # Review structure templates for variety - realistic like booking.com/tripadvisor
        self.review_structures = [
            "The {aspect} was {problem}",
            "{aspect} {problem}",
            "Terrible {aspect} - {problem}",
            "Worst {aspect} ever, {problem}",
            "Avoid this place! {aspect} {problem}",
            "Disappointed with {aspect} that {problem}",
            "Never again! {aspect} {problem}",
            "Don't stay here, {aspect} {problem}",
            "Awful experience with {aspect} - {problem}",
            "Disgusting {aspect}, {problem}",
            "Shocking! {aspect} {problem}",
            "Can't believe {aspect} {problem}",
            "Hotel from hell! {aspect} {problem}",
            "Save your money, {aspect} {problem}",
            "Nightmare stay - {aspect} {problem}",
            "Absolutely terrible {aspect} {problem}",
            "What a joke! {aspect} {problem}",
            "Worst hotel ever! {aspect} {problem}",
            "Stay away! {aspect} {problem}",
            "Total disaster - {aspect} {problem}"
        ]
    
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