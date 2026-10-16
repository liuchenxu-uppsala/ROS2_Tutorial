import rclpy
from rclpy.node import Node
class ParamNode(Node):
    def __init__(self):
        super().__init__('param_node')
        self.declare_parameter('my_str','hello_world')
        self.declare_parameter('my_int',10)
        self.create_timer(1,self.timer_callback)
    def timer_callback(self):
        my_str = self.get_parameter('my_str').get_parameter_value().string_value
        self.get_logger().info('my_str 的值是:%s' % my_str)
def main():
    rclpy.init()
    param_node = ParamNode()
    rclpy.spin(param_node)
    param_node.destroy_node()
    rclpy.shutdown()