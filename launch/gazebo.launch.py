import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro

def generate_launch_description():
    pkg_share = FindPackageShare(package='my_robot_description').find('my_robot_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)

    params = {'robot_description': robot_description_config.toxml()}

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(FindPackageShare('ros_gz_sim').find('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'my_robot'],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        spawn_entity
    ])
