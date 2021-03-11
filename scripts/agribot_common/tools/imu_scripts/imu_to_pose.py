#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseStamped


class Callbacker(object):
    def __init__(self):
        self.imu_1_sub = rospy.Subscriber("agribot/imu/filtered", Imu,
                                          self.imu_1_callback)
        self.imu_2_sub = rospy.Subscriber("agribot/imu/raw", Imu,
                                          self.imu_2_callback)

        self.pose_1_pub = rospy.Publisher("pose_1_pub",
                                          PoseStamped,
                                          queue_size=1)
        self.pose_2_pub = rospy.Publisher("pose_2_pub",
                                          PoseStamped,
                                          queue_size=1)

    def imu_1_callback(self, msg):
        pose = PoseStamped()
        pose.header.frame_id = "odom"
        pose.header.stamp = rospy.Time.now()
        pose.pose.orientation = msg.orientation
        self.pose_1_pub.publish(pose)

    def imu_2_callback(self, msg):
        pose = PoseStamped()
        pose.header.frame_id = "odom"
        pose.header.stamp = rospy.Time.now()
        pose.pose.orientation = msg.orientation
        self.pose_2_pub.publish(pose)


rospy.init_node("imu_to_pose")
CB = Callbacker()
rospy.spin()
