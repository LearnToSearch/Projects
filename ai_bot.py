import random
import re
from datetime import datetime

class ARGOOceanChatbot:
    def __init__(self):
        self.name = "FloatChat ARGO Bot"
        self.ocean_data = self.initialize_ocean_data()
        self.fish_species = self.initialize_fish_species()
        self.greetings = ["hello", "hi", "hey", "greetings", "howdy"]
        self.farewells = ["bye", "goodbye", "see you", "farewell", "quit", "exit"]
        
    def initialize_ocean_data(self):
        """Initialize ocean data with comprehensive information"""
        return {
            "pacific": {
                "name": "Pacific Ocean",
                "temperature": "22.5°C (72.5°F) average surface temperature",
                "salinity": "34.7 PSU average salinity",
                "oxygen": "4.5-6.2 mg/L (varies by depth and location)",
                "currents": "Major currents: Kuroshio, California, Humboldt, East Australian",
                "depth": "Average depth: 4,280m (14,040ft), Maximum: 10,911m (Mariana Trench)",
                "coordinates": "0°N 160°W (approximate center)",
                "area": "165,250,000 km² (63,800,000 sq mi)",
                "volume": "710,000,000 km³ (170,000,000 cu mi)",
                "facts": "The Pacific Ocean is the largest and deepest ocean, covering about 30% of Earth's surface.",
                "data_source": "ARGO Float WMO 4901254, 2023-09-15",
                "countries": ["United States", "Canada", "Mexico", "Japan", "Australia", "China", "Chile", "Peru"],
                "oxygen_min": 4.5,
                "oxygen_max": 6.2,
                "ph_level": "7.8-8.3 (slightly alkaline)"
            },
            "atlantic": {
                "name": "Atlantic Ocean",
                "temperature": "18.9°C (66.0°F) average surface temperature",
                "salinity": "35.4 PSU average salinity",
                "oxygen": "5.0-6.5 mg/L (higher in northern regions)",
                "currents": "Major currents: Gulf Stream, North Atlantic Drift, Canary, Benguela",
                "depth": "Average depth: 3,646m (11,962ft), Maximum: 8,376m (Puerto Rico Trench)",
                "coordinates": "0°N 30°W (approximate center)",
                "area": "106,460,000 km² (41,100,000 sq mi)",
                "volume": "310,410,900 km³ (74,471,500 cu mi)",
                "facts": "The Atlantic Ocean is the second largest and saltiest ocean, crucial for global thermohaline circulation.",
                "data_source": "ARGO Float WMO 3901402, 2023-09-10",
                "countries": ["United States", "Brazil", "United Kingdom", "France", "Spain", "South Africa", "Nigeria"],
                "oxygen_min": 5.0,
                "oxygen_max": 6.5,
                "ph_level": "7.9-8.4 (slightly alkaline)"
            },
            "indian": {
                "name": "Indian Ocean",
                "temperature": "26.0°C (78.8°F) average surface temperature",
                "salinity": "34.8 PSU average salinity",
                "oxygen": "4.2-5.8 mg/L (lower in northern regions)",
                "currents": "Major currents: Agulhas, West Australian, Monsoon Drift",
                "depth": "Average depth: 3,741m (12,274ft), Maximum: 7,258m (Java Trench)",
                "coordinates": "20°S 80°E (approximate center)",
                "area": "70,560,000 km² (27,240,000 sq mi)",
                "volume": "264,000,000 km³ (63,000,000 cu mi)",
                "facts": "The Indian Ocean is the warmest ocean, significantly influencing monsoon patterns in Asia.",
                "data_source": "ARGO Float WMO 2902267, 2023-09-12",
                "countries": ["India", "Indonesia", "Australia", "South Africa", "Maldives", "Sri Lanka", "Thailand"],
                "oxygen_min": 4.2,
                "oxygen_max": 5.8,
                "ph_level": "7.8-8.3 (slightly alkaline)"
            },
            "southern": {
                "name": "Southern Ocean",
                "temperature": "2.0°C (35.6°F) average surface temperature",
                "salinity": "34.2 PSU average salinity",
                "oxygen": "6.0-8.0 mg/L (higher due to cold water)",
                "currents": "Major current: Antarctic Circumpolar Current",
                "depth": "Average depth: 4,500m (14,800ft), Maximum: 7,235m (South Sandwich Trench)",
                "coordinates": "65°S 90°E (approximate center)",
                "area": "21,960,000 km² (8,480,000 sq mi)",
                "volume": "71,800,000 km³ (17,200,000 cu mi)",
                "facts": "The Southern Ocean connects the Atlantic, Pacific, and Indian Oceans and plays a key role in global climate regulation.",
                "data_source": "ARGO Float WMO 5904463, 2023-09-05",
                "countries": ["No sovereign nations, surrounds Antarctica"],
                "oxygen_min": 6.0,
                "oxygen_max": 8.0,
                "ph_level": "7.9-8.2 (slightly alkaline)"
            },
            "arctic": {
                "name": "Arctic Ocean",
                "temperature": "-1.5°C (29.3°F) average surface temperature",
                "salinity": "30.5 PSU average salinity",
                "oxygen": "7.0-9.0 mg/L (highest due to very cold water)",
                "currents": "Major currents: Beaufort Gyre, Transpolar Drift",
                "depth": "Average depth: 1,205m (3,953ft), Maximum: 5,550m (Eurasia Basin)",
                "coordinates": "90°N 0°E (North Pole)",
                "area": "15,558,000 km² (6,006,000 sq mi)",
                "volume": "18,750,000 km³ (4,500,000 cu mi)",
                "facts": "The Arctic Ocean is the smallest and shallowest ocean, experiencing significant sea ice loss due to climate change.",
                "data_source": "ARGO Float WMO 7900542, 2023-09-18",
                "countries": ["United States (Alaska)", "Canada", "Russia", "Norway", "Greenland (Denmark)", "Iceland"],
                "oxygen_min": 7.0,
                "oxygen_max": 9.0,
                "ph_level": "7.8-8.1 (slightly alkaline)"
            }
        }
    
    def initialize_fish_species(self):
        """Initialize fish species data for each ocean"""
        return {
            "pacific": [
                {"name": "Pacific Salmon", "scientific_name": "Oncorhynchus spp.", "habitat": "Coastal and open ocean", "conservation_status": "Varies by species"},
                {"name": "Bluefin Tuna", "scientific_name": "Thunnus orientalis", "habitat": "Open ocean", "conservation_status": "Endangered"},
                {"name": "Clownfish", "scientific_name": "Amphiprioninae", "habitat": "Coral reefs", "conservation_status": "Least Concern"},
                {"name": "Manta Ray", "scientific_name": "Mobula birostris", "habitat": "Open ocean", "conservation_status": "Vulnerable"}
            ],
            "atlantic": [
                {"name": "Atlantic Cod", "scientific_name": "Gadus morhua", "habitat": "Coastal and deep water", "conservation_status": "Vulnerable"},
                {"name": "Blue Marlin", "scientific_name": "Makaira nigricans", "habitat": "Open ocean", "conservation_status": "Vulnerable"},
                {"name": "Humpback Whale", "scientific_name": "Megaptera novaeangliae", "habitat": "Open ocean", "conservation_status": "Least Concern"},
                {"name": "American Lobster", "scientific_name": "Homarus americanus", "habitat": "Coastal seabed", "conservation_status": "Least Concern"}
            ],
            "indian": [
                {"name": "Manta Ray", "scientific_name": "Mobula alfredi", "habitat": "Coral reefs", "conservation_status": "Vulnerable"},
                {"name": "Coral Trout", "scientific_name": "Plectropomus leopardus", "habitat": "Coral reefs", "conservation_status": "Least Concern"},
                {"name": "Whale Shark", "scientific_name": "Rhincodon typus", "habitat": "Open ocean", "conservation_status": "Endangered"},
                {"name": "Clownfish", "scientific_name": "Amphiprion ocellaris", "habitat": "Coral reefs", "conservation_status": "Least Concern"}
            ],
            "southern": [
                {"name": "Antarctic Krill", "scientific_name": "Euphausia superba", "habitat": "Open ocean", "conservation_status": "Least Concern"},
                {"name": "Patagonian Toothfish", "scientific_name": "Dissostichus eleginoides", "habitat": "Deep water", "conservation_status": "Vulnerable"},
                {"name": "Emperor Penguin", "scientific_name": "Aptenodytes forsteri", "habitat": "Coastal and ice", "conservation_status": "Near Threatened"},
                {"name": "Weddell Seal", "scientific_name": "Leptonychotes weddellii", "habitat": "Coastal and ice", "conservation_status": "Least Concern"}
            ],
            "arctic": [
                {"name": "Arctic Cod", "scientific_name": "Boreogadus saida", "habitat": "Coastal and open ocean", "conservation_status": "Least Concern"},
                {"name": "Greenland Shark", "scientific_name": "Somniosus microcephalus", "habitat": "Deep water", "conservation_status": "Vulnerable"},
                {"name": "Narwhal", "scientific_name": "Monodon monoceros", "habitat": "Open ocean", "conservation_status": "Near Threatened"},
                {"name": "Beluga Whale", "scientific_name": "Delphinapterus leucas", "habitat": "Coastal and open ocean", "conservation_status": "Least Concern"}
            ]
        }
    
    def correct_spelling(self, query):
        """Correct common spelling mistakes in ocean-related terms"""
        corrections = {
            "pasific": "pacific",
            "atlantik": "atlantic",
            "indian": "indian",
            "southern": "southern",
            "artic": "arctic",
            "antartic": "southern",
            "temp": "temperature",
            "sal": "salinity",
            "current": "currents",
            "deep": "depth",
            "warm": "temperature",
            "cold": "temperature",
            "hot": "temperature",
            "salt": "salinity",
            "flow": "currents",
            "oxy": "oxygen",
            "o2": "oxygen",
            "fish": "fishes",
            "species": "fishes",
            "ph": "ph level",
            "acidity": "ph level"
        }
        
        words = query.lower().split()
        corrected_words = [corrections.get(word, word) for word in words]
        return " ".join(corrected_words)
    
    def detect_ocean(self, query):
        """Detect which ocean is mentioned in the query"""
        query = query.lower()
        oceans = {
            "pacific": ["pacific", "pacific ocean"],
            "atlantic": ["atlantic", "atlantic ocean"],
            "indian": ["indian", "indian ocean"],
            "southern": ["southern", "southern ocean", "antarctic", "antarctica"],
            "arctic": ["arctic", "arctic ocean"]
        }
        
        for ocean, keywords in oceans.items():
            for keyword in keywords:
                if keyword in query:
                    return ocean
        return None
    
    def get_ocean_info(self, ocean, info_type):
        """Get specific information about an ocean"""
        if ocean not in self.ocean_data:
            return f"I don't have information about that ocean."
        
        if info_type in self.ocean_data[ocean]:
            return self.ocean_data[ocean][info_type]
        else:
            return f"I don't have {info_type} information for the {self.ocean_data[ocean]['name']}."
    
    def get_fish_info(self, ocean):
        """Get information about fish species in an ocean"""
        if ocean not in self.fish_species:
            return f"I don't have fish species information for that ocean."
        
        fish_list = self.fish_species[ocean]
        response = f"Common fish species in the {self.ocean_data[ocean]['name']}:\n"
        for fish in fish_list:
            response += f"- {fish['name']} ({fish['scientific_name']}): {fish['habitat']}, Conservation Status: {fish['conservation_status']}\n"
        return response
    
    def compare_oceans(self, parameter):
        """Compare a specific parameter across all oceans"""
        if parameter not in ["temperature", "salinity", "oxygen", "depth"]:
            return "I can only compare temperature, salinity, oxygen, or depth across oceans."
        
        response = f"Comparison of {parameter} across oceans:\n"
        for ocean, data in self.ocean_data.items():
            response += f"- {data['name']}: {data[parameter]}\n"
        return response
    
    def get_general_info(self, ocean):
        """Get general information about an ocean"""
        if ocean not in self.ocean_data:
            return "I don't have information about that ocean."
        
        data = self.ocean_data[ocean]
        response = f"Information about the {data['name']}:\n"
        response += f"- Location: {data['coordinates']}\n"
        response += f"- Area: {data['area']}\n"
        response += f"- Volume: {data['volume']}\n"
        response += f"- Average Depth: {data['depth']}\n"
        response += f"- Temperature: {data['temperature']}\n"
        response += f"- Salinity: {data['salinity']}\n"
        response += f"- Oxygen Levels: {data['oxygen']}\n"
        response += f"- pH Level: {data['ph_level']}\n"
        response += f"- Interesting Fact: {data['facts']}\n"
        response += f"- Data Source: {data['data_source']}\n"
        return response
    
    def generate_response(self, query):
        """Generate a response to a user query"""
        query = self.correct_spelling(query.lower())
        
        # Check for greetings
        if any(greeting in query for greeting in self.greetings):
            return "Hello! I'm FloatChat, your AI assistant for exploring ARGO ocean data. How can I help you today?"
        
        # Check for farewells
        if any(farewell in query for farewell in self.farewells):
            return "Goodbye! Thank you for using FloatChat. Feel free to return with more questions about ocean data!"
        
        # Detect which ocean is being discussed
        ocean = self.detect_ocean(query)
        
        # Handle specific information requests
        if "temperature" in query:
            if ocean:
                return f"The temperature in the {self.ocean_data[ocean]['name']} is {self.ocean_data[ocean]['temperature']}."
            else:
                return self.compare_oceans("temperature")
        
        elif "salinity" in query or "salt" in query:
            if ocean:
                return f"The salinity in the {self.ocean_data[ocean]['name']} is {self.ocean_data[ocean]['salinity']}."
            else:
                return self.compare_oceans("salinity")
        
        elif "oxygen" in query or "o2" in query:
            if ocean:
                return f"The oxygen levels in the {self.ocean_data[ocean]['name']} are {self.ocean_data[ocean]['oxygen']}."
            else:
                return self.compare_oceans("oxygen")
        
        elif "depth" in query or "deep" in query:
            if ocean:
                return f"The depth of the {self.ocean_data[ocean]['name']} is {self.ocean_data[ocean]['depth']}."
            else:
                return self.compare_oceans("depth")
        
        elif "ph" in query or "acidity" in query:
            if ocean:
                return f"The pH level in the {self.ocean_data[ocean]['name']} is {self.ocean_data[ocean]['ph_level']}."
            else:
                response = "pH levels across oceans:\n"
                for ocean_name, data in self.ocean_data.items():
                    response += f"- {data['name']}: {data['ph_level']}\n"
                return response
        
        elif "fish" in query or "species" in query:
            if ocean:
                return self.get_fish_info(ocean)
            else:
                return "Which ocean are you interested in? I can tell you about fish species in the Pacific, Atlantic, Indian, Southern, or Arctic Ocean."
        
        elif "current" in query or "flow" in query:
            if ocean:
                return f"The major currents in the {self.ocean_data[ocean]['name']} are: {self.ocean_data[ocean]['currents']}."
            else:
                response = "Major ocean currents:\n"
                for ocean_name, data in self.ocean_data.items():
                    response += f"- {data['name']}: {data['currents']}\n"
                return response
        
        elif "location" in query or "where" in query or "coordinates" in query:
            if ocean:
                return f"The {self.ocean_data[ocean]['name']} is located at approximately {self.ocean_data[ocean]['coordinates']}."
            else:
                response = "Ocean locations:\n"
                for ocean_name, data in self.ocean_data.items():
                    response += f"- {data['name']}: {data['coordinates']}\n"
                return response
        
        elif "area" in query or "size" in query:
            if ocean:
                return f"The {self.ocean_data[ocean]['name']} has an area of {self.ocean_data[ocean]['area']}."
            else:
                response = "Ocean areas:\n"
                for ocean_name, data in self.ocean_data.items():
                    response += f"- {data['name']}: {data['area']}\n"
                return response
        
        elif "fact" in query or "interesting" in query:
            if ocean:
                return f"Interesting fact about the {self.ocean_data[ocean]['name']}: {self.ocean_data[ocean]['facts']}"
            else:
                response = "Interesting facts about oceans:\n"
                for ocean_name, data in self.ocean_data.items():
                    response += f"- {data['name']}: {data['facts']}\n"
                return response
        
        # General information about a specific ocean
        elif ocean:
            return self.get_general_info(ocean)
        
        # Default response for unrecognized queries
        else:
            return "I'm not sure I understand. I can help you with information about ocean temperature, salinity, oxygen levels, depth, currents, fish species, and more. Try asking about a specific ocean or parameter."

def main():
    """Main function to run the chatbot"""
    chatbot = ARGOOceanChatbot()
    
    print("=" * 60)
    print("Welcome to FloatChat - ARGO Ocean Data Chatbot")
    print("=" * 60)
    print("I can help you explore data about oceans including:")
    print("- Temperature, salinity, oxygen levels, and pH")
    print("- Depth and geographical information")
    print("- Currents and water movement patterns")
    print("- Fish species and marine life")
    print("- Interesting facts and data sources")
    print("Type 'quit' or 'exit' to end the conversation")
    print("=" * 60)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in chatbot.farewells:
            print(f"\n{chatbot.name}: Goodbye! Thank you for using FloatChat.")
            break
        
        response = chatbot.generate_response(user_input)
        print(f"\n{chatbot.name}: {response}")

if __name__ == "__main__":
    main()