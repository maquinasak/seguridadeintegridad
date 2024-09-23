import pytest

def str_len(theStr):
    return len(theStr)

def test_string_length():
    caracteres = ["1","ds","tre","cuat","cinco"]    
    for idx,valor in enumerate(caracteres):
        print(valor,idx,str_len(valor))
        result = str_len(valor)
        assert result == (idx+1)


