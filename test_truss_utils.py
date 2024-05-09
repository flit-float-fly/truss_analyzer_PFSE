import truss_utils as tu

def test_remove_comma():
    test_num = "1,000"
    assert tu.remove_comma(test_num) == 1000

def test_find_span():
    test_txt1 = "SPAN = 4600 mm"
    assert tu.find_span(test_txt1) == "4600"

def test_find_adjacent_numbers():
    numbers = [1, 5, 7, 8, 15]
    target = 11
    assert tu.find_adjacent_numbers(numbers, target) == (8, 15)

def test_isolate_sw():
    test_txt = "12.0\n6.0\n1.21"
    assert tu.isolate_sw(test_txt) == 12.0

def test_model_sw():
    test_len_dict = {"TC":15000,
                 "BC":13125,
                 "Diagonal":2039,
                 "Vertical":800}
    test_type_dict = {"TC":("Double Angle", "3 x 3 x 0.236"),
                 "BC":("Double Angle", "2 1/4 x 2 1/4 x 0.236"),
                 "Diagonal":("Double Angle", "2 1/4 x 2 1/4 x 0.236"),
                 "Vertical":("Round Bar", "5/8")}
    test_n_diag = 8
    test_n_vert = 4
    assert int(tu.model_sw(test_len_dict, test_type_dict, test_n_diag, test_n_vert)) == 497