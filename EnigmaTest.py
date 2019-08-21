import unittest
from configparser import ConfigParser
from Enigma import Enigma


class TestEnigma(unittest.TestCase):
    def createConfig(self):
        config = ConfigParser()
        config['rotors'] = {}
        config['plugboard'] = {}

        return config

    def createRotorConfig(self):
        config = self.createConfig()
        config['rotors']['rotor1'] = 'i'
        config['rotors']['rotor2'] = 'ii'
        config['rotors']['rotor3'] = 'iii'
        config['rotors']['rotor1Pos'] = '0'
        config['rotors']['rotor2Pos'] = '0'
        config['rotors']['rotor3Pos'] = '0'
        config['rotors']['rotor1Ring'] = '0'
        config['rotors']['rotor2Ring'] = '0'
        config['rotors']['rotor3Ring'] = '0'

        config['plugboard'] = {'a': 'M', 'e': 'T'}

        return config

    def testRotorIds(self):
        e = Enigma(self.createRotorConfig())
        assert e.rotor1.id == 'I', \
            "Failed to assign rotor correctly"

    def testRotorPositions(self):
        e = Enigma(self.createRotorConfig())
        assert e.rotor1.position == 0, \
            "Failed to assign rotor position correctly"

    def testAdvanceRightRotor(self):
        e = Enigma(self.createRotorConfig())
        pos1 = e.rotor1.position
        e.encode('a')
        assert e.rotor1.position == pos1 + 1, \
            "Failed to advance right rotor on encode"

    def testAdvanceMiddleRotor(self):
        e = Enigma(self.createRotorConfig())
        e.rotor1.position = 25
        pos2 = e.rotor2.position
        e.encode('a')
        assert e.rotor2.position == pos2 + 1, \
            "Failed to advance middle rotor on encode"

    def testAdvanceLeftRotor(self):
        e = Enigma(self.createRotorConfig())
        e.rotor1.position = 25
        e.rotor2.position = 25
        pos3 = e.rotor3.position
        e.encode('a')
        assert e.rotor3.position == pos3 + 1, \
            "Failed to advance left rotor on encode"

    def testEncodeSimple(self):
        e = Enigma(self.createRotorConfig())
        str = e.encode('aaa')

        assert str[0] != 'A', "Failed to encode properly"
        assert str[1] != 'A', "Failed to encode properly"
        assert str[2] != 'A', "Failed to encode properly"

        e = Enigma(self.createRotorConfig())
        e = Enigma(self.createRotorConfig())
        str2 = e.encode(str)

        assert str2 == "AAA", "Failed to decode properly"

    def testPlugboardCreation(self):
        e = Enigma(self.createRotorConfig())
        assert e.plugboard.get_wiring('A') == 'M'
        assert e.plugboard.get_wiring('T') == 'E'
        assert e.plugboard.get_wiring('X') == 'X'

    # I was able to verify these encodings against the enigmaco.de emulator,
    # among others, with identical settings.
    #
    # Note that "HELLO" will not necessarily encode to "AMNCZ" with these
    # same settings in other emulators, depending on the wiring of the rotors
    # and other variations. While this matches a few different emulators out
    # there and fits to my very imperfect understanding of how the Enigma
    # worked, I make no claim that the results are historically accurate.
    def testString(self):
        e = Enigma(self.createRotorConfig())
        msg = e.encode('HELLO')

        assert msg == 'AMNCZ', "Encoded large message improperly"

        e = Enigma(self.createRotorConfig())
        decode = e.encode(msg)
        assert decode == 'HELLO', "Decoded large message improperly"


if __name__ == '__main__':
    unittest.main()
