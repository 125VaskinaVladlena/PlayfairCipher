class PlayfairCipher:
    def __init__(self, key):
        self.size = 5
        self.alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # J заменена на I
        self.key_table = self.generate_key_table(key)
        
    def generate_key_table(self, key):
        key = key.upper().replace('J', 'I')
        key_letters = []
        for ch in key:
            if ch in self.alphabet and ch not in key_letters:
                key_letters.append(ch)
        for ch in self.alphabet:
            if ch not in key_letters:
                key_letters.append(ch)
        
        table = [key_letters[i*self.size:(i+1)*self.size] for i in range(self.size)]
        return table

    def find_position(self, ch):
        for row in range(self.size):
            for col in range(self.size):
                if self.key_table[row][col] == ch:
                    return (row, col)
        return None
    
    def process_text(self, text):
        text = text.upper().replace('J', 'I')
        filtered = [c for c in text if c in self.alphabet]
        result = []
        i = 0
        while i < len(filtered):
            a = filtered[i]
            if i + 1 < len(filtered):
                b = filtered[i + 1]
                if a == b:
                    # Вставляем X между повторяющимися буквами
                    b = 'X'
                    i += 1
                else:
                    i += 2
            else:
                b = 'X'
                i += 1
            result.append(a)
            result.append(b)
        bigrams = [(result[i], result[i + 1]) for i in range(0, len(result), 2)]
        return bigrams

    def encrypt_pair(self, a, b):
        row1, col1 = self.find_position(a)
        row2, col2 = self.find_position(b)

        if row1 == row2:
            col1 = (col1 + 1) % self.size
            col2 = (col2 + 1) % self.size
        elif col1 == col2:
            row1 = (row1 + 1) % self.size
            row2 = (row2 + 1) % self.size
        else:
            col1, col2 = col2, col1
        
        return self.key_table[row1][col1] + self.key_table[row2][col2]

    def decrypt_pair(self, a, b):
        row1, col1 = self.find_position(a)
        row2, col2 = self.find_position(b)

        if row1 == row2:
            col1 = (col1 - 1) % self.size
            col2 = (col2 - 1) % self.size
        elif col1 == col2:
            row1 = (row1 - 1) % self.size
            row2 = (row2 - 1) % self.size
        else:
            col1, col2 = col2, col1
        
        return self.key_table[row1][col1] + self.key_table[row2][col2]

    def encrypt(self, text):
        bigrams = self.process_text(text)
        encrypted = [self.encrypt_pair(a, b) for a, b in bigrams]
        return ''.join(encrypted)

    def clean_decrypted_text(self, text):
        result = []
        i = 0
        while i < len(text):
            result.append(text[i])
            # Удаляем 'X', вставленные между повторяющимися буквами
            if (i + 2 < len(text) and
                text[i] == text[i + 2] and
                text[i + 1] == 'X'):
                i += 2
            else:
                i += 1
        # Удаляем последний символ 'X', если он лишний
        if result[-1] == 'X':
            result.pop()
        return ''.join(result)

    def decrypt(self, text):
        text = text.upper().replace('J', 'I')
        bigrams = [(text[i], text[i + 1]) for i in range(0, len(text), 2)]
        decrypted = [self.decrypt_pair(a, b) for a, b in bigrams]
        raw_text = ''.join(decrypted)
        clean_text = self.clean_decrypted_text(raw_text)
        return clean_text