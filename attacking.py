def create_base_vector_list(public_key_vector, ciphered_message):
    """
    :param public_key_vector:
    :param ciphered_message:
    :return: a list which holds public key vector and ciphered_message combined
    """
    result = []
    sub_result = []
    reference_index = 0
    l = len(public_key_vector) + 1
    for i in range(0, l-1):
        for j in range(0, l):
            if j == reference_index:
                sub_result.append(1)
            else:
                sub_result.append(0)
        reference_index += 1
        result.append(sub_result)
        sub_result = []
    sub_result.extend(public_key_vector)
    sub_result.append(ciphered_message*-1)
    result.append(sub_result)

    return result


def get_first_column_as_bit_sequence(n):
    """
    :param n:
    :return: a bit sequence which is first column of the matrix
    """
    result = ""
    for i in n:
        result += str(i[0])

    return result[:-1]
