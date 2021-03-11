#!/usr/bin/env python
import rospy
from tf2_msgs.msg import TFMessage

PREVIOUS_STAMP = None


def tf_callback(msg):
    global PREVIOUS_STAMP

    # First tf callback - set previous stamp
    if PREVIOUS_STAMP is None:
        PREVIOUS_STAMP = msg.transforms[0].header.stamp
        return

    for transform in msg.transforms:
        if PREVIOUS_STAMP > transform.header.stamp:
            print('Ascending order broke at time {} for {} => {} transform'.
                  format(transform.header.stamp.to_sec(),
                         transform.header.frame_id, transform.child_frame_id))
    PREVIOUS_STAMP = msg.transforms[0].header.stamp


def listener():
    rospy.init_node('tf_listener', anonymous=True)
    rospy.Subscriber("/tf", TFMessage, tf_callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
