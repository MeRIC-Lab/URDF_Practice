import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():

    pkgPath = launch_ros.substitutions.FindPackageShare(package='manipulator').find('manipulator')
    default_urdfModelPath = os.path.join(pkgPath, 'urdf/testbot.urdf')
    rvizConfigPath = os.path.join(pkgPath, 'config/config.rviz')
    
    #Print URDF path (for Debugging)
    print(default_urdfModelPath)
    
    #To set the urdf path using launch parameter
    urdfModelPath = LaunchConfiguration('urdf_model')
    
    #Set the parameter of robot     
    robot_description_param = {'robot_description': Command(['xacro ', urdfModelPath])}
    #with open(urdfModelPath, 'r') as infp:
    #    robot_desc = infp.read()
        
    #robot_description_param = {'robot_description': robot_desc}
    
    robot_state_publisher_node = launch_ros.actions.Node(
        package = 'robot_state_publisher', 
        executable = 'robot_state_publisher', 
        name = 'robot_sate_publisher',
        output='screen', 
        parameters = [robot_description_param]
    )
        
    joint_state_publisher_node = launch_ros.actions.Node(
        package = 'joint_state_publisher', 
        executable = 'joint_state_publisher', 
        name = 'joint_sate_publisher',
        output='screen'
    )   
    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package = 'joint_state_publisher_gui', 
        executable = 'joint_state_publisher_gui', 
        name = 'joint_sate_publisher_gui',        
        condition = launch.conditions.IfCondition(LaunchConfiguration('gui'))
    )  
    rviz_node = launch_ros.actions.Node(
        package = 'rviz2', 
        executable = 'rviz2', 
        name = 'rviz2',
        output='screen', 
        arguments = ['-d', rvizConfigPath]
    )
    
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='urdf_model', default_value=default_urdfModelPath,
                                            description='Absolute path to robot urdf file'), 
        launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
                                            description='This is a flag to enable joint_state_publisher_gui'), 
        robot_state_publisher_node, 
        joint_state_publisher_node, 
        joint_state_publisher_gui_node,
        rviz_node
    ])
