import rospy


def get_parameter(param_name):
    if not rospy.has_param(param_name):
        raise ValueError("'{}' param not set".format(param_name))
    return rospy.get_param(param_name)
