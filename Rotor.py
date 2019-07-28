class Rotor():
    rotorIds = ['I', 'II', 'III', 'IV', 'V', 'RFL']
    #   "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    wirings = [
        "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "ESOVPZJAYQUIRHXLNFTGKDCMWB",
        "VZBRGITYUPSDNHLXAWMJQOFECK",
        "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    ]

    def __init__(self, rotor_id, pos='0', ring='0'):
        self.id = rotor_id.upper()
        assert self.id in self.rotorIds, "unrecognized Rotor ID " + self.id
        rotor_num = self.rotorIds.index(self.id)
        self.wiring = self.wirings[rotor_num]

        self.position = int(pos)
        assert self.position >= 0 and self.position < 26, "Initial position must be between 0 and 25"

        self.ring = int(ring)
        assert self.ring >= 0 and self.ring < 26, "Ring setting must be between 0 and 25"

    def advance(self):
        self.position += 1
        if self.position == 26:
            self.position = 0

    def forward_encode(self, ch):
        assert ch.isalpha()
        ch = ch.upper()
        chidx = ord(ch) - ord('A')
        idx = (chidx + self.position) % 26
        idx = (idx - self.ring) % 26
        # Adjust idx for rings (need to review ring model)
        chidx = ord(self.wiring[idx]) - ord('A')
        chidx = (chidx + self.ring) % 26
        return chr(((chidx - self.position) % 26) + ord('A'))

    def backward_encode(self, ch):
        assert ch.isalpha()
        ch = ch.upper()
        chidx = ord(ch) - ord('A')
        idx = (chidx + self.position) % 26
        idx = (idx - self.ring) % 26
        # Adjust idx for rings (need to review ring model)
        chidx = self.wiring.index(chr(idx + ord('A')))
        chidx = (chidx + self.ring) % 26
        return chr(((chidx - self.position) % 26) + ord('A'))
