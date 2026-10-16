import rclpy
from rclpy.node import Node
from std_msgs.msg import String
class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__("Subscriber")
        self.create_subscription(String,'publish_py',self.subsribe_callback,qos_profile = 10)
    def subsribe_callback(self,msg_received:String):
        self.get_logger().info('收到消息%s' % msg_received.data)

def main(args=None):
    rclpy.init(args=args)
    subscriber = MinimalSubscriber()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()