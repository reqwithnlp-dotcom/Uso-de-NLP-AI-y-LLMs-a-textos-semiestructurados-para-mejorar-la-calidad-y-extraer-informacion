def run_tests():

    # Test 1
    s1 = "The letter was written by Juan."
    assert is_passive(s1) == True

    # Test 2
    s2 = "A bridge was built over the river."
    assert is_passive(s2) == True

    # Test 3
    s3 = "Maria eats an apple."
    assert is_passive(s3) == False

    # Test 4
    s4 = "John plays football."
    assert is_passive(s4) == False

    # Test posiciones
    s5 = "The cake was eaten by Tom."
    positions = passive_positions(s5)

    assert isinstance(positions, list)

    print("✅ TODOS LOS TESTS PASARON")


run_tests()