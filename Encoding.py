class Encoding:
    @staticmethod
    def Encrypt(s, key)->str:
        encoded_bytes=[ord(char)+i+ key for i, char in enumerate(s)]
        enc_s=".".join(map(str, encoded_bytes))
        enc_s= Encoding.ENCS_TRANS(enc_s)
        return enc_s
    @staticmethod
    def ENCS_TRANS(s: str) -> str:
        """
        Transposes the encoded string. Currently reverses the order of components.
        """
        split_string = s.split(".")
        transposed = ".".join(split_string[::-1])  # Reverse the list and join with "."
        return transposed

# Example usage:
"""if __name__ == "__main__":
    original_string = "hello"
    encoded_string = Encoding.Encrypt(original_string)
    print(f"Original: {original_string}")
    print(f"Encoded: {encoded_string}")"""