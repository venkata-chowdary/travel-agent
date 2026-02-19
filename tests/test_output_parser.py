import unittest
from schemas.output_parser import PydanticOutputParser
from schemas.itinerary import Itinerary

class TestPydanticOutputParser(unittest.TestCase):
    def setUp(self):
        self.parser = PydanticOutputParser()

    def test_clean_json(self):
        json_str = '{"destination": "Paris", "total_cost": 1000, "flight_details": {"airline": "AirFrance", "flight_number": "AF123", "departure_time": "10:00", "arrival_time": "12:00", "price": 500}, "hotel_details": {"name": "Hotel Paris", "address": "123 Rue de Rivoli", "check_in": "14:00", "check_out": "11:00", "price_per_night": 100, "total_price": 500}, "weather_details": "Sunny", "notes": "Have make a fun trip"}'
        result = self.parser.parse(json_str)
        self.assertIsInstance(result, Itinerary)
        self.assertEqual(result.destination, "Paris")

    def test_markdown_json(self):
        json_str = '```json\n{"destination": "London", "total_cost": 1200, "flight_details": {"airline": "BA", "flight_number": "BA123", "departure_time": "10:00", "arrival_time": "12:00", "price": 600}, "hotel_details": {"name": "Hotel London", "address": "123 Oxford St", "check_in": "14:00", "check_out": "11:00", "price_per_night": 120, "total_price": 600}, "weather_details": "Cloudy", "notes": "Bring an umbrella"}\n```'
        result = self.parser.parse(json_str)
        self.assertIsInstance(result, Itinerary)
        self.assertEqual(result.destination, "London")

    def test_text_surrounded_json(self):
        json_str = 'Here is the itinerary: {"destination": "Rome", "total_cost": 1500, "flight_details": {"airline": "Alitalia", "flight_number": "AZ123", "departure_time": "10:00", "arrival_time": "12:00", "price": 700}, "hotel_details": {"name": "Hotel Rome", "address": "123 Via del Corso", "check_in": "14:00", "check_out": "11:00", "price_per_night": 160, "total_price": 800}, "weather_details": "Hot", "notes": "Wear sunscreen"} Hope you like it!'
        result = self.parser.parse(json_str)
        self.assertIsInstance(result, Itinerary)
        self.assertEqual(result.destination, "Rome")

    def test_malformed_json(self):
        json_str = '{"destination": "Berlin", "total_cost": 1000' # Missing closing brace
        with self.assertRaises(ValueError):
            self.parser.parse(json_str)

if __name__ == '__main__':
    unittest.main()
