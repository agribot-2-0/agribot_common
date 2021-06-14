#!/usr/bin/env python2

import argparse
import rospy
import math
import pandas as pd
from std_msgs.msg import Float32
from agribot_msgs.msg import AgribotCaterpillar


class PidTunning:
    def __init__(self):
        #         super(ImuCalibrationOnline, self).__init__(rospy.loginfo)
        self.setpoint_sub = None
        self.processvalue_sub = None
        self.data_setpoint = {"timestamp": [], "setpoint": []}
        self.data_processvalue = {"timestamp": [], "processvalue": []}
        self.current_setpoint = 0
        self.current_proccesvalue = 0
        self.control_publisher = rospy.Publisher("/agribot/control/caterpillar",
                                                 AgribotCaterpillar,
                                                 queue_size=10)

        self.control_msg = AgribotCaterpillar()
        self.controls = [0, -0.5, 0.5, 0, -0.15, 0.15, 0, -0.075, 0.075]

    def sp_cb(self, cb_msg):
        pass

    def pv_cb(self, cb_msg):
        time = rospy.get_time()
        self.current_proccesvalue = cb_msg.data
        self.data_processvalue["timestamp"].append(time)
        self.data_processvalue["processvalue"].append(cb_msg.data)
        self.data_setpoint["timestamp"].append(time)
        self.data_setpoint["setpoint"].append(self.current_setpoint)

    def collect_data(self, topic_set_point, topic_process_value):
        # Collect data until Ctrl-C is pressed
        # Ctrl-C is catched with try-except, so it doesn't stop the program
        # try:
        self.setpoint_sub = rospy.Subscriber(topic_set_point,
                                             AgribotCaterpillar,
                                             self.sp_cb,
                                             queue_size=100)
        self.processvalue_sub = rospy.Subscriber(topic_process_value,
                                                 Float32,
                                                 self.pv_cb,
                                                 queue_size=100)
        print('[PidTunning] Calibration started')

        for control in self.controls:
            print('[PidTunning] Sending control {}'.format(control))
            rate = rospy.Rate(10)  # 10hz
            self.current_setpoint = control
            counter = 0
            while not rospy.is_shutdown():
                self.control_msg.front_angular = control
                self.control_publisher.publish(self.control_msg)
                if control > 0 and self.current_proccesvalue > math.radians(40): break
                if control < 0 and self.current_proccesvalue < math.radians(-40): break
                if counter > 50 and control == 0: break
                counter += 1
                rate.sleep()

        print('[PidTunning] stopped.')
        self.setpoint_sub.unregister()
        self.processvalue_sub.unregister()

    def save_to_csv(self, filename):
        df_setpoint = pd.DataFrame(data=self.data_setpoint)
        df_processvalue = pd.DataFrame(data=self.data_processvalue)

        df_setpoint.set_index("timestamp", inplace=True)
        df_processvalue.set_index("timestamp", inplace=True)
        result = df_setpoint.join(df_processvalue, how='outer')
        # result = result.dropna()
        result.to_csv(filename)


if __name__ == '__main__':
    try:
        PARSER = argparse.ArgumentParser(description='PID Tuning to file')

        # PARSER.add_argument('-i', metavar='input', required=True, help='setpoint data topic')
        # PARSER.add_argument('-o', metavar='output', required=True, help='process value data topic')
        # PARSER.add_argument('-f', metavar='filename', required=True, help='filename')
        # ARGS = PARSER.parse_args()

        # Initialize
        rospy.init_node('pid_tunning')
        PT = PidTunning()

        # Collect data and compute parameters
        PT.collect_data("/agribot/control/caterpillar", "/agribot/encoder/cart/front")
        PT.save_to_csv("output.csv")

    except rospy.ROSInterruptException:
        pass
