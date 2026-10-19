import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

def quaternion_from_euler(roll, pitch, yaw):
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return [qx, qy, qz, qw]

class DynamicFrameBroadcaster(Node):
    def __init__(self):
        super().__init__("DynamicFrameBroadcaster")
        self.angle = 0
        self.brocadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1,self.timer_callback)
    def timer_callback(self):
        tfs = TransformStamped()
        tfs.header.stamp = self.get_clock().now().to_msg()
        tfs.header.frame_id = 'base_link'
        tfs.child_frame_id = 'radar_link'

        tfs.transform.translation.x = 1.0
        tfs.transform.translation.y = 1.0
        tfs.transform.translation.z = 0.5

        q = quaternion_from_euler(0,0,self.angle)
        tfs.transform.rotation.x = q[0]
        tfs.transform.rotation.y = q[1]
        tfs.transform.rotation.z = q[2]
        tfs.transform.rotation.w = q[3]

        self.brocadcaster.sendTransform(tfs)
        self.angle = self.angle + 0.05

def main():
    rclpy.init()
    dfb = DynamicFrameBroadcaster()
    rclpy.spin(dfb)
    dfb.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()