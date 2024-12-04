class Decrypt:
    @staticmethod
    def DECS(encrypted_string,key):
        # Reverse the transposition
        reversed_string = Decrypt.ENCS_TRANS(encrypted_string)

        # Split the reversed string by "." to get encoded integer values
        split_values = reversed_string.split(".")
        decoded_bytes = []

        # Decode each byte by subtracting its index from the value
        for i, value in enumerate(split_values):
            if value:  # Ignore empty elements
                original_int = int(value) - i-key
                decoded_bytes.append(original_int)

        # Convert byte array back to the original string
        return bytes(decoded_bytes).decode()

    @staticmethod
    def ENCS_TRANS(s):
        # Transposition: reverse the order of values
        split_string = s.split(".")
        reversed_split = list(filter(None, reversed(split_string)))  # Filter out empty strings
        return ".".join(reversed_split) + "."

# Testing the decryption with encrypted input
"""if __name__ == "__main__":
    encrypted = "115.111.110.102.104"  # Example encrypted string
    decrypted = Decrypt.DECS(encrypted)
    print("Decrypted:", decrypted)"""
