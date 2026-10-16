import rclpy
from rclpy.node import Node
from tutorial_interfaces.srv import AddTwoInts

class MinimalService(Node):
    def __init__(self):
        super().__init__("MinimalService")
        self.create_service(AddTwoInts,'add_two_ints',self.service_callback)
        self.get_logger().info("服务端已启动")
    def service_callback(self,request:AddTwoInts.Request,response:AddTwoInts.Response):
        response.sum = request.a + request.b
        self.get_logger().info(f'收到来自请求{request.a} + {request.b}')
        return response

def main(args = None):
    rclpy.init(args=args)
    service  =  MinimalService()
    rclpy.spin(service)
    service.destroy_node()
    rclpy.shutdown()