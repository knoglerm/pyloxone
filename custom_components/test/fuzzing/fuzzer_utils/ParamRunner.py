import logging
import inspect
import random

from custom_components.test.fuzzing.fuzzer_utils.Runner import Runner


class ParamRunner(Runner):
    """Paramter runner class, inherits from the abstract runner class."""

    logger = logging.getLogger(__name__)

    def __init__(self):
        """constructor"""
        pass

    def run(self, function, param_set: list) -> list:
        """Executes all transferred parameter sets for the transferred function.

        :param function: The passed function which is to be fuzzed.
        :type function: function
        :param param_set: The parameter set transferred from the fuzzer.
        :type param_set: list

        :return: Returns a list with two integers, the first number retruns the number of passed tests and the second of failed
        :rtype: list
        """

        sig = inspect.signature(function)
        num_params = len(sig.parameters)
        self.logger.info("The given functions needs " + str(num_params) + " parameters")

        passed_tests = 0
        failed_tests = 0
        for param in param_set:
            try:
                function(*param)
                passed_tests += 1
                self.logger.debug(f"Test passed with parameters: {param}")
            except Exception as e:
                failed_tests += 1
                self.logger.error(f"Test failed with parameters: {param}. Exception: {e}")

        return [passed_tests, failed_tests]
    
    def limit_param_set(self, param_set: list, runs: int) -> list:
        """Generates a specific selection of an individual value pool. A list of lists is returned with a specified number of elements.

        :param param_set: The value pool as list of lists.
        :type param_nr: list
        :param runs: Number of elements selected from the value pool.
        :type types: int

        :return: A random selection of certain elements from the parameter set.
        :rtype: list
        """

        # Validate input parameters
        if not isinstance(param_set, list):
            self.logger.error("Param_set must be of type list.")
            raise TypeError("Param_set must be of type list.")
        if len(param_set) == 0:
            self.logger.error("Length of param_set must be greater then 0.")
            raise ValueError("Length of param_set must be greater then 0.")
        if not isinstance(runs, int) or runs <= 0:
            self.logger.error("Runs must be of type int and greater than 0. Parameter set is returned unchanged.")
            return param_set
        
        # Selection of random elements from param_set if the number of runs is smaller than the number of elements in param_set
        if runs > len(param_set):
            self.logger.info("Length of param_set is smaller than the value of runs. Returned param_set unchanged.")
            return param_set
        else:
            self.logger.info(f"Decresed elements in param_set from {len(param_set)} to {runs}")
            return random.sample(param_set, runs)
