import logging
import inspect

from custom_components.test.fuzzing.fuzzer_utils.Runner import Runner


class ParamRunner(Runner):
    """Paramter runner class, inherits from the abstract runner class."""

    def __int__(self):
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

        logger = logging.getLogger(__name__)
        sig = inspect.signature(function)
        num_params = len(sig.parameters)
        logger.info("The given functions needs " + str(num_params) + " parameters")

        passed_tests = 0
        failed_tests = 0
        for param in param_set:
            try:
                function(*param)
                passed_tests += 1
                logger.debug(f"Test passed with parameters: {param}")
            except Exception as e:
                failed_tests += 1
                logger.error(f"Test failed with parameters: {param}. Exception: {e}")

        return [passed_tests, failed_tests]
