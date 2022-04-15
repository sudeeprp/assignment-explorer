from mergestatus import Interest
import unittest

class MergeStatusTest(unittest.TestCase):
    def test_username_by_removing_interest(self):
        self.assertEqual(Interest('a-batch', 'tdd-buckets', 'a-sheet')
            .reponame2user('tdd-buckets-AlbertoPenaMx'), "AlbertoPenaMx")

    def test_username_retains_hyphen(self):
        self.assertEqual(Interest('a-batch', 'tdd-buckets', 'a-sheet')
            .reponame2user('tdd-buckets-firstname-lastname'), "firstname-lastname")

    def test_removal_of_language_to_make_user(self):
        self.assertEqual(Interest('a-batch', 'well-named', 'a-sheet')
            .reponame2user('well-named-in-py-AlbertoPenaMx'), "AlbertoPenaMx")
       
unittest.main()
