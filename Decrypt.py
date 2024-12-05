class Decrypt:
    @staticmethod
    def DECS(encrypted_string,key):
        #Returns string to correct order
        decrypted_string = Decrypt.DECS_TRANS(encrypted_string)

        #Subtract the key and index
        decoded_bytes = [(ord(char) - i - key) % 128 for i, char in enumerate(decrypted_string)]

        decrypted_string = ''.join(chr(byte) for byte in decoded_bytes)

        return decrypted_string

    @staticmethod
    def DECS_TRANS(s):
        char_array = list(s)
        middle = len(char_array) // 2
        firstHalf = char_array[:middle]
        secondHalf = char_array[middle:]

        firstHalf.reverse()
        secondHalf.reverse()

        return ''.join(firstHalf) + ''.join(secondHalf)
# Testing the decryption with encrypted input
"""if __name__ == "__main__":
    encrypted = "sA=<4z<CHDK"  # Example encrypted string
    decrypted = Decrypt.DECS(encrypted, 12345678)
    print("Decrypted:", decrypted)"""
