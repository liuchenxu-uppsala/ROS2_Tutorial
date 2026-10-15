# ROS2_Tutorial

![ROS 2](https://img.shields.io/badge/ROS%202-Humble-22314E?logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu&logoColor=white)

My ROS 2 learning notes and practice code, following Seeed Studio's ROS 2 beginner series
([AI_Robotics_Academy](https://github.com/Seeed-Projects/AI_Robotics_Academy)).

每一课是一个独立的工作空间（`<课名>/src/...`），笔记统一记在本文件里。

| 课 | 文件夹 | 内容 |
|---|---|---|
| 1 | [`HelloWorld`](HelloWorld) | 第一个 Python 节点 |
| 2 | [`2_CountDown`](2_CountDown) | 自定义 Action：倒计时服务端 + 客户端 |

---

## 环境

- 在 Docker 容器里开发（Ubuntu 22.04 + ROS 2 Humble），宿主机 `~/dobot_shared` = 容器 `/dobot_ws/shared`
- VS Code 通过 Dev Containers 的 *Attach to Running Container* 连进容器
- **编译、运行都在容器里；git 在宿主机上**

## 通用流程

```bash
cd <课名>/src
ros2 pkg create <包名> --build-type ament_python --dependencies rclpy   # 包名放最前面

cd ..                                   # 回到工作空间根目录（不要在 src 里编译）
colcon build --symlink-install
source install/setup.bash               # 每个新终端都要 source 一次
ros2 run <包名> <程序名>
```

| 改了什么 | 重新编译 | 重新 source | 重启程序 |
|---|:-:|:-:|:-:|
| 已有 `.py` 的内容 | | | ✅ |
| `setup.py`（新增程序） | ✅ | ✅ | ✅ |
| `.msg` / `.srv` / `.action` | ✅ | ✅ | ✅ |
| 新开终端 | | ✅ | |

---

## 1 · HelloWorld

最小的 Python 节点：创建节点，打印一条日志。

```python
rclpy.init(args=args)              # 初始化 ROS 2 通信环境
node = Node('Hello_World_Node')    # 创建节点，此时 ros2 node list 才能看到它
node.get_logger().info('...')      # 注意 get_logger() 要带括号
rclpy.spin(node)                   # 一直运行，等待并处理事件
rclpy.shutdown()
```

**要点**

- 工作空间 = 一个带 `src/` 的文件夹；`colcon build` 生成 `build/ install/ log/`
- `ament_python` 包的两层同名文件夹：外层是 ROS 包（放 `package.xml`、`setup.py`），里层是 Python 代码
- `setup.py` 里登记程序：`'程序名 = Python包.文件名:main'`，`ros2 run` 用的是**程序名**
- 包名要在 4 处保持一致：`package.xml` 的 `<name>`、`setup.py` 的 `package_name`、`resource/` 里的空文件名、`setup.cfg`
- 程序名 ≠ 文件名 ≠ 节点名，三者各管各的

---

## 2 · CountDown（Action）

![Action 客户端与服务端](2_action_client_server.png)

客户端交任务"从 N 开始倒数" → 服务端每秒报告"还剩几" → 数完返回结果。

### 话题 · 服务 · Action

| | 话题 | 服务 | Action |
|---|---|---|---|
| 方式 | 单向、持续 | 一问一答 | 交任务 → 报进度 → 拿结果，可取消 |
| 类型文件 | `.msg` | `.srv` | `.action`（任务 `---` 结果 `---` 进度） |

**一个 Action = 3 个服务 + 2 个话题**，创建 `ActionServer` / `ActionClient` 时自动生成：

| 通道 `/countdown/_action/...` | 种类 | 作用 | 对应代码 |
|---|---|---|---|
| `send_goal` | 服务 | 交任务 | 客户端 `send_goal_async()` |
| `get_result` | 服务 | 要结果 | 服务端 `return result` / 客户端 `get_result_async()` |
| `cancel_goal` | 服务 | 取消 | 客户端 `cancel_goal_async()` |
| `feedback` | 话题 | 进度 | 服务端 `publish_feedback()` / 客户端 `feedback_callback` |
| `status` | 话题 | 结局 | 服务端 `succeed()` / `abort()` / `canceled()` |

### 两个包

```
2_CountDown/src/
├── my_interface/       # ament_cmake：只放类型 action/CountDown.action
└── action_demo_py/     # ament_python：countdown_server.py + countdown_client.py
```

- `.action` 必须靠 rosidl 生成代码，只能用 `ament_cmake`，所以类型单独成包
- 类型全名 `my_interface/action/CountDown` = 包名 / 种类 / 类型名
- Python 里：`CountDown.Goal`、`CountDown.Result`、`CountDown.Feedback` 分别对应三段

### 运行

```bash
# 终端 1
ros2 run action_demo_py countdown_server
# 终端 2（二选一）
ros2 run action_demo_py countdown_client
ros2 action send_goal /countdown my_interface/action/CountDown "{start: 5}" --feedback
```

### 关键 API

| 服务端 | 说明 |
|---|---|
| `ActionServer(self, CountDown, 'countdown', self.execute_callback)` | 节点、类型、名字、干活的函数 |
| `goal_handle.request.start` | 读任务内容 |
| `goal_handle.publish_feedback(fb)` | 报进度 |
| `goal_handle.succeed()` + `return result` | 前者是 ROS 官方结局，后者是自定义结果数据，两个都要 |

| 客户端 | 说明 |
|---|---|
| `send_goal_async(goal, feedback_callback=self.cb)` | 返回 Future；回调只写函数名，不加括号 |
| `rclpy.spin_until_future_complete(self, future)` | 边处理消息边等，直到 Future 有结果 |
| `send_future.result()` | `ClientGoalHandle`：`.accepted`、`.get_result_async()` |
| `result_future.result()` | `.status`（4 成功 / 5 取消 / 6 失败）+ `.result` |
| `feedback_callback(self, feedback_msg)` | 进度在 `feedback_msg.feedback` 里 |

### 观察命令

```bash
ros2 action list -t
ros2 action info /countdown
ros2 interface show my_interface/action/CountDown
```

---

## 常见问题

| 现象 | 原因 → 解决 |
|---|---|
| `The passed action type is invalid` | 终端没 source 本工作空间 |
| `src/` 里出现 `build/ install/ log/` | 在 `src` 里编译了 → 删掉，回根目录重编 |
| `AssertionError: ... must be a sub message of type ..._Result` | `execute_callback` 没 `return result` |
| `sequence size exceeds remaining buffer` | 两边类型版本不一致 → 全部关闭、`ros2 daemon stop`、重新 source 再启动 |
| VS Code 不能跳转 / 没有提示 | `.vscode/settings.json` 里加 `python.analysis.extraPaths`（`/opt/ros/humble/...` 和本工作空间 `install/.../dist-packages`） |

## rclpy 回调速查（Humble 没有类型标注）

| 回调 | 收到 | 返回 |
|---|---|---|
| 定时器 | 无 | 无 |
| 话题订阅 | `msg` | 无 |
| 服务端 | `request, response` | `response` |
| Action `goal_callback` | `Goal` | `GoalResponse.ACCEPT / REJECT` |
| Action `execute_callback` | `ServerGoalHandle` | `Result` |
| Action `cancel_callback` | `ServerGoalHandle` | `CancelResponse.ACCEPT / REJECT` |
| Action `feedback_callback` | `feedback_msg`（`.goal_id`、`.feedback`） | 无 |

不确定参数是什么时：`def cb(self, *args): print(args)`，或者在回调里加 `breakpoint()`。

---

## License

[GPL-3.0](LICENSE)
