from concurrent.futures import Future
import sys

import rclpy
from rclpy.node import Node
from tutorial_interfaces.srv import AddTwoInts

class MinimalClient(Node):
    def __init__(self):
        super().__init__('MinimalClient')
        self.request = AddTwoInts.Request()
        self.client = self.create_client(AddTwoInts,'add_two_ints')
        while not self.client.wait_for_service():
            self.get_logger().info('正在等待服务端...')
    def send_request(self, a:int, b:int):
        self.request.a = a
        self.request.b = b
        self.call_future:Future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self,self.call_future)
        return self.call_future.result()
def main():
    if len(sys.argv)< 3:
        print("用法: ros2 run py_service_pkg client X Y")
        return
    rclpy.init()
    client  =  MinimalClient()
    response:AddTwoInts.Response = client.send_request(int(sys.argv[1]),int(sys.argv[2]))
    client.get_logger().info('计算结果: %d' % response.sum)
    client.destroy_node()
    rclpy.shutdown()