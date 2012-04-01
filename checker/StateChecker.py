""" This module defines classes to check the states for some objects,
e.g. Buildbot.
"""

import urllib
import re


class StateChecker(object):
    """ Check state of certain object and return whether it's okay to be used.
    """

    def is_ok(self):
        pass


class BuildbotStateChecker(StateChecker):
    """ State checker used to check whether state of buildbot is ok
    to be used.
    Define several methods making querying buildbot states easy.
    Subclasses must implement the is_ok() method.
    """

    def __init__(self, url, open_url_func = urllib.urlopen):
        StateChecker.__init__(self)
        self.__buildbot_url = url
        self.__buildbot_url_handle = open_url_func(url)

    def get_builder_states(self):
        content = self.__buildbot_url_handle.read()
        lines = content.splitlines()
        
        # uses the regex to match the states.
        # Because using DOM method to parse the page is not so reliable.
        state_pattern = re.compile(r'class="Activity (?P<state>\w+)"')
        states = []
        for line in lines:
            match_result = state_pattern.search(line)
            if match_result != None:
                states.append(match_result.group('state'))
                
        return states

    def is_ok(self):
        pass


class BuildbotIdleStateChecker(BuildbotStateChecker):


    def __init__(self, *args):
        BuildbotStateChecker.__init__(self, *args)

    def is_buildbot_idle(self, states):
        """ determine whether buildbot is idle from the given states.
        So far, idle means all builders are idle
        """
        
        for state in states:
            if state != 'idle':
                return False
        
        return True
    
    def is_ok(self):
        states = self.get_builder_states()
        return self.is_buildbot_idle(states)


import unittest

class _StateCheckerTest(unittest.TestCase):


    def setUp(self):
        self.__test_data_path = './data/bbotmon'
        
        test_file = self.__test_data_path + '/index.htm'
        self.__state_checker = BuildbotIdleStateChecker(test_file, open)

    def test_get_builder_states(self):
        states = self.__state_checker.get_builder_states()

        self.assertTrue(8, len(states))

    def test_is_buildbot_idle(self):
        states = ['idle', 'building', 'idle']
        self.assertFalse(self.__state_checker.is_buildbot_idle(states))
        
        states = ['idle', 'idle', 'idle']
        self.assertTrue(self.__state_checker.is_buildbot_idle(states))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(
        _StateCheckerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


