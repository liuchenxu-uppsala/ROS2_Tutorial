import rclpy
from rclpy.node import Node
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
import tf2_geometry_msgs 
from geometry_msgs.msg import PointStamped
from rclpy.time import Time
from tf2_ros import TransformException

class FrameListener(Node):
    def __init__(self):
        super().__init__('FrameListener')
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer,self)
        timer = self.create_timer(0.05,self.timer_callback)
    def timer_callback(self):
        point = PointStamped()
        point.header.frame_id = 'radar_link'
        point.header.stamp = Time().to_msg()
        point.point.x = 2.0
        point.point.y = 0.0
        point.point.z = 0.0
        try:
            base_point = self.buffer.transform(point,'base_link')
            self.get_logger().info(f'\n雷达看到点: ({point.point.x:.2f}, {point.point.y:.2f})'
                f'\n基座推算点: ({base_point.point.x:.2f}, {base_point.point.y:.2f})'
                f'\n-----------------------------------')
        except TransformException as ex:
            self.get_logger().info(f'无法获取坐标变换: {ex}')

def main():
    rclpy.init()
    listener = FrameListener()
    rclpy.spin(listener)
    listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
