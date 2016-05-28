import constants
import logger


logger = logger.build_logger('knapsack_solver')


def solve_knapsack(alg, private_key_vector, deciphered_item, best_response):
    """
    :param alg:
    :param private_key_vector:
    :param deciphered_item:
    :param best_response:
    :return: knapsack solution by algorithm
    """
    if alg == constants.algorithm_back_tracking:
        return back_tracking_solution(private_key_vector, deciphered_item, best_response)
    else:
        return ""


def back_tracking_solution(private_key_vector, deciphered_item, best_response):
    """
    :param private_key_vector:
    :param deciphered_item:
    :param best_response:
    :return: knapsack solution by recursive algorithm
    """
    reference_index = 0
    editable_deciphered_item = deciphered_item
    if editable_deciphered_item == 0:
        return ""
    else:
        for i in reversed(private_key_vector):
            item = i
            if editable_deciphered_item >= item:
                if reference_index == 0:
                    reference_index = private_key_vector.index(item)
                editable_deciphered_item -= item
                best_response = "1" + best_response
            else:
                best_response = "0" + best_response
        if editable_deciphered_item != 0:
            best_response = ""
            if reference_index != 0:
                for k in range(0, len(private_key_vector) - reference_index):
                    best_response = '0' + best_response

                best_response = back_tracking_solution(private_key_vector[:reference_index], deciphered_item, best_response)
            else:
                return ""

    return best_response

