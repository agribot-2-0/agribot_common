#!/usr/bin/env python3

import rosbag
import rospy
import tf2_py
import tf2_ros
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud
import sensor_msgs
from sensor_msgs.msg import PointField
import sensor_msgs.point_cloud2 as pc2

import numpy as np
from cv_bridge import CvBridge
import cv2
import open3d
import ctypes  # convert float to uint32

import traceback
import logging
import warnings
import argparse

# The data structure of each point in ros PointCloud2: 16 bits = x + y + z + rgb
FIELDS_XYZ = [
    PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
    PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
    PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
]
FIELDS_XYZRGB = FIELDS_XYZ + \
    [PointField(name='rgb', offset=12, datatype=PointField.UINT32, count=1)]


# bit operations
def unpack_rgb_uint32(rgb_uint32):
    return ((rgb_uint32 & 0x00ff0000) >> 16, (rgb_uint32 & 0x0000ff00) >> 8,
            (rgb_uint32 & 0x000000ff))


def unpack_rgb_float(rgb_float):
    return unpack_rgb_uint32(
        int(
            ctypes.cast(ctypes.pointer(ctypes.c_float(rgb_float)),
                        ctypes.POINTER(ctypes.c_uint32)).contents.value))


def convert_ros_cloud_to_open3d(ros_cloud):

    # Get cloud data from ros_cloud
    field_names = [field.name for field in ros_cloud.fields]
    cloud_data = pc2.read_points(ros_cloud, skip_nans=True, field_names=field_names)

    # Check empty
    open3d_cloud = open3d.geometry.PointCloud()

    # Set open3d_cloud
    if "rgb" in field_names:
        IDX_RGB_IN_FIELD = 3  # x, y, z, rgb

        xyz = []
        rgb = []
        for x, y, z, _rgb in cloud_data:
            xyz.append((x, y, z))
            if type(cloud_data[0][IDX_RGB_IN_FIELD]) == float:
                rgb.append((unpack_rgb_float(_rgb)))
            else:
                rgb.append((unpack_rgb_uint32(_rgb)))

        # combine
        if (len(xyz) == 0):
            return None
        open3d_cloud.points = open3d.utility.Vector3dVector(np.array(xyz))
        open3d_cloud.colors = open3d.utility.Vector3dVector(np.array(rgb) / 255.0)
    elif "intensity" in field_names:
        xyz = []
        rgb = []
        for x, y, z, intensity in cloud_data:
            xyz.append((x, y, z))
            rgb.append((intensity, intensity, intensity))
        if (len(xyz) == 0):
            return None
        open3d_cloud.points = open3d.utility.Vector3dVector(np.array(xyz))
        open3d_cloud.colors = open3d.utility.Vector3dVector(np.array(rgb) / 255.0)
    else:
        xyz = [(x, y, z) for x, y, z in cloud_data]  # get xyz
        if (len(xyz) == 0):
            return None
        open3d_cloud.points = open3d.utility.Vector3dVector(np.array(xyz))

    # return
    return open3d_cloud


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
                tf_buffer_core.set_transform_static(msg_tf, "default_authority")

    return tf_buffer_core


def find_closest_tf(tf_buffer_core, pointcloud, target_frame):
    try:
        transform = tf_buffer_core.lookup_transform_core(target_frame, pointcloud.header.frame_id,
                                                         pointcloud.header.stamp)
    except tf2_ros.ExtrapolationException as e:
        logging.info('{}. Taking latest instead'.format(e))
        transform = tf_buffer_core.lookup_transform_core(target_frame, pointcloud.header.frame_id,
                                                         rospy.Time(0))

    return transform


def save_image(images):
    image_time_diffs = np.array([abs(snapshot_time - t) for t, img in images])
    closest_img_idx = np.argmin(image_time_diffs)
    closest_img = images[closest_img_idx][1]
    bridge = CvBridge()
    cv2_img = bridge.imgmsg_to_cv2(closest_img, "bgr8")
    cv2.imwrite('{}.jpg'.format(output_name), cv2_img)

    return closest_img_idx


