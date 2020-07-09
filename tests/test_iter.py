from import_pyASBC import pyASBC

def test_asbc_iter_files():
    asbc = pyASBC.Asbc5Iterator()     
    xmlfiles = asbc.iter_files()
    print(list(xmlfiles))
    assert True
