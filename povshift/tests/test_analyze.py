import unittest

from povshift.detector import POVShiftDetector


class TestAnalyzeStage(unittest.TestCase):
    def setUp(self):
        self.detector = POVShiftDetector()

    def test_tc_01_simple_clause(self):
        clauses = self.detector.analyze("John opened the door.")

        self.assertEqual(len(clauses), 1)
        self.assertEqual(clauses[0].text, "John opened the door.")
        self.assertEqual(clauses[0].sentence_index, 0)
        self.assertIsNotNone(clauses[0].subject)
        self.assertEqual(clauses[0].subject.canonical_name, "John")
        self.assertEqual(clauses[0].verb, "open")

    def test_tc_02_multiple_sentences(self):
        clauses = self.detector.analyze("John opened the door. Mary entered.")

        self.assertEqual(len(clauses), 2)
        self.assertEqual(clauses[0].sentence_index, 0)
        self.assertEqual(clauses[1].sentence_index, 1)
        self.assertEqual(clauses[0].subject.canonical_name, "John")
        self.assertEqual(clauses[1].subject.canonical_name, "Mary")
        self.assertEqual(clauses[0].verb, "open")
        self.assertEqual(clauses[1].verb, "enter")

    def test_tc_03_empty_text(self):
        with self.assertRaises(ValueError):
            self.detector.analyze("")

    def test_tc_04_coreference(self):
        clauses = self.detector.analyze("John entered the room. He sat down.")
        resolved = self.detector.resolve_coreference(clauses)

        self.assertEqual(resolved[1].subject.canonical_name, "John")
        self.assertEqual(resolved[1].subject.mentions, ["John", "He"])

    def test_tc_05_female_coreference(self):
        clauses = self.detector.analyze("Mary entered the room. She sat down.")
        resolved = self.detector.resolve_coreference(clauses)

        self.assertEqual(resolved[1].subject.canonical_name, "Mary")
        self.assertEqual(resolved[1].subject.mentions, ["Mary", "She"])

    def test_tc_06_ambiguous_coreference(self):
        clauses = self.detector.analyze("John met Paul. He smiled.")
        resolved = self.detector.resolve_coreference(clauses)

        self.assertIsNone(resolved[1].subject)

    def test_tc_07_cognitive_state(self):
        clauses = self.detector.analyze("John wondered where Mary was.")
        enriched = self.detector.detect_internal_states(clauses)

        self.assertTrue(enriched[0].internal_state)
        self.assertEqual(enriched[0].state_type, "cognition")
        self.assertEqual(enriched[0].experiencer.canonical_name, "John")

    def test_tc_08_emotional_state(self):
        clauses = self.detector.analyze("Mary felt afraid.")
        enriched = self.detector.detect_internal_states(clauses)

        self.assertTrue(enriched[0].internal_state)
        self.assertEqual(enriched[0].state_type, "emotion")
        self.assertEqual(enriched[0].experiencer.canonical_name, "Mary")

    def test_tc_09_observable_action(self):
        clauses = self.detector.analyze("John opened the door.")
        enriched = self.detector.detect_internal_states(clauses)

        self.assertFalse(enriched[0].internal_state)
        self.assertIsNone(enriched[0].state_type)
        self.assertIsNone(enriched[0].experiencer)

    def test_tc_10_initial_focus(self):
        clauses = self.detector.analyze("John wondered about Mary.")
        resolved = self.detector.resolve_coreference(clauses)
        enriched = self.detector.detect_internal_states(resolved)
        focus = self.detector.update_focus(enriched)

        self.assertEqual(focus[0].character.canonical_name, "John")

    def test_tc_11_same_focus_through_coreference(self):
        clauses = self.detector.analyze("John wondered about Mary. He felt nervous.")
        resolved = self.detector.resolve_coreference(clauses)
        enriched = self.detector.detect_internal_states(resolved)
        focus = self.detector.update_focus(enriched)

        self.assertEqual(focus[0].character.canonical_name, "John")
        self.assertEqual(focus[1].character.canonical_name, "John")

    def test_tc_12_focus_change(self):
        clauses = self.detector.analyze("John wondered about Mary. Mary knew he was waiting.")
        resolved = self.detector.resolve_coreference(clauses)
        enriched = self.detector.detect_internal_states(resolved)
        focus = self.detector.update_focus(enriched)

        self.assertEqual(focus[0].character.canonical_name, "John")
        self.assertEqual(focus[1].character.canonical_name, "Mary")

    def test_tc_13_clear_pov_shift(self):
        shifts = self.detector.detect("John wondered where Mary was. Mary knew he was waiting.")

        self.assertEqual(len(shifts), 1)
        self.assertEqual(shifts[0].from_character.canonical_name, "John")
        self.assertEqual(shifts[0].to_character.canonical_name, "Mary")

    def test_tc_14_no_pov_shift_with_coreference(self):
        shifts = self.detector.detect("John wondered where Mary was. He knew she was coming.")

        self.assertEqual(shifts, [])

    def test_tc_15_character_change_without_pov_shift(self):
        shifts = self.detector.detect("John opened the door. Mary entered.")

        self.assertEqual(shifts, [])

    def test_tc_16_person_shift_without_internal_state(self):
        shifts = self.detector.detect("I opened the door. You closed it.")

        self.assertEqual(shifts, [])

    def test_tc_17_person_shift_with_internal_state(self):
        shifts = self.detector.detect("I felt nervous. You felt angry.")

        self.assertEqual(len(shifts), 1)
        self.assertEqual(shifts[0].from_character.canonical_name, "I")
        self.assertEqual(shifts[0].to_character.canonical_name, "You")

    def test_tc_22_multiple_clauses_same_sentence(self):
        clauses = self.detector.analyze("John opened the door and Mary felt afraid.")

        self.assertEqual(len(clauses), 2)
        self.assertEqual(clauses[0].sentence_index, 0)
        self.assertEqual(clauses[1].sentence_index, 0)
        self.assertEqual(clauses[0].subject.canonical_name, "John")
        self.assertEqual(clauses[1].subject.canonical_name, "Mary")
        self.assertFalse(clauses[0].internal_state)
        self.assertFalse(clauses[1].internal_state)


if __name__ == "__main__":
    unittest.main()
