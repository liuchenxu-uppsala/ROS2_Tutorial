import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    srv_pkg_dir = get_package_share_directory('py_service_pkg')
    srv_launch = os.path.join(srv_pkg_dir, 'launch', 'add_two_ints.launch.py')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(srv_launch),
            launch_arguments={'a': '7', 'b': '8'}.items(),
        ),

        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim',
            parameters=[{'background_r': 255}],
        ),
    ])