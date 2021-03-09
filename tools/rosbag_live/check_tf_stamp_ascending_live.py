#!/usr/bin/env python
import rospy
from tf2_msgs.msg import TFMessage

previous_stamp = None


def tf_callback(msg):
    global previous_stamp

    # First tf callback - set previous stamp
    if previous_stamp is None:
        previous_stamp = msg.transforms[0].header.stamp
        return

    for transform in msg.transforms:
        if previous_stamp > transform.header.stamp:
            print('Ascending order broke at time {} for {} => {} transform'.
                  format(transform.header.stamp.to_sec(),
                         transform.header.frame_id, transform.child_frame_id))
    previous_stamp = msg.transforms[0].header.stamp


def listener():
    rospy.init_node('tf_listener', anonymous=True)
    rospy.Subscriber("/tf", TFMessage, tf_callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
