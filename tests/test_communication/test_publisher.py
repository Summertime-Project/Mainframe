import unittest
import gc
from weakref import WeakMethod

from communication.message import VelocityMessage, AngularVelocityMessage
from communication.publisher import Publisher


class Foo:
    def __init__(self):
        self.vx = 0

    def receiveMessage(self, message: VelocityMessage) -> None:
        self.vx = message.x


class PublisherTest(unittest.TestCase):
    def test_add_callbacks(self):
        publisher = Publisher()
        foo = Foo()

        publisher.add_callback(VelocityMessage, foo.receiveMessage)

        m1 = VelocityMessage(10, 11, 12)
        m2 = AngularVelocityMessage(-1, -2, -3)

        publisher.update_callback(m1)
        self.assertEqual(m1.x, foo.vx)

        publisher.update_callback(m2)
        self.assertNotEqual(m2.x, foo.vx)

    def test_remove_callback(self):
        publisher = Publisher()
        foo = Foo()

        publisher.add_callback(VelocityMessage, foo.receiveMessage)
        m1 = VelocityMessage(10, 11, 12)

        publisher.remove_callback(VelocityMessage, foo.receiveMessage)

        publisher.update_callback(m1)

        self.assertNotEqual(m1.x, foo.vx)

    def test_no_accessing_deleted_object(self):
        publisher = Publisher()
        foo = Foo()

        # ONLY FOR THIS TEST - normaly use .add_callback
        publisher.callbacks[VelocityMessage] = [WeakMethod(foo.receiveMessage)]

        m1 = VelocityMessage(10, 11, 12)

        foo = None
        gc.collect()

        self.assertIsNone(publisher.callbacks[VelocityMessage][0](), "The object is not dead after deleting")


if __name__ == '__main__':
    unittest.main()