def save_pointcloud(pointclouds):
    pointcloud_time_diffs = np.array([abs(snapshot_time - t) for t, img in pointclouds])
    closest_pointcloud_idx = np.argmin(pointcloud_time_diffs)
    closest_pointcloud = pointclouds[closest_pointcloud_idx][1]
    if closest_pointcloud.header.frame_id != pc_target_frame:
        try:
            transform = find_closest_tf(tf_buffer_core, closest_pointcloud, pc_target_frame)
            closest_pointcloud_in_target_frame = do_transform_cloud(closest_pointcloud, transform)
        except Exception as e:
            logging.error(traceback.format_exc())
            exit()

        logging.info('Transformed pointcloud from {} to {} frame'.format(
            closest_pointcloud.header.frame_id, pc_target_frame))

    else:
        logging.info('Frame ids match, no transform necessary...')
        closest_pointcloud_in_target_frame = closest_pointcloud
    # Save pointcloud
    if (closest_pointcloud_in_target_frame.width == 0
            or closest_pointcloud_in_target_frame.height == 0):
        logging.error(
            'Pointcloud {} has no width or heights - assuiming empty.'.format(pc_target_frame))
        return None
    received_open3d_cloud = convert_ros_cloud_to_open3d(closest_pointcloud_in_target_frame)

    # write to file
    output_filename = output_name + ".pcd"
    open3d.io.write_point_cloud(output_filename, received_open3d_cloud)

    return closest_pointcloud_idx


parser = argparse.ArgumentParser()
parser.add_argument('--input_bag_path')
parser.add_argument('--image_topic', default='/zed2_node/rgb/image_rect_color')
parser.add_argument('--pc_topic', default='/agribot/obstacle_detection/front/3d/lidar/point_cloud')
parser.add_argument('--pc_target_frame', default='zed2_left_camera_frame')
parser.add_argument('--snapshot_time', default=1.0)
parser.add_argument('--output_name', default='out1')

args = parser.parse_args()
input_bag_path = args.input_bag_path
image_topic = str(args.image_topic)
pc_topic = args.pc_topic
pc_target_frame = args.pc_target_frame
snapshot_time = args.snapshot_time
output_name = args.output_name
topics = [image_topic, pc_topic]

logging.getLogger().setLevel(logging.INFO)
logging.getLogger('rospy').setLevel(logging.WARN)

with rosbag.Bag(input_bag_path) as inbag:

    start_time_s = inbag.get_start_time()
    end_time_s = inbag.get_end_time()
    bag_length_s = end_time_s - start_time_s

    if snapshot_time > bag_length_s:
        logging.error('[SNAPSHOT_TIME > bag_length_s] No data saved, exiting...')
        exit()

    tf_buffer_core = tf_buffer_core_from_bag(inbag)

    images = []
    pointclouds = []

    for topic, msg, t in inbag.read_messages(topics=topics):
        if topic == image_topic:
            t_from_start_s = t.to_sec() - start_time_s
            images.append((t_from_start_s, msg))
        elif topic == pc_topic:
            t_from_start_s = t.to_sec() - start_time_s
            pointclouds.append((t_from_start_s, msg))
        else:
            logging.warn('Unsupported topic')

if (len(pointclouds) == 0):
    logging.warn('There is no pointclouds on given topic.')
    closest_img_idx = save_image(images)
    logging.info('Saved image #{} from time {} for bag {}'.format(closest_img_idx, snapshot_time,
                                                                  input_bag_path))
elif (len(images) == 0):
    logging.warn('There is no images on given topic.')
    closest_pointcloud_idx = save_pointcloud(pointclouds)
    logging.info('Saved pointcloud #{} from time {} for bag {}'.format(
        closest_pointcloud_idx, snapshot_time, input_bag_path))
elif (len(pointclouds) == 0 and len(images) == 0):
    logging.error(
        'There is no images or pointclouds on given topic in bag{}.Exiting.'.format(input_bag_path))
    exit
else:
    closest_img_idx = save_image(images)
    closest_pointcloud_idx = save_pointcloud(pointclouds)
    logging.info('Saved image #{} and pointcloud #{} from time {} for bag {}'.format(
        closest_img_idx, closest_pointcloud_idx, snapshot_time, input_bag_path))
