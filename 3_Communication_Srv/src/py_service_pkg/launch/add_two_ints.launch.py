from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument('a',default_value = '2'),
            DeclareLaunchArgument('b',default_value = '3'),
            Node(
                package='py_service_pkg',
                executable='server',
                output='screen',
            ),
            Node(
                package = 'py_service_pkg',
                executable = 'client',
                arguments =  [LaunchConfiguration('a'),LaunchConfiguration('b')],
                output='screen',           
            )
        ]
    )