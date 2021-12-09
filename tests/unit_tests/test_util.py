from hit_processing.util import subtract_lists


def test_subtract_lists():
    """ GIVEN two different lists with some overlapping elements
        WHEN subtract_list(list1, list2) is called
        THEN result should be elements from list1 not present in list2
    """
    list1 = ["a", "b", "c", "dd", "eee"]
    list2 = ["b", "dd"]

    difference = subtract_lists(list1, list2)

    assert set(difference) == {"a", "c", "eee"}
