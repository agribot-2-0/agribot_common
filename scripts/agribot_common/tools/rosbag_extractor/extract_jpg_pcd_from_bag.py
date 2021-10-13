#!/usr/bin/env python2

import rosbag
import rospy
import tf2_py
import tf2_ros
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud

import numpy as np
from cv_bridge import CvBridge
import cv2
import pypcd

import traceback
import logging
import warnings


def tf_buffer_core_from_bag(bag):

    tf_buffer_core = tf2_py.BufferCore(rospy.Duration(10000000))

    # Suppress "UserWarning: translation should be of type Quaternion/Vector3" warnings from tf_buffer_core.set_transform
    warnings.simplefilter('ignore', UserWarning)

    for topic, msg, t in bag.read_messages(topics=['/tf', '/tf_static']):
        if topic == '/tf':
            for msg_tf in msg.transforms:
                tf_buffer_core.set_transform(msg_tf, "default_authority")
        elif topic == '/tf_static':
            for msg_tf in msg.transforms:
                tf_buffer_core.set_transform_static(
                    msg_tf, "default_authority")

    return tf_buffer_core


def find_closest_tf(tf_buffer_core, pointcloud, target_frame):
    try:
        transform = tf_buffer_core.lookup_transform_core(
            target_frame, pointcloud.header.frame_id, pointcloud.header.stamp)
    except tf2_ros.ExtrapolationException as e:
        logging.info('{}. Taking latest instead'.format(e))
        transform = tf_buffer_core.lookup_transform_core(
            target_frame, pointcloud.header.frame_id, rospy.Time(0))

    return transform


INPUT_BAG_PATH = '/home/olek/agribot/logs/08_2021/11_08_2021/begin_end_line_v1.bag'
IMAGE_TOPIC = '/zed2_node/rgb/image_rect_color'
POINTCLOUD_TOPIC = '/agribot/obstacle_detection/front/3d/stereo_camera/point_cloud'
# POINTCLOUD_TOPIC = '/agribot/obstacle_detection/front/3d/lidar/point_cloud'
POINTCLOUD_TARGET_FRAME = 'zed2_left_camera_frame'
SNAPSHOT_TIME = 1.0    # wrt bag time (not header time)
OUTPUT_NAME = 'out1'

TOPICS = [IMAGE_TOPIC, POINTCLOUD_TOPIC]

logging.getLogger().setLevel(logging.INFO)
logging.getLogger('rospy').setLevel(logging.WARN)


with rosbag.Bag(INPUT_BAG_PATH) as inbag:

    start_time_s = inbag.get_start_time()
    end_time_s = inbag.get_end_time()
    bag_length_s = end_time_s - start_time_s

    if SNAPSHOT_TIME > bag_length_s:
        logging.error(
            '[SNAPSHOT_TIME > bag_length_s] No data saved, exiting...')
        exit()

    tf_buffer_core = tf_buffer_core_from_bag(inbag)

    images = []
    pointclouds = []

    for topic, msg, t in inbag.read_messages(topics=TOPICS):
        if topic == IMAGE_TOPIC:
            t_from_start_s = t.to_sec() - start_time_s
            images.append((t_from_start_s, msg))
        elif topic == POINTCLOUD_TOPIC:
            t_from_start_s = t.to_sec() - start_time_s
            pointclouds.append((t_from_start_s, msg))
        else:
            logging.warn('Unsupported topic')


image_time_diffs = np.array([abs(SNAPSHOT_TIME - t) for t, img in images])
closest_img_idx = np.argmin(image_time_diffs)
pointcloud_time_diffs = np.array(
    [abs(SNAPSHOT_TIME - t) for t, img in pointclouds])
closest_pointcloud_idx = np.argmin(pointcloud_time_diffs)


closest_img = images[closest_img_idx][1]
closest_pointcloud = pointclouds[closest_pointcloud_idx][1]

# Transform pointcloud to target frame
if closest_pointcloud.header.frame_id != POINTCLOUD_TARGET_FRAME:
    try:
        transform = find_closest_tf(
            tf_buffer_core, closest_pointcloud, POINTCLOUD_TARGET_FRAME)
        closest_pointcloud_in_target_frame = do_transform_cloud(
            closest_pointcloud, transform)
    except Exception as e:
        logging.error(traceback.format_exc())
        exit()

    logging.info('Transformed pointcloud from {} to {} frame'.format(
        closest_pointcloud.header.frame_id, POINTCLOUD_TARGET_FRAME))

else:
    logging.info('Frame ids match, no transform necessary...')
    closest_pointcloud_in_target_frame = closest_pointcloud

# Save image
bridge = CvBridge()
cv2_img = bridge.imgmsg_to_cv2(closest_img, "bgr8")
cv2.imwrite('{}.jpg'.format(OUTPUT_NAME), cv2_img)

# Save pointcloud
pypcd_pointcloud = pypcd.PointCloud.from_msg(
    closest_pointcloud_in_target_frame)
pypcd_pointcloud.save('{}.pcd'.format(OUTPUT_NAME))

logging.info('Saved image #{} and pointcloud #{} from time {} for bag {}'.format(
    closest_img_idx, closest_pointcloud_idx, SNAPSHOT_TIME, INPUT_BAG_PATH))
