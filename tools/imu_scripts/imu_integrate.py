#!/usr/bin/env python

import rospy
import tf
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseStamped


class Callbacker:

    def __init__(self):
        self.imu_sub = rospy.Subscriber("agribot/imu/raw", Imu, self.imu_callback)
        self.pose_integrate_pub = rospy.Publisher("pose_integrate_pub", PoseStamped, queue_size=1)

        self.r = 0.0
        self.p = 0.0
        self.y = 0.0
        self.prev_stamp = None

    def imu_callback(self, msg):
        if self.prev_stamp is None:
            self.prev_stamp = msg.header.stamp
        else:
            dt = (msg.header.stamp - self.prev_stamp).to_sec()
            self.prev_stamp = msg.header.stamp

            self.r += (msg.angular_velocity.x*dt)
            self.p += (msg.angular_velocity.y*dt)
            self.y += (msg.angular_velocity.z*dt)

            print(self.r, self.p, self.y)

            pose = PoseStamped()
            pose.header.frame_id = "odom"
            pose.header.stamp = rospy.Time.now()
            quat = tf.transformations.quaternion_from_euler(self.r, self.p, self.y)
            pose.pose.orientation.x = quat[0]
            pose.pose.orientation.y = quat[1]
            pose.pose.orientation.z = quat[2]
            pose.pose.orientation.w = quat[3]
            self.pose_integrate_pub.publish(pose)


rospy.init_node("imu_integrate")
cb = Callbacker()
rospy.spin()
