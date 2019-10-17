# coding: utf-8

from __future__ import division, print_function

import tensorflow as tf
import numpy as np
import cv2
import time
import os

from utils.misc_utils import parse_anchors, read_class_names
from utils.nms_utils import gpu_nms
from utils.plot_utils import get_color_table, plot_one_box
from utils.data_aug import letterbox_resize

from model1 import yolov3

def session(anchor_path = r'D:\GithubProjects\TM\data\yolo_anchors.txt', new_size = [416, 416], class_name_path = r'D:\GithubProjects\TM\data\coco.names', restore_path = r'D:\GithubProjects\TM\data\darknet_weights\yolov3.ckpt'):
    # Initilizing
    anchors = parse_anchors(anchor_path)
    classes = read_class_names(class_name_path)
    num_class = len(classes)

    color_table = get_color_table(num_class)

    # Initializing session
    #sess2 = tf.Session()
    input_data = tf.placeholder(tf.float32, [1, new_size[1], new_size[0], 3], name='input_data')
    yolo_model = yolov3(num_class, anchors)
    with tf.variable_scope('yolov3'):
        pred_feature_maps = yolo_model.forward(input_data, False)
    pred_boxes, pred_confs, pred_probs = yolo_model.predict(pred_feature_maps)

    pred_scores = pred_confs * pred_probs

    boxes, scores, labels = gpu_nms(pred_boxes, pred_scores, num_class, max_boxes=50, score_thresh=0.5, nms_thresh=0.45)

    #Tensorflow
    sess2 = tf.Session()
    saver = tf.train.Saver()
    saver.restore(sess2, restore_path)


    return sess2, boxes, scores, labels, input_data, classes, color_table

def obj_rec(input_image, sess2, boxes, scores, labels, input_data, classes, color_table, new_size = [416, 416], letterbox_resize1 = True):
    start = time.time()
    #Actual image processing
    img_ori = cv2.imread(input_image)
    if letterbox_resize1:
        img, resize_ratio, dw, dh = letterbox_resize(img_ori, new_size[0], new_size[1])
    else:
        height_ori, width_ori = img_ori.shape[:2]
        img = cv2.resize(img_ori, tuple(new_size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.asarray(img, np.float32)
    img = img[np.newaxis, :] / 255.

    boxes_, scores_, labels_ = sess2.run([boxes, scores, labels], feed_dict={input_data: img})

    # rescale the coordinates to the original image
    if letterbox_resize:
        boxes_[:, [0, 2]] = (boxes_[:, [0, 2]] - dw) / resize_ratio
        boxes_[:, [1, 3]] = (boxes_[:, [1, 3]] - dh) / resize_ratio
    else:
        boxes_[:, [0, 2]] *= (width_ori/float(new_size[0]))
        boxes_[:, [1, 3]] *= (height_ori/float(new_size[1]))

    end = time.time()
    inference_time = end - start

    print("Inference time: " + str(round(inference_time)) + "ms")
    print('*' * 30)
    print("box coords:")
    print(boxes_)
    print('*' * 30)
    print("scores:")
    print(scores_)
    print('*' * 30)
    print("labels:")
    print(', '.join([classes[x] for x in labels_]))
    print('*' * 30)

    for i in range(len(boxes_)):
        x0, y0, x1, y1 = boxes_[i]
        plot_one_box(img_ori, [x0, y0, x1, y1], label=classes[labels_[i]] + ', {:.2f}%'.format(scores_[i] * 100), color=color_table[labels_[i]])

    label = 'Inference time: %.2f ms' % (inference_time)
    cv2.putText(img_ori, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    filepath, file_extension = os.path.splitext(input_image)
    processed_img = os.path.join(filepath + "_yolo_out" + file_extension)

    cv2.imwrite(processed_img, img_ori)
    print("Path to processed image: " + processed_img)

    return processed_img

#sess2, boxes, scores, labels, input_data, classes, color_table = session()
#path = obj_rec(r'C:\Users\Stefan\Downloads\yolo1.jpg', sess2, boxes, scores, labels, input_data, classes, color_table)