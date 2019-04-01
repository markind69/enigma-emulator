# enigma-emulator
Simple Python emulator of an enigma machine. This is the first step in a toy NLP project I'm working on.


The surprise for me in researching the Enigma machine is that it is fundamentally just an extended version of the old Caesar cipher, in which each character is substituted with another character offset in the alphabet. For example, with an offset of 2, "ABCD" becomes "CDEF". For those who remember spoiler-encodings from back in the days of 1990's Usenet forums, ROT-13 is just a specific instance of a Caesar code.

In a more complex version of the Caesar code, the offset is increased by one, modulo 26 (or whatever the size of your alphabet), for each character encoded. In this instance, with an initial offset of 2, "ABCD" becomes "CEGI", because the offset from "A" is 2, from "B" is 3, and so on. 

For all practical purposes, the Enigma machine does a variation of this, mixed with a simple substitution cipher, but encoded three times in a row across all rotors, further encoded with a simple substitution cipher in the "Reflector". The encoding is then made backwards through the three rotors again. Finally, to further obfuscate the original character, both the input and the output are run through the "plugboard", in which some pairs of characters are swapped. As a character is encoded, the first rotor has its position advanced by one. When any rotor advances past "Z", the next rotor in order is advanced by one.

The sample config file sets up the rotors and plugboard. Each enigma machine made use of three out of five available rotors, arranged in a particular order. In this implementation, "rotor1" is the one the character is encoded through first in the first run, and last after going through the reflector.

Each type of rotor (numbered "I", "II", "III", "IV", and "V") had a different substitution cipher encoding built into it. The "position" setting ("rotor1Pos", "rotor2Pos", and "rotor3Pos") is started at a specific index offset between 0 and 25. (This was actually a letter value in the original machines.) The ring setting was an additional offset setting that could be used against each rotor.

The plugboard was physically a series of plugs corresponding to each letter, each of which could be connected to another letter. As a result, no letter in a pair of connected letters can be connected to another letter. For example, if "A" is connected to "T", then "T" cannot be connected to any other letter. Also note that this means that "A" will be substituted for "T" both in the input and output characters, and also that "T" will be substituted for "A".

If you'd like to comment or let me know of any errors, please post them on the blog entry (https://cheeseandpear.blogspot.com/2019/04/programming-doodle-enigma-emulator.html) or send me an email (elindberg@acm.org). My intention next is to start playing with decrypting strategies, probably focusing on modern NLP tools, rather than trying to mimic the actual methods, such as the Bombe or Banburismus. Though now that I think of it, those might be fun to try as well...
