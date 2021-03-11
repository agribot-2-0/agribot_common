#!/usr/bin/env python

import rospy
import tf
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseStamped


class Callbacker(object):  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.imu_sub = rospy.Subscriber("agribot/imu/raw", Imu,
                                        self.imu_callback)
        self.pose_integrate_pub = rospy.Publisher("pose_integrate_pub",
                                                  PoseStamped,
                                                  queue_size=1)

        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.prev_stamp = None

    def imu_callback(self, msg):
        if self.prev_stamp is None:
            self.prev_stamp = msg.header.stamp
        else:
            dt = (msg.header.stamp - self.prev_stamp).to_sec()  # pylint: disable=invalid-name
            self.prev_stamp = msg.header.stamp

            self.roll += (msg.angular_velocity.x * dt)
            self.pitch += (msg.angular_velocity.y * dt)
            self.yaw += (msg.angular_velocity.z * dt)

            print(self.roll, self.pitch, self.yaw)

            pose = PoseStamped()
            pose.header.frame_id = "odom"
            pose.header.stamp = rospy.Time.now()
            quat = tf.transformations.quaternion_from_euler(
                self.roll, self.pitch, self.yaw)
            pose.pose.orientation.x = quat[0]
            pose.pose.orientation.y = quat[1]
            pose.pose.orientation.z = quat[2]
            pose.pose.orientation.w = quat[3]
            self.pose_integrate_pub.publish(pose)


rospy.init_node("imu_integrate")
CB = Callbacker()
rospy.spin()
