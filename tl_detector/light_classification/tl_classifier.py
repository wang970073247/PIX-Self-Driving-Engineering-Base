from styx_msgs.msg import TrafficLight

import numpy as np
import os
import tensorflow as tf


import rospy

SCORE_THRESHOLD = 0.5
LABEL2STATE_MAP = {1: TrafficLight.RED,
                   2: TrafficLight.YELLOW,
                   3: TrafficLight.GREEN}

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        # Variables
        current_path = os.getcwd()
        PATH_TO_CKPT = os.path.join(current_path, 'light_classification', 'light_graph', 'frozen_inference_graph.pb')
        NUM_CLASSES = 3
        
        # Load a (frozen) Tensorflow model into memory
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.sess =  tf.Session(graph=self.detection_graph)    
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')


        
    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        t0 = rospy.get_time()

        # Actual detection.
        image_np_expanded = np.expand_dims(image, axis=0)
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
  
        state = self.get_state(scores, classes)
        dt = rospy.get_time() - t0
        rospy.loginfo("TLClassifier::get_classification() - Detection elapsed time: %f", dt)
        rospy.loginfo("TLClassifier::get_classification() - state: %d", state)
        return state
    
    def get_state(self, scores, classes, boxes=None):
        scores_flat = scores.flatten()
        max_score = np.max(scores_flat)
        
        if max_score < SCORE_THRESHOLD:
            return TrafficLight.UNKNOWN
        else:
            label = classes.flatten()[np.argmax(scores_flat)]
            return LABEL2STATE_MAP[label]
