import unittest
from src.generation.insight_generator import InsightGenerator

class TestInsightGenerator(unittest.TestCase):

    def setUp(self):
        self.insight_generator = InsightGenerator()

    def test_generate_insights_empty_input(self):
        result = self.insight_generator.generate_insights([])
        self.assertEqual(result, [])

    def test_generate_insights_single_input(self):
        input_data = [{"key": "value"}]
        result = self.insight_generator.generate_insights(input_data)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_generate_insights_multiple_inputs(self):
        input_data = [{"key1": "value1"}, {"key2": "value2"}, {"key3": "value3"}]
        result = self.insight_generator.generate_insights(input_data)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

    def test_generate_insights_invalid_input(self):
        with self.assertRaises(TypeError):
            self.insight_generator.generate_insights("invalid input")

    def test_generate_insights_none_input(self):
        with self.assertRaises(TypeError):
            self.insight_generator.generate_insights(None)

if __name__ == '__main__':
    unittest.main()
