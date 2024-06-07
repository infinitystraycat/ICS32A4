from Profile import Profile

from ds_messenger import DirectMessenger

PORT = 3021
HOST = '168.235.86.101'

def test_dm():
    dm = DirectMessenger(HOST, 'may', 'pwd')
    prof = Profile()
    PATHN = 'c:/Users/straycat/OneDrive/Desktop/ICS32Class/a4code/testfile.dsu'
    prof.load_profile(PATHN)
    newlist = dm.get_all_from_friend('testmay')
    print(newlist)
    assert newlist is not None
