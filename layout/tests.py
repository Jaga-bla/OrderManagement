from django.test import TestCase
from .models import Contract

class ContractTestCase(TestCase):
    def setUp(self):
        Contract.objects.create(name="lion", sound="roar")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')