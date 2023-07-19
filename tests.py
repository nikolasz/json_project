import unittest
from main import Message, Conversation, dfs, get_conversation_text, write_conversation_to_file

class TestMain(unittest.TestCase):
    def test_message_creation(self):
        # Test the Message constructor
        message = Message('1', 'Hello, world!', None, [])
        self.assertEqual(message.id_, '1')
        self.assertEqual(message.message, 'Hello, world!')
        self.assertIsNone(message.parent_message_id)
        self.assertEqual(message.children_ids, [])
        self.assertEqual(message.children, [])

    def test_conversation_creation(self):
        # Test the Conversation constructor
        messages = {'1': Message('1', 'Hello, world!', None, [])}
        conversation = Conversation('1', 'Test Conversation', 123456, messages)
        self.assertEqual(conversation.id_, '1')
        self.assertEqual(conversation.title, 'Test Conversation')
        self.assertEqual(conversation.create_time, 123456)
        self.assertEqual(conversation.messages, messages)

    def test_dfs(self):
        # Test the dfs function
        messages = {'1': Message('1', 'Hello', None, ['2']), '2': Message('2', 'Hi', '1', [])}
        visited = set()
        message_text = dfs('1', messages, visited)
        self.assertEqual(message_text, 'Hello\nHi\n')

# Manually create a test suite and add the test cases to it
suite = unittest.TestSuite()
suite.addTest(TestMain('test_message_creation'))
suite.addTest(TestMain('test_conversation_creation'))
suite.addTest(TestMain('test_dfs'))

# Run the test suite
runner = unittest.TextTestRunner()
runner.run(suite)
