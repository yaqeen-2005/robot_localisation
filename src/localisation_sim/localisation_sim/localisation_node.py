import rclpy
import math
from rclpy.node import Node
from nav_msgs.msg import Odometry
import random

class localisationNode(Node):
	def __init__(self):
		super().__init__('localisation_node')
		self.create_subscription(Odometry, '/odom', self.odom_callback,10)
		self.x = 0.0
		self.y = 0.0
		self.dt = 0.0
		self.previous_time = None
		self.theta = 0.0
	def odom_callback(self, msg):
		x = msg.pose.pose.position.x
		y = msg.pose.pose.position.y
		v = msg.twist.twist.linear.x
		omega = msg.twist.twist.angular.z
		v += random.gauss(0, 0.02)
		omega += random.gauss(0, 0.01)
		current_time = (
   			msg.header.stamp.sec +
    		msg.header.stamp.nanosec * 1e-9
		)
		if self.previous_time is None:
			self.previous_time = current_time
			return

		self.dt = current_time - self.previous_time
		self.previous_time = current_time

		if self.dt <= 0:
			return
		
		self.theta += omega * self.dt

		self.x += v * math.cos(self.theta) * self.dt
		self.y += v * math.sin(self.theta) * self.dt
		self.get_logger().info( f"Estimated: x={self.x:.3f}, "
    		f"y={self.y:.3f}, theta={self.theta:.3f}")
		
def main():
    rclpy.init()
    node = localisationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
