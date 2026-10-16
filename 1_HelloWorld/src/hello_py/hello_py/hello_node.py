import rclpy
from rclpy.node import Node
def main(args=None):
    rclpy.init(args = args)
    node = Node("Hello_World_Node")
    node.get_logger().info("Hello World from Python!")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
