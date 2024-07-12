#encryption function
def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        encrypted_char = chr((ord(char) + shift) % 256)
        encrypted_text += encrypted_char
    return encrypted_text

#decryption function
def decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        decrypted_char = chr((ord(char) - shift) % 256)
        decrypted_text += decrypted_char
    return decrypted_text
