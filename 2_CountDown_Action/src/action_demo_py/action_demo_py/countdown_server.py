import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from my_interface.action import CountDown

class CountDownServer(Node):
    def __init__(self):
        super().__init__('countdown_server')
        self._server = ActionServer(self,CountDown,"countdown",self.execute_callback)
        self.get_logger().info("CountDownServer Start!")

    def execute_callback(self,goal_handle:ServerGoalHandle):
        goal: CountDown.Goal  = goal_handle.request
        start = goal.start
        self.get_logger().info(f'开始从{start}倒计时')
        feedback = CountDown.Feedback()
        for remaining in range(start,0,-1):
            feedback.remaining = remaining
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'反馈: 还剩 {remaining}')
            time.sleep(1)
        goal_handle.succeed()
        result = CountDown.Result()
        result.success = True
        result.message = f'从{start}倒数完成'
        return result
def main(args=None):
    rclpy.init(args=args)
    node = CountDownServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
           rclpy.shutdown()