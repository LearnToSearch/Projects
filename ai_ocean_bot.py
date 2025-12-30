import random
import re
import numpy as np
from datetime import datetime
from collections import defaultdict
import math

class AdvancedOceanChatbot:
    def __init__(self):
        self.name = "FloatChat ARGO AI Assistant"
        self.ocean_data = self.initialize_ocean_data()
        self.marine_life = self.initialize_marine_life()
        self.conservation_data = self.initialize_conservation_data()
        self.climate_data = self.initialize_climate_data()
        self.human_impact_data = self.initialize_human_impact_data()
        
        # Conversation history for context
        self.conversation_history = []
        
        # Initialize keyword patterns for intent recognition
        self.initialize_keyword_patterns()
        
        print(f"{self.name} initialized. Ready to answer your ocean-related questions!")
    
    def initialize_keyword_patterns(self):
        """Initialize patterns for intent recognition"""
        self.keyword_patterns = {
            'greeting': [r'hello', r'hi', r'hey', r'greetings', r'howdy'],
            'farewell': [r'bye', r'goodbye', r'see you', r'farewell', r'quit', r'exit'],
            'ocean_info': [r'pacific', r'atlantic', r'indian', r'southern', r'arctic', r'ocean'],
            'marine_life': [r'fish', r'species', r'marine', r'coral', r'whale', r'dolphin', 
                           r'shark', r'plankton', r'krill', r'seal', r'penguin'],
            'climate': [r'climate', r'warming', r'temperature', r'change', r'current', r'el nino',
                       r'la nina', r'weather', r'co2', r'carbon'],
            'conservation': [r'conservation', r'protect', r'endangered', r'threat', r'pollution',
                            r'plastic', r'overfishing', r'sustainable', r'preserve'],
            'human_impact': [r'human', r'impact', r'fishing', r'pollution', r'tourism', r'shipping',
                            r'mining', r'offshore', r'drilling'],
            'scientific': [r'data', r'research', r'study', r'science', r'scientific', r'argo',
                          r'float', r'measurement', r'experiment'],
            'geography': [r'location', r'where', r'coordinates', r'area', r'size', r'depth',
                         r'trench', r'ridge', r'basin'],
            'chemistry': [r'salinity', r'oxygen', r'ph', r'acidification', r'nutrient', r'chemical',
                         r'composition', r'element'],
            'physics': [r'current', r'wave', r'tide', r'pressure', r'density', r'circulation',
                       r'gyre', r'upwelling', r'thermocline']
        }
    
    def initialize_ocean_data(self):
        """Initialize comprehensive ocean data"""
        # This would be expanded with real data in a production system
        return {
            "pacific": {
                "name": "Pacific Ocean",
                "temperature": {"surface": "22.5°C", "deep": "1-4°C", "trend": "+0.12°C/decade"},
                "salinity": "34.7 PSU average",
                "oxygen": {"surface": "6.2 mg/L", "deep": "4.5 mg/L", "trend": "-0.5%/decade"},
                "ph": {"surface": "8.05", "trend": "-0.02/decade"},
                "currents": ["Kuroshio Current", "California Current", "Humboldt Current", "East Australian Current"],
                "depth": {"average": "4,280m", "max": "10,911m (Challenger Deep, Mariana Trench)"},
                "area": "165,250,000 km²",
                "volume": "710,000,000 km³",
                "coordinates": "0°N 160°W (approximate center)",
                "countries": ["USA", "Canada", "Mexico", "Japan", "Australia", "China", "Chile", "Peru"],
                "facts": [
                    "Largest and deepest ocean, covering about 30% of Earth's surface",
                    "Home to the Great Barrier Reef, the world's largest coral reef system",
                    "Contains the Mariana Trench, the deepest point on Earth"
                ],
                "biodiversity": "High - contains about 50% of the world's marine species",
                "data_source": "ARGO Float Network, NOAA, UNESCO-IOC"
            },
            # Similar data structures for other oceans...
        }
    
    def initialize_marine_life(self):
        """Initialize marine life database"""
        return {
            "pacific": {
                "mammals": ["Blue Whale", "Humpback Whale", "Orca", "Dolphins", "Sea Otters"],
                "fish": ["Pacific Salmon", "Tuna", "Halibut", "Sardines", "Anchovies"],
                "invertebrates": ["Giant Pacific Octopus", "Jellyfish", "Krill", "Crab", "Shrimp"],
                "corals": ["Great Barrier Reef Corals", "Coral Polyps", "Sea Anemones"],
                "plants": ["Kelp Forests", "Phytoplankton", "Sea Grasses"],
                "endangered": ["Blue Whale", "Sea Otter", "Leatherback Turtle"]
            },
            # Similar data for other oceans...
        }
    
    def initialize_conservation_data(self):
        """Initialize conservation issues data"""
        return {
            "pollution": {
                "plastic": "8 million tons of plastic enter oceans yearly",
                "chemical": "Industrial runoff and oil spills harm marine ecosystems",
                "noise": "Shipping and sonar disrupt marine mammal communication"
            },
            "overfishing": {
                "status": "90% of global fish stocks are overfished or fully exploited",
                "impact": "Disrupts food webs and marine ecosystem balance"
            },
            "habitat_destruction": {
                "coral_reefs": "50% of coral reefs have been lost in last 30 years",
                "mangroves": "35% of mangroves have been destroyed",
                "seagrass": "29% of seagrass habitats have disappeared"
            },
            "climate_impact": {
                "coral_bleaching": "Rising temperatures cause coral bleaching events",
                "sea_level_rise": "Threatens coastal habitats and communities",
                "acidification": "Ocean pH has dropped by 0.1 units since industrial revolution"
            }
        }
    
    def initialize_climate_data(self):
        """Initialize climate-related ocean data"""
        return {
            "temperature_trend": "Global ocean surface temperature increased by 0.88°C since 1900",
            "sea_level_rise": "Global mean sea level has risen about 20cm since 1900",
            "acidification": "Ocean pH has decreased by 0.1 units (30% increase in acidity)",
            "current_changes": "Major ocean currents are slowing due to meltwater input",
            "extreme_events": "Increased frequency of marine heatwaves and harmful algal blooms"
        }
    
    def initialize_human_impact_data(self):
        """Initialize human impact data"""
        return {
            "fishing": "Global fish catch peaked at 86 million tons in 1996",
            "shipping": "90% of world trade is carried by sea",
            "tourism": "Coastal tourism generates $ billions annually",
            "mining": "Deep-sea mining threatens unique ecosystems",
            "energy": "Offshore wind and oil extraction impact marine environments"
        }
    
    def detect_intent(self, query):
        """Use pattern matching to detect user intent"""
        query = query.lower()
        intent_scores = defaultdict(int)
        
        for intent, patterns in self.keyword_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    intent_scores[intent] += 1
        
        # Return intent with highest score
        if intent_scores:
            return max(intent_scores.items(), key=lambda x: x[1])[0]
        return "general"
    
    def get_sentiment(self, query):
        """Simple sentiment analysis"""
        positive_words = ['love', 'great', 'awesome', 'amazing', 'beautiful', 'wonderful']
        negative_words = ['hate', 'terrible', 'awful', 'disgusting', 'sad', 'worried']
        
        query = query.lower()
        positive_count = sum(1 for word in positive_words if word in query)
        negative_count = sum(1 for word in negative_words if word in query)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        return "neutral"
    
    def generate_ocean_facts(self, ocean_name):
        """Generate interesting facts about an ocean"""
        if ocean_name not in self.ocean_data:
            return "I don't have detailed information about that ocean."
        
        data = self.ocean_data[ocean_name]
        facts = [
            f"The {data['name']} is the world's {['largest', 'second largest', 'third largest', 'fourth largest', 'smallest'][['pacific', 'atlantic', 'indian', 'southern', 'arctic'].index(ocean_name)]} ocean.",
            f"It has an average depth of {data['depth']['average']} and reaches {data['depth']['max']} at its deepest point.",
            f"Surface temperatures average {data['temperature']['surface']} with a warming trend of {data['temperature']['trend']}.",
            f"Ocean acidification is occurring at a rate of {data['ph']['trend']} pH units per decade.",
            f"Oxygen levels have been declining at a rate of {data['oxygen']['trend']} in recent decades.",
            f"Major currents include: {', '.join(data['currents'][:3])}."
        ]
        
        return " ".join(facts)
    
    def answer_scientific_question(self, query):
        """Answer scientific questions about the ocean"""
        query = query.lower()
        
        if any(word in query for word in ['acid', 'ph']):
            return ("Ocean acidification is the ongoing decrease in the pH of the Earth's oceans, "
                   "caused by the uptake of carbon dioxide (CO₂) from the atmosphere. "
                   "Since the Industrial Revolution, the pH of surface ocean waters has fallen by 0.1 pH units, "
                   "representing a 30% increase in acidity. This affects marine organisms, particularly those "
                   "with calcium carbonate shells or skeletons like corals and shellfish.")
        
        elif any(word in query for word in ['current', 'circulation', 'gyre']):
            return ("Ocean currents are driven by wind, water density differences, and tides. "
                   "Major surface currents form large circular patterns called gyres. "
                   "The thermohaline circulation is a deep-ocean current driven by differences in water density "
                   "caused by temperature (thermo) and salinity (haline). This 'global conveyor belt' plays a "
                   "crucial role in regulating Earth's climate.")
        
        elif any(word in query for word in ['temperature', 'warming', 'heat']):
            return ("The ocean has absorbed more than 90% of the excess heat trapped by greenhouse gases. "
                   "Sea surface temperatures have increased by approximately 0.88°C since 1900. "
                   "Marine heatwaves have become more frequent and intense, causing coral bleaching and "
                   "disrupting marine ecosystems.")
        
        elif any(word in query for word in ['salinity', 'salt']):
            return ("Ocean salinity varies by region, with higher salinity in subtropical regions where "
                   "evaporation exceeds precipitation, and lower salinity near the equator and poles where "
                   "rainfall and meltwater dilute seawater. The average ocean salinity is about 35 parts per thousand. "
                   "Changes in salinity patterns can indicate shifts in the global water cycle.")
        
        return "I need more specific details to answer your scientific question about the ocean."
    
    def answer_conservation_question(self, query):
        """Answer conservation-related questions"""
        query = query.lower()
        
        if any(word in query for word in ['plastic', 'pollution']):
            return ("Plastic pollution is a major threat to marine environments. An estimated 8 million metric tons "
                   "of plastic enter the ocean each year. Plastic debris harms marine life through entanglement and "
                   "ingestion. Microplastics have been found throughout the water column and in marine organisms, "
                   "with unknown long-term effects on ecosystems and human health.")
        
        elif any(word in query for word in ['overfish', 'fishing']):
            return ("Overfishing occurs when fish are caught faster than they can reproduce. According to the UN FAO, "
                   "about 90% of global fish stocks are either overfished or fully exploited. Sustainable fishing "
                   "practices, marine protected areas, and consumer awareness are important solutions to this problem.")
        
        elif any(word in query for word in ['coral', 'reef']):
            return ("Coral reefs are among the most biodiverse ecosystems on Earth, but they are severely threatened. "
                   "About 50% of the world's coral reefs have been lost in the last 30 years due to climate change, "
                   "pollution, overfishing, and disease. Coral bleaching events have become more frequent and severe "
                   "as ocean temperatures rise.")
        
        elif any(word in query for word in ['protect', 'conservation', 'save']):
            return ("There are many ways to help protect the ocean: reduce plastic use, choose sustainable seafood, "
                   "support marine protected areas, reduce carbon footprint, avoid products that harm marine life, "
                   "and support organizations working on ocean conservation. Individual actions combined with policy "
                   "changes can make a significant difference.")
        
        return "I need more specific details to answer your conservation question about the ocean."
    
    def answer_marine_life_question(self, query):
        """Answer questions about marine life"""
        query = query.lower()
        
        if any(word in query for word in ['whale']):
            return ("Whales are magnificent marine mammals that play crucial roles in ocean ecosystems. "
                   "Baleen whales like blue whales filter-feed on krill, while toothed whales like orcas hunt fish "
                   "and marine mammals. Many whale species were brought to near extinction by commercial whaling "
                   "but some populations are recovering thanks to international protection efforts.")
        
        elif any(word in query for word in ['shark']):
            return ("Sharks are ancient predators that have existed for over 400 million years. Contrary to popular "
                   "belief, most shark species are not dangerous to humans. Sharks play vital roles as apex predators "
                   "in maintaining healthy ocean ecosystems. Many shark populations are declining due to overfishing, "
                   "particularly for the shark fin trade.")
        
        elif any(word in query for word in ['coral']):
            return ("Corals are marine invertebrates that form colonies. Each coral polyp is a tiny animal that secretes "
                   "a hard exoskeleton of calcium carbonate. Coral reefs are built by many such polyps over thousands of years. "
                   "Corals have a symbiotic relationship with photosynthetic algae called zooxanthellae, which provide them with energy.")
        
        elif any(word in query for word in ['plankton']):
            return ("Plankton are small organisms that drift in ocean currents. Phytoplankton are microscopic plants that "
                   "perform photosynthesis, producing about 50% of the world's oxygen. Zooplankton are tiny animals that feed "
                   "on phytoplankton. Together, they form the base of most marine food webs.")
        
        return "I need more specific details to answer your question about marine life."
    
    def generate_response(self, query):
        """Generate a response to a user query using AI techniques"""
        # Store conversation history for context
        self.conversation_history.append(("user", query))
        
        # Clean and preprocess query
        clean_query = query.lower().strip()
        
        # Detect intent and sentiment
        intent = self.detect_intent(clean_query)
        sentiment = self.get_sentiment(clean_query)
        
        # Handle greetings
        if intent == "greeting":
            responses = [
                "Hello! I'm FloatChat, your AI assistant for ocean science and conservation.",
                "Hi there! I'm here to answer your questions about the world's oceans.",
                "Greetings! I'm an AI specialized in oceanography and marine science."
            ]
            response = random.choice(responses)
        
        # Handle farewells
        elif intent == "farewell":
            responses = [
                "Goodbye! Thank you for learning about our oceans with me.",
                "Farewell! Remember that every action counts in protecting our marine environments.",
                "See you later! Feel free to return with more questions about ocean science."
            ]
            response = random.choice(responses)
        
        # Handle scientific questions
        elif intent == "scientific":
            response = self.answer_scientific_question(clean_query)
        
        # Handle conservation questions
        elif intent == "conservation":
            response = self.answer_conservation_question(clean_query)
        
        # Handle marine life questions
        elif intent == "marine_life":
            response = self.answer_marine_life_question(clean_query)
        
        # Handle ocean information requests
        elif intent == "ocean_info":
            # Detect which ocean is mentioned
            ocean_mentioned = None
            for ocean in ["pacific", "atlantic", "indian", "southern", "arctic"]:
                if ocean in clean_query:
                    ocean_mentioned = ocean
                    break
            
            if ocean_mentioned:
                response = self.generate_ocean_facts(ocean_mentioned)
            else:
                response = "I can tell you about the Pacific, Atlantic, Indian, Southern, or Arctic Ocean. Which one interests you?"
        
        # Handle general questions with contextual awareness
        else:
            # Check if this continues previous conversation
            if len(self.conversation_history) > 1:
                prev_query = self.conversation_history[-2][1].lower()
                
                # Continue previous topic if relevant
                if "ocean" in prev_query or "marine" in prev_query:
                    if "why" in clean_query or "how" in clean_query:
                        response = "That's an excellent follow-up question. The mechanisms behind ocean phenomena are fascinating and often involve complex interactions between physical, chemical, and biological processes."
                    else:
                        response = "Would you like me to elaborate on any specific aspect of ocean science or conservation?"
                else:
                    response = "I'm not sure I understand. Could you rephrase your question about the ocean?"
            else:
                # Default response for unclear queries
                response = ("I'm an AI assistant specialized in ocean science. I can help with questions about "
                          "marine life, ocean conservation, climate impacts, marine ecosystems, and scientific "
                          "research. What would you like to know about our oceans?")
        
        # Add sentiment-aware closing
        if sentiment == "positive":
            closings = ["I share your enthusiasm for ocean conservation!", 
                       "It's wonderful to see your interest in marine science!",
                       "Your curiosity about the ocean is inspiring!"]
            response += " " + random.choice(closings)
        elif sentiment == "negative":
            closings = ["I understand your concerns about ocean health. There are many ways to help!",
                       "It's normal to feel worried about ocean challenges, but there's hope through collective action.",
                       "Many people share your concerns, which is why ocean conservation efforts are growing worldwide."]
            response += " " + random.choice(closings)
        
        # Store response in history
        self.conversation_history.append(("assistant", response))
        
        # Keep history manageable
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        return response

def main():
    """Main function to run the advanced chatbot"""
    chatbot = AdvancedOceanChatbot()
    
    print("=" * 70)
    print("Advanced FloatChat - ARGO Ocean Data AI Assistant")
    print("=" * 70)
    print("I can answer complex questions about:")
    print("- Ocean science and marine biology")
    print("- Climate change impacts on oceans")
    print("- Marine conservation and sustainability")
    print("- Oceanography and marine research")
    print("- Human impacts on marine ecosystems")
    print("Type 'quit' or 'exit' to end the conversation")
    print("=" * 70)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print(f"\n{chatbot.name}: Thank you for chatting about our oceans. Goodbye!")
                break
            
            response = chatbot.generate_response(user_input)
            print(f"\n{chatbot.name}: {response}")
            
        except KeyboardInterrupt:
            print(f"\n\n{chatbot.name}: Session ended. Thank you for using FloatChat!")
            break
        except Exception as e:
            print(f"\n{chatbot.name}: I encountered an error. Please try rephrasing your question.")
            # print(f"Error: {e}")  # Uncomment for debugging

if __name__ == "__main__":
    main()