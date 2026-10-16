import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('py_publisher')
        time_period = 0.5
        self.publisher = self.create_publisher(String,'publish_py',10)
        self.create_timer(time_period,self.timer_callback)
        self.i = 0
    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World %d' % self.i
        self.publisher.publish(msg)
        self.get_logger().info('publishing data:%s' % msg.data)
        self.i = self.i + 1
def main(args=None):
    rclpy.init(args=args)
    publisher = MinimalPublisher()
    rclpy.spin(publisher)
    publisher.destroy_node()
    rclpy.shutdown()
