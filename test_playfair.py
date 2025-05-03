import unittest
from playfair import PlayfairCipher

class TestPlayfairCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = PlayfairCipher('Playfair Example')

    def test_key_table(self):
        expected_table = [
            ['P', 'L', 'A', 'Y', 'F'],
            ['I', 'R', 'E', 'X', 'M'],
            ['B', 'C', 'D', 'G', 'H'],
            ['K', 'N', 'O', 'Q', 'S'],
            ['T', 'U', 'V', 'W', 'Z']
        ]
        self.assertEqual(self.cipher.key_table, expected_table)

    def test_process_text(self):
        text = 'BALLOON'
        bigrams = self.cipher.process_text(text)
        self.assertEqual(bigrams, [('B', 'A'), ('L', 'X'), ('L', 'O'), ('O', 'N')])

    def test_encrypt(self):
        plaintext = "Hide the gold in the tree stump"
        ciphertext = self.cipher.encrypt(plaintext)
        self.assertEqual(ciphertext, "BMODZBXDNABEKUDMUIXMMOUVIF")

    def test_decrypt(self):
        ciphertext = "BMODZBXDNABEKUDMUIXMMOUVIF"
        plaintext = self.cipher.decrypt(ciphertext)
        self.assertTrue(plaintext.startswith("HIDETHEGOLDINTHETREESTUMP"))

if __name__ == '__main__':
    unittest.main()