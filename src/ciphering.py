import logger


logger = logger.build_logger('ciphering')


def generate_public_key_vector(private_key_vector, modulo, multiplicative_to_mask):
    """
    :param private_key_vector:
    :param modulo:
    :param multiplicative_to_mask:
    :return: public key vector which is generated from private key vector, modulo and multiplicative
    """
    cipher_matrix = list()
    for i in range(0, len(private_key_vector)):
        private_key = private_key_vector[i]
        cipher_item = (private_key*multiplicative_to_mask) % modulo
        cipher_matrix.append(cipher_item)

    return cipher_matrix


def cipher_with_bit_sequences(public_key_vector, bit_sequences):
    """
    :param public_key_vector:
    :param bit_sequences:
    :return: list of ciphered item(sum) which equals to bit*public_key_vector_item one-by-one matched indexes
    """
    ciphered_items = list()
    for i in range(0, len(bit_sequences)):
        ciphered_item = 0
        bit_sequence = bit_sequences[i]
        for k in range(0, len(bit_sequence)):
            bit_item = int(bit_sequence[k])
            cipher_matrix_item = public_key_vector[k]
            ciphered_item += bit_item*cipher_matrix_item
        ciphered_items.append(ciphered_item)

    return ciphered_items
