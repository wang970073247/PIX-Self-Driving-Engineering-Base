![ROS_cover](./img/ROS_cover.png)
机器人几乎拥有者相同的架构。
ROS 提供了强劲的通信系统，允许不同组件互相沟通。<br>
机器人从构造上来说，都可以执行三个大致步骤：感知、决策与驱动。
![robotic_structure](./img/robotic_structure.png)
ROS 管理这三个复杂的步骤时，将每个分解为很多更小的单元，我们称之为 Node。<br>
通常，系统上的每个 Node 负责机器人功能总体的一个特定的小部分。
例如，系统中可能每个传感器都有相应 Node
此外还有 Node 对应位置估算，行为执行和马达控制。
![node](./img/node.png)
