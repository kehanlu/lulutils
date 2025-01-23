def caesar_cipher(text, shift, mode="encode"):
    """
    Caesar cipher that preserves upper and lower case letters.
    Non-alphabetic characters remain unchanged.
    """
    def shift_char(char, shift_amount):
        if char.islower():
            return chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a'))
        elif char.isupper():
            return chr((ord(char) - ord('A') + shift_amount) % 26 + ord('A'))
        else:
            return char

    if mode == "encode":
        shift_amount = shift
    elif mode == "decode":
        shift_amount = -shift
    else:
        raise ValueError("Mode must be 'encode' or 'decode'.")

    return "".join(shift_char(char, shift_amount) for char in text)


def caesar_name(name, shift, mode="encode"):
    if mode == "decode":
        shift = -shift
    return name[:3] + caesar_cipher(name[3:], shift, mode="encode")