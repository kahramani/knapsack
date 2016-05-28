from random import randint
from random import choice
import string
import re
import math
import configparser
import constants
import logger


logger = logger.build_logger("utility")


def read_property_key(key, structure_type, section, file_name):
    """
    :param key:
    :param structure_type:
    :param section:
    :param file_name:
    :return: read key with desired type of structure from property file
    """
    try:
        config = configparser.RawConfigParser()
        config.optionxform = str
        config.read(file_name)
        if structure_type == constants.structure_type_int:
            return config.getint(section, key)
        elif structure_type == constants.structure_type_float:
            return config.getfloat(section, key)
        elif structure_type == constants.structure_type_boolean:
            return config.getboolean(section, key)
        else:
            return config.get(section, key)
    except configparser.Error:
        raise Exception("Failed to read key from file. File: \'" + file_name + "\', Section: \'" + section + "\', " +
                        "Key: \'" + key + "\', Type: \'" + structure_type + "\'")

    return key

# initialize first parameters - start
comma_delimiter = ","
hyphen_delimiter = "-"
log_enabled = read_property_key("log_enabled", constants.structure_type_boolean, constants.section_parameters,
                                constants.property_file)
random_text_test = read_property_key("random_text_test", constants.structure_type_boolean, constants.section_parameters,
                                constants.property_file)
length_of_random_text = 0
if random_text_test:
    length_of_random_text = read_property_key("length_of_random_text", constants.structure_type_int,
                                              constants.section_parameters, constants.property_file)
length_of_key_vector = read_property_key("length_of_key_vector", constants.structure_type_int,
                                         constants.section_vector, constants.property_file)
random_key_vector_addition_range = read_property_key("random_key_vector_addition_range", constants.structure_type_int,
                                                     constants.section_vector, constants.property_file)
private_key_vector_initial_range = read_property_key("private_key_vector_initial_range", constants.structure_type_string
                                                     , constants.section_vector, constants.property_file)
private_key_vector_start_value = int(private_key_vector_initial_range.split(hyphen_delimiter)[0])
private_key_vector_stop_value = int(private_key_vector_initial_range.split(hyphen_delimiter)[1])
# initialize first parameters - end


def validate_initial_parameters():
    """
    :return: validate initial parameters before run
    """
    validation_message = ""
    log_enable_regex_check = check_regex_match(str(log_enabled), constants.regex_pattern_boolean)
    initial_range_regex_check = check_regex_match(str(private_key_vector_initial_range), constants.regex_pattern_range)
    random_key_addition_regex_check = check_regex_match(str(random_key_vector_addition_range), constants.regex_pattern_digit)
    if not log_enable_regex_check:
        validation_message = "Log enabled parameter can set only true or false. " + \
                             "Rearrange it from " + str(constants.property_file)
    elif not initial_range_regex_check:
        validation_message = "Private key initial range format is wrong. " + \
                             "Rearrange it from " + str(constants.property_file)
    elif not random_key_addition_regex_check:
        validation_message = "Random key addition range format is wrong. " + \
                             "Rearrange it from " + str(constants.property_file)
    elif length_of_key_vector < 8:
        validation_message = "Length of key vector must be at least 8. " + \
                             "Rearrange it from " + str(constants.property_file)
    return validation_message


def user_input(m, r):
    """
    :param m: direction message
    :param r: regex pattern to validate
    :return: user input text
    """
    text_input = input(m + " > ")
    while not check_regex_match(text_input, r):
        wrong_input = "\n" + constants.background_colorant_red + "You entered a wrong input." + \
                      constants.attribute_default + "\n" + m
        text_input = input(wrong_input + " > ")

    return text_input


def press_enter_to_continue():
    """
    :return:
    """
    input("Press Enter to continue...\n")


