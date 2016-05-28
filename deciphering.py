import utility
import constants
import math
import knapsack_solver
import logger


logger = logger.build_logger('deciphering')


def calculate_modular_inverse(alg, n, m):
    """
    :param alg: algorithm  type
    :param n: multiplicative
    :param m: modulo
    :return: modular multiplicative inverse by algorithm
    """
    if alg == constants.algorithm_brute_force:
        return modular_inverse_via_brute_force(n, m)
    elif alg == constants.algorithm_totient:
        return modular_inverse_via_totient(n, m)
    else:
        return -1


def modular_inverse_via_brute_force(n, m):
    """
    :param n:
    :param m:
    :return: modular multiplicative inverse calculated by brute force algorithm
    """
    inverse = 0
    for i in range(1, m):
        if (n*i) % m == 1:
            inverse = i
            break

    return inverse


def modular_inverse_via_totient(n, m):
    """
    :param n:
    :param m:
    :return: modular multiplicative inverse calculated by Extended Euclidean algorithm
    """
    inverse = 0
    g, x, y = extended_greatest_common_divisor(n, m)
    if g != 1:
        raise Exception('Modular inverse does not exist!')
    else:
        inverse = x % m

    return inverse


def phi(n):
    """
    :param n:
    :return: phi function (totient) of n
    """
    phi_response = 0
    for k in range(1, n+1):
        if math.gcd(n, k) == 1:
            phi_response += 1

    return phi_response


def extended_greatest_common_divisor(a, b):
    """
    :param a:
    :param b:
    :return: greatest common divisor of a and b
    """
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_greatest_common_divisor(b % a, a)
        return g, x - (b // a) * y, y


def decipher_vector_elements(ciphered_vector, modulo, multiplicative):
    """
    :param ciphered_vector:
    :param modulo:
    :param multiplicative:
    :return: deciphered vector generated with using ciphered item and the modular inverse of initial mod and key
    """
    deciphered_vector = list()
    multiplicative_inverse = calculate_modular_inverse(constants.algorithm_totient, multiplicative, modulo)
    for i in range(0, len(ciphered_vector)):
        ciphered_item = ciphered_vector[i]
        deciphered_item = (ciphered_item*multiplicative_inverse) % modulo
        deciphered_vector.append(deciphered_item)

    return deciphered_vector


def deciphered_items_to_bit_sequence(alg, private_key_vector, deciphered_item):
    return knapsack_solver.solve_knapsack(alg, private_key_vector, deciphered_item, "")
