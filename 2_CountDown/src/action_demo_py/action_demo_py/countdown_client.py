from concurrent.futures import Future

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from my_interface.action import CountDown

class CountDownClient(Node):
    def __init__(self):
        super().__init__("countdown_client")
        self._client = ActionClient(self,CountDown,"countdown")

    def send_goal(self,start):
        goal = CountDown.Goal()
        goal.start = start
        self.get_logger().info(f'倒计时从{start}开始')
        self._client.wait_for_server()
        goal_result:Future = self._client.send_goal_async(goal=goal,feedback_callback=self.feedback_callback)
        rclpy.spin_until_future_complete(self,goal_result)
        goal_handle:ClientGoalHandle = goal_result.result()
        if goal_handle.accepted:
            self.get_logger().info(f'任务被接受了')
        else:
            self.get_logger().info(f'任务被拒绝了')
        result_future:Future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self,result_future)
        response  = result_future.result()
        result:CountDown.Result = response.result
        self.get_logger().info(
            f'结果: success={result.success}, message={result.message}, status={response.status}')

    def feedback_callback(self,feedback_msg:CountDown.Impl.FeedbackMessage):
        self.get_logger().info(f'收到反馈: 还剩 {feedback_msg.feedback.remaining}')
        pass

def main(args=None):
    rclpy.init(args=args)
    client = CountDownClient()
    try:
        client.send_goal(5)
    except KeyboardInterrupt:
        pass
    finally:
        client.destroy_node()
        rclpy.shutdown()