def convert_text_to_bit(text, bit_length, encoding='utf-8', errors='surrogatepass'):
    """
    :param text:
    :param bit_length:
    :param encoding:
    :param errors:
    :return: ASCII response of a char
    """
    bit_sequence = ""
    for i in range(0, len(text)):
        char = text[i]
        bits = bin(int.from_bytes(char.encode(encoding, errors), 'big'))[2:]
        bit_sequence += bits.zfill(bit_length * ((len(bits) + bit_length-1) // bit_length))

    return bit_sequence


def convert_bit_to_text(bits, bit_length, encoding='utf-8', errors='surrogatepass'):
    """

    :param bits:
    :param bit_length:
    :param encoding:
    :param errors:
    :return: Char response of ASCII binary value
    """
    try:
        n = int(bits, 2)
        return n.to_bytes((n.bit_length() + bit_length-1) // bit_length, 'big').decode(encoding, errors) or '\0'
    except:
        return '?'


def group_on_sequence(seq, n):
    """
    :param seq:
    :param n:
    :return: list of bit sequence which is split and grouped by n
    """
    grouped_list = list()
    seq_len = int(len(seq))
    rest_count = int(seq_len/n)
    while seq:
        grouped_list.append(seq[:n])
        if len(seq) == n:
            break
        rest_count -= 1
        reverse_cursor = n*rest_count
        seq = seq[-reverse_cursor:]

    return grouped_list


def calculate_greatest_common_divisor(n, m):
    """
    :param n:
    :param m:
    :return: greatest common divisor of n and m
    """
    return math.gcd(n, m)


def convert_raw_matrix_to_list(raw_matrix, delimiter):
    """
    :param raw_matrix:
    :param delimiter:
    :return: list of int matrix values which are originally string
    """
    matrix = list()
    items = raw_matrix.split(delimiter)
    for i in range(0, len(items)):
        matrix.append(int(items[i]))

    return matrix


def check_regex_match(text, regex_pattern):
    """
    :param text: text to check does pattern match
    :param regex_pattern: pattern to look up
    :return: does regex_pattern match on text or not
    """
    if regex_pattern == "":
        return True
    compiled_regex = re.compile(regex_pattern)
    match = compiled_regex.search(text)
    if match:
        return True
    else:
        return False


def is_prime(n):
    """
    :param n: a number to check is it prime
    :return: is n a prime number or not
    """
    if n < 0:
        return False
    else:
        return all(n % i for i in range(2, n))


def is_co_prime(m, n):
    """
    :param m: a number to check
    :param n: a number to check
    :return: are m and n coprimes or not
    """
    if calculate_greatest_common_divisor(m, n) == 1:
        return True
    else:
        return False


def generate_super_increasing_vector(l=length_of_key_vector):
    """
    :param l: length of vector #default value retrieves from property file
    :return: an int list containing vector items
    """
    vector = list()
    vector_item_pre_sum = 0
    for i in range(0, l):
        random_int = generate_random_int(vector_item_pre_sum, vector_item_pre_sum+random_key_vector_addition_range)
        vector_item_pre_sum += random_int + 1
        vector.append(random_int)
    return vector


def determine_modulo_acc_to_random_key_vector(random_key_vector):
    sum_of_list = sum(random_key_vector)
    return randint(sum_of_list + 1, sum_of_list + random_key_vector_addition_range)


def determine_element_to_mask(modulo):
    element_found = False
    element = 0
    while not element_found:
        element = generate_random_int(1, modulo-1)
        if is_co_prime(modulo, element):
            element_found = True

    return element


def generate_random_int(start, stop):
    """
    :param start: reference to start
    :param stop: reference to stop
    :return: a random int generated between start and stop references
    """
    if start == 0:
        return randint(private_key_vector_start_value, private_key_vector_stop_value)
    else:
        return randint(start, stop)


def find_prime_numbers_in_range(start, stop):
    """
    :param start: reference to start
    :param stop: reference to start
    :return: a int list including prime numbers between start and stop references
    """
    result = []
    while start <= stop:
        if is_prime(start):
            result.append(start)
        start += 1
    return result


def generate_random_text(l):
    """
    :param l: length of text
    :return: a random text which contains letters, digits and punctuations
    """
    random_text = ""
    chars = string.ascii_letters + string.digits + string.punctuation
    for n in range(l):
        random_text += choice(chars)
    return random_text
