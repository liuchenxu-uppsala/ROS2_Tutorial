# ROS2_Tutorial

![ROS 2](https://img.shields.io/badge/ROS%202-Humble-22314E?logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu&logoColor=white)

My ROS 2 learning notes and practice code, following Seeed Studio's ROS 2 beginner series
([AI_Robotics_Academy](https://github.com/Seeed-Projects/AI_Robotics_Academy)).

| 课 | 文件夹 | 内容 |
|---|---|---|
| 1 | [`HelloWorld`](HelloWorld) | 第一个 Python 节点 |
| 2 | [`2_CountDown`](2_CountDown) | 自定义 Action：倒计时 |
| 3 | [`3_Communication_Srv`](3_Communication_Srv) | 话题、自定义服务 AddTwoInts |

---

## 环境与流程

Docker 容器（Ubuntu 22.04 + ROS 2 Humble）里编译运行，宿主机上 git。每一课是一个独立工作空间。

```bash
cd <课名>/src && ros2 pkg create <包名> --build-type ament_python --dependencies rclpy
cd .. && colcon build --symlink-install     # 在工作空间根目录编译，不要在 src 里
source install/setup.bash                   # 每个新终端都要 source
ros2 run <包名> <程序名>
```

- 只改了已有 `.py`：重启程序即可；改了 `setup.py` 或接口文件：重新编译 + source
- 自定义接口（`.msg` / `.srv` / `.action`）必须放在 `ament_cmake` 包里

## 三种通信方式

| | 话题 | 服务 | Action |
|---|---|---|---|
| 方式 | 单向、持续 | 一问一答 | 交任务 → 报进度 → 拿结果 |
| 接口文件 | `.msg`（1 段） | `.srv`（请求 `---` 响应） | `.action`（任务 `---` 结果 `---` 进度） |
| 例子 | `/joint_states` | `/compute_fk` | `FollowJointTrajectory` |

---

## 1 · HelloWorld

```python
rclpy.init()               # 初始化通信环境
node = Node('Hello_World_Node')
node.get_logger().info('...')
rclpy.spin(node)           # 一直运行，靠回调干活
rclpy.shutdown()
```

- `setup.py` 里登记程序：`'程序名 = Python包.文件名:main'`，`ros2 run` 用的是程序名
- 程序名、文件名、节点名是三回事

## 2 · CountDown（Action）

![Action](2_action_client_server.png)

- 两个包：`my_interface`（`action/CountDown.action`）+ `action_demo_py`（服务端、客户端）
- 一个 Action = 3 个服务（send_goal / get_result / cancel_goal）+ 2 个话题（feedback / status），库自动创建
- 服务端：`publish_feedback()` 报进度，`succeed()` 设结局，`return result` 给结果
- 客户端：`send_goal_async()` → `get_result_async()`，进度在 `feedback_callback` 里收

```bash
ros2 run action_demo_py countdown_server
ros2 run action_demo_py countdown_client
```

## 3 · 话题与服务

![Service](3_Communication_Srv/3_service_client_server.png)

**话题**

- `create_publisher(String, 'topic', 10)`：10 是队列长度；`publish()` 发完就返回，不等订阅者
- 每个订阅者有自己的队列，处理不过来就丢最旧的
- `create_timer(0.5, cb)`：每 0.5 秒调用一次，但只有在 spin 时才会调用

**服务**：`tutorial_interfaces/srv/AddTwoInts`（`int64 a, b --- int64 sum`）+ `py_service_pkg`

```python
# 服务端
self.create_service(AddTwoInts, 'add_two_ints', self.callback)
def callback(self, request, response):
    response.sum = request.a + request.b
    return response

# 客户端
self.cli = self.create_client(AddTwoInts, 'add_two_ints')
while not self.cli.wait_for_service(timeout_sec=1.0): ...   # 每次最多等 1 秒
future = self.cli.call_async(req)
rclpy.spin_until_future_complete(self, future)
```

```bash
ros2 run py_service_pkg server
ros2 run py_service_pkg client 2 3      # 计算结果: 5
```

---

## 要点速记

- `rclpy.spin(node)` 会停在那一行；所有回调都靠 spin 家族来调用
- 回调作为参数时只写函数名，不加括号：`callback=self.cb`
- `self.a.f(x)`：点号前的对象自动传入；`rclpy.xxx(node, ...)` 这种模块函数要显式传节点
- 检查接口：`ros2 interface show 包名/srv/类型名`；"找不到类型"通常是终端没 source
- VS Code 找不到自定义接口：`settings.json` 的 `python.analysis.extraPaths` 里加 `<课名>/install/<接口包>/local/lib/python3.10/dist-packages`

| 回调 | 收到 | 返回 |
|---|---|---|
| 定时器 | 无 | 无 |
| 话题订阅 | `msg` | 无 |
| 服务端 | `request, response` | `response` |
| Action `execute_callback` | `ServerGoalHandle` | `Result` |
| Action `feedback_callback` | `feedback_msg`（`.feedback`） | 无 |

---

## License

[GPL-3.0](LICENSE)
