import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro

def generate_launch_description():
    pkg_share = FindPackageShare(package='my_robot_description').find('my_robot_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)

    params = {'robot_description': robot_description_config.toxml()}

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[params]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        )
    ])
