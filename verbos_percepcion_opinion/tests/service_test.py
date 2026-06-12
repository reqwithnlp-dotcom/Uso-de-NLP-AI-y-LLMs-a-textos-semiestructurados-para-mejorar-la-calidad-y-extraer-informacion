"""
Basic tests for verbos_percepcion_opinion.service.
"""

import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import app.services.service as service


class TestVerbosPercepcionOpinion(unittest.TestCase):
	def test_oracion1(self):
		resultado = service.detect_opinion_and_perception(
			"I think that this method is not the most suitable."
		)
		self.assertEqual(
			resultado,
			{
				"opinion_perception": ["think"],
				"others": [
					"I",
					"that",
					"this",
					"method",
					"is",
					"not",
					"the",
					"most",
					"suitable",
				],
			},
		)

	def test_oracion2(self):
		resultado = service.detect_opinion_and_perception(
			"María watched the movie and listened to the music."
		)
		self.assertEqual(
			resultado,
			{
				"opinion_perception": [],
				"others": [
					"María",
					"watched",
					"the",
					"movie",
					"and",
					"listened",
					"to",
					"the",
					"music",
				],
			},
		)

	def test_oracion3(self):
		resultado = service.detect_opinion_and_perception("I feel pain in my back.")
		self.assertEqual(
			resultado,
			{
				"opinion_perception": ["feel"],
				"others": ["I", "pain", "in", "my", "back"],
			},
		)

if __name__ == "__main__":
    unittest.main()