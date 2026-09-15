import unittest

from povshift.domain import Character, Clause, FocusState, POVShift


class TestDomainModel(unittest.TestCase):
    def test_character_identity_and_mentions(self):
        john = Character(
            id=1,
            canonical_name="John",
            mentions=["John", "he"],
        )

        self.assertEqual(john.id, 1)
        self.assertEqual(john.canonical_name, "John")
        self.assertEqual(john.mentions, ["John", "he"])

    def test_clause_captures_internal_state_and_experiencer(self):
        mary = Character(
            id=2,
            canonical_name="Mary",
            mentions=["Mary", "she"],
        )

        clause = Clause(
            text="Mary felt afraid.",
            sentence_index=0,
            subject=mary,
            verb="feel",
            internal_state=True,
            state_type="emotion",
            experiencer=mary,
        )

        self.assertTrue(clause.internal_state)
        self.assertEqual(clause.state_type, "emotion")
        self.assertEqual(clause.experiencer, mary)
        self.assertEqual(clause.subject, mary)
        self.assertEqual(clause.verb, "feel")

    def test_focus_state_tracks_sentence_focus(self):
        john = Character(
            id=1,
            canonical_name="John",
            mentions=["John"],
        )

        focus_state = FocusState(
            character=john,
            sentence_index=0,
            reason="internal_state",
        )

        self.assertEqual(focus_state.character, john)
        self.assertEqual(focus_state.sentence_index, 0)
        self.assertEqual(focus_state.reason, "internal_state")

    def test_pov_shift_tracks_change_and_confidence(self):
        john = Character(
            id=1,
            canonical_name="John",
            mentions=["John"],
        )
        mary = Character(
            id=2,
            canonical_name="Mary",
            mentions=["Mary"],
        )

        shift = POVShift(
            from_character=john,
            to_character=mary,
            sentence_index=1,
            confidence=0.91,
            evidence=["focus_changed", "different_experiencer", "internal_state"],
        )

        self.assertEqual(shift.from_character, john)
        self.assertEqual(shift.to_character, mary)
        self.assertEqual(shift.sentence_index, 1)
        self.assertGreaterEqual(shift.confidence, 0.0)
        self.assertLessEqual(shift.confidence, 1.0)
        self.assertIn("focus_changed", shift.evidence)


if __name__ == "__main__":
    unittest.main()
