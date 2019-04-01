import sys
from configparser import ConfigParser
from Rotor import Rotor
from Plugboard import PlugBoard

'''
Basic emulator of a "simple" three-rotor Enigma machine.
This is based extensively on the model and sample C emulator published by
Harald Schmidt of the Miami College of Arts and Sciences
(http://www.cs.miami.edu/home/harald/enigma/index.html)

This code just encodes/decodes the given message.
'''
class Enigma():
    def __init__(self, settings):
        self.rotor1 = Rotor(settings['rotors']['rotor1'],
                            settings['rotors']['rotor1Pos'],
                            settings['rotors']['rotor1Ring'])
        self.rotor2 = Rotor(settings['rotors']['rotor2'],
                            settings['rotors']['rotor2Pos'],
                            settings['rotors']['rotor2Ring'])
        self.rotor3 = Rotor(settings['rotors']['rotor3'],
                            settings['rotors']['rotor3Pos'],
                            settings['rotors']['rotor3Ring'])
        self.reflector = Rotor('RFL')

        self.plugboard = PlugBoard(settings['plugboard'])

        assert self.rotor1.id != self.rotor2.id and \
               self.rotor1.id != self.rotor3.id and \
               self.rotor2.id != self.rotor3.id, \
            "Identical rotors may not be used in one machine"

    '''
    Advance the rotors so that the first runs through all 26 settings before 
        advancing the second, which advances the third when it has completed
        all 26 settings. (Like individual digits in an odometer)
    '''
    def advanceRotors(self):
        self.rotor1.advance()
        if self.rotor1.position == 0:
            self.rotor2.advance()
            if self.rotor2.position == 0:
                self.rotor3.advance()

    '''
    The encoding runs through the plugboard, the three rotors, the reflector,
        back through the rotors in reverse order, and back out the plugboard.
        
        1.) Map the character to its setting in the plugboard
        2.) Advance the rotors before continuing.
        3.) Map that character to its setting in each rotor, from 1 to 3.
        4.) Map that character to it setting in the Reflector.
        5.) Map that character to its reverse setting in each rotor from 3 to 1.
        6.) Map that character to its setting in the plugboard
    
        Note that rotors are numbered so that rotor 1 is the first encountered in
        the encoding (notionally, "right to left")
    '''
    def encodeChar(self, inch):
        assert inch.isalpha()

        # Swap input character with plugboard setting
        ch = self.plugboard.getWiring(inch.upper())
        self.advanceRotors()

        # Forward Rotor encodings
        outch = self.rotor1.forwardEncode(ch)
        outch = self.rotor2.forwardEncode(outch)
        outch = self.rotor3.forwardEncode(outch)

        # Reflector encoding
        outch = self.reflector.forwardEncode(outch)

        # Reverse Rotor encodings
        outch = self.rotor3.backwardEncode(outch)
        outch = self.rotor2.backwardEncode(outch)
        outch = self.rotor1.backwardEncode(outch)

        # Final swap with plugboard settings
        outch = self.plugboard.getWiring(outch)

        # Validate no character ever codes to itself
        assert outch != inch.upper()
        # self.advanceRotors()

        return outch

    def encode(self, str):
        outstr = ''
        for c in str:
            outstr += self.encodeChar(c)

        return outstr

    def makeConfig(self, outfile):
        config = ConfigParser()
        config['rotors'] = {}
        with config['rotors'] as rSet:
            rSet['rotor1'] = self.rotor1.id
            rSet['rotor2'] = self.rotor2.id
            rSet['rotor3'] = self.rotor3.id
            rSet['rotor1Pos'] = self.rotor1.position
            rSet['rotor2Pos'] = self.rotor2.position
            rSet['rotor3Pos'] = self.rotor3.position
            rSet['rotor1Ring'] = self.rotor1.ring
            rSet['rotor2Ring'] = self.rotor2.ring
            rSet['rotor3Ring'] = self.rotor3.ring

        config.write(outfile)

if __name__ == '__main__':
    c = ConfigParser()
    with open('config.ini', 'r') as f:
        c.read_file(f)
    e = Enigma(c)

    print("Input the message to be encoded")
    print("Only alphabetic values, without spaces or punctuation, are accepted.\n")
    print("Hit return without typing any message to exit.\n")

    while True:
        inmsg = input("Message --> ")
        msg = ''
        if len(inmsg) == 0:
            sys.exit()

        for c in inmsg:
            if c.isalpha():
                msg += c.upper()

        print(e.encode(msg))
