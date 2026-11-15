# SUMSA-NASA-ROVER-SOFTWARE
# NASA JPL Rover — ROS 2 Simulation

This guide explains how to launch and control the NASA JPL Open Source Rover in **Gazebo Harmonic** and **RViz2**.


## 1. Source the ROS 2 Workspace

Run the following commands in **every new terminal**:

```bash
source /opt/ros/jazzy/setup.bash
source ~/sumsa_rover_ws/install/setup.bash
```

## 2. Launch Gazebo

Choose one of the available simulation environments.

**Maze environment:**

```bash
ros2 launch osr_gazebo maze_world.launch.py
```

**Mars environment:**

```bash
ros2 launch osr_gazebo mars_world.launch.py
```

**Default LiDAR test environment:**

```bash
ros2 launch osr_gazebo empty_world.launch.py
```

Keep the Gazebo terminal running.

## 3. Activate the Joint State Broadcaster (THis has to be when gazebo launches, but idk y its not activating. Loki tried evveryhitng ;-;)

Open a **second terminal** and source the workspace.

Check the controllers:

```bash
ros2 control list_controllers
```

If `joint_state_broadcaster` is inactive, activate it:

```bash
ros2 control switch_controllers --activate joint_state_broadcaster
```

Verify:

```bash
ros2 control list_controllers
```

The following controllers should be active:

```text
joint_state_broadcaster   active
wheel_controller         active
servo_controller         active
```

## 4. Launch RViz2

Open a **third terminal** and source the workspace.

To launch RViz2 normally:

```bash
rviz2
```

Alternatively, load the existing LiDAR configuration:

```bash
rviz2 -d $(ros2 pkg prefix osr_gazebo)/share/osr_gazebo/rviz/lidar_test.rviz
```

### RViz2 Configuration

Set the following:

**Global Options**
- Fixed Frame: `base_link`

**RobotModel**
- Description Source: `Topic`
- Description Topic: `/robot_description`

**LaserScan**
- Topic: `/scan`
- Style: `Points`

**Note:** The LiDAR points will move relative to the rover when using `base_link` as the Fixed Frame. To visualise measurements relative to a stationary environment, a working odometry transform is required.

## 5. Drive the Rover

Open a **fourth terminal** and source the workspace.

Start keyboard teleoperation:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```


## 6 Rebuilding After Changes

If you modify the Gazebo package, rebuild it using:

```bash
cd ~/sumsa_rover_ws
source /opt/ros/jazzy/setup.bash

colcon build --symlink-install --packages-select osr_gazebo

source install/setup.bash
```
