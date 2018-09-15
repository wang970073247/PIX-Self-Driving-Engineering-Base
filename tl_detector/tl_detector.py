#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped, Pose
from styx_msgs.msg import TrafficLightArray, TrafficLight
#from styx_msgs.msg import Lane
#from autoware_msgs.msg import lane
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from light_classification.tl_classifier import TLClassifier
import tf
import cv2
import yaml
import math

STATE_COUNT_THRESHOLD = 3

class TLDetector(object):
    def __init__(self):
        rospy.init_node('tl_detector')

        self.pose = None
        self.waypoints = None
        self.camera_image = None
        self.lights = []
	# initializae the state of the program
        self.state = TrafficLight.UNKNOWN
        self.last_state = TrafficLight.UNKNOWN
        self.last_wp = -1
        self.state_count = 0
        self.last_waypoint = None
        self.stop_line_waypoints = None
	# make the first function initalizae
        self.bridge = CvBridge()
        self.light_classifier = TLClassifier()
        self.listener = tf.TransformListener()

        sub1 = rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        #sub2 = rospy.Subscriber('/base_waypoints', lane, self.waypoints_cb)

        '''
        /vehicle/traffic_lights provides you with the location of the traffic light in 3D map space and
        helps you acquire an accurate ground truth data source for the traffic light
        classifier by sending the current color state of all traffic lights in the
        simulator. When testing on the vehicle, the color state will not be available. You'll need to
        rely on the position of the light and the camera image to predict it.
        '''
        #sub3 = rospy.Subscriber('/vehicle/traffic_lights', TrafficLightArray, self.traffic_cb)
        sub6 = rospy.Subscriber('/camera0/image_raw', Image, self.image_cb)
        self.image_nb_pub = rospy.Publisher('/image_traffic_light', Image, queue_size=1)
	
	self.taffic_light_state = rospy.Publisher('/chatter',Int32,queue_size=1)
        
        config_string = rospy.get_param("/traffic_light_config")
        self.config = yaml.load(config_string)

        self.upcoming_red_light_pub = rospy.Publisher('/traffic_waypoint', Int32, queue_size=1)
        
        self.bridge = CvBridge()
        self.light_classifier = TLClassifier()
        self.listener = tf.TransformListener()

        self.state = TrafficLight.UNKNOWN
        self.last_state = TrafficLight.UNKNOWN
        self.last_wp = -1
        self.state_count = 0
        self.last_waypoint = None
        self.stop_line_waypoints = None
        self.pose = None
        self.has_image = None

        rospy.spin()

    def pose_cb(self, msg):
        self.pose = msg

    def waypoints_cb(self, waypoints):
        self.waypoints = waypoints

    def traffic_cb(self, msg):
        self.lights = msg.lights

    def image_cb(self, msg):
        """Identifies red lights in the incoming camera image and publishes the index
            of the waypoint closest to the red light's stop line to /traffic_waypoint

        Args:
            msg (Image): image from car-mounted camera

        """
        self.has_image = True
        self.camera_image = msg

	light_wp = -1

        light_wp, state = self.process_traffic_lights()

        '''
        Publish upcoming red lights at camera frequency.
        Each predicted state has to occur `STATE_COUNT_THRESHOLD` number
        of times till we start using it. Otherwise the previous stable state is
        used.
        '''
        if self.state != state:
            self.state_count = 0
            self.state = state

        elif self.state_count >= STATE_COUNT_THRESHOLD:
            self.last_state = self.state
            light_wp = light_wp if state == TrafficLight.RED else -1
            self.last_wp = light_wp
            self.upcoming_red_light_pub.publish(Int32(light_wp))
            if state == TrafficLight.RED:
            	self.state_count = 0 

        else:
            self.upcoming_red_light_pub.publish(Int32(self.last_wp))
        self.state_count += 1
        rospy.loginfo("TL:   --- count-------------------------------------- %s",self.state_count)

    def get_closest_waypoint(self, waypoints, vehicle_pose):
        
        if self.last_waypoint:
           
            closest_waypoint = self.get_closest_local_waypoint(waypoints, vehicle_pose, self.last_waypoint)
        else:
           
            closest_waypoint = self.get_closest_global_waypoint(waypoints, vehicle_pose)
        self.last_waypoint = closest_waypoint
        return closest_waypoint

    def get_closest_global_waypoint(self, waypoints, vehicle_pose):
        
        closest_dist = 1000000
        closest_waypoint = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2 )#+ (a.z-b.z)**2)
        for i in range(1, len(waypoints)):
            dist = dl(waypoints[i].pose.pose.position, vehicle_pose.position)
            if dist < closest_dist:
                closest_waypoint = i
                closest_dist = dist
        return closest_waypoint

    def get_closest_local_waypoint(self, waypoints, vehicle_pose, last_waypoint):
       
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2)
        closest_dist = dl(waypoints[last_waypoint].pose.pose.position, vehicle_pose.position)
        closest_waypoint = last_waypoint

        MIN_WAYPOINTS_TO_SEARCH = 10

       
        next_waypoint = last_waypoint + 1 if last_waypoint + 1 < len(waypoints) else 0
        waypoints_checked = MIN_WAYPOINTS_TO_SEARCH
        while waypoints_checked > 0:
            dist = dl(waypoints[next_waypoint].pose.pose.position, vehicle_pose.position)
            if dist < closest_dist:
                closest_dist = dist
                closest_waypoint = next_waypoint
            next_waypoint = next_waypoint + 1 if next_waypoint + 1 < len(waypoints) else 0
            waypoints_checked = waypoints_checked - 1

        # Search
        prev_waypoint = last_waypoint - 1 if last_waypoint - 1 >= 0 else len(waypoints) - 1
        waypoints_checked = MIN_WAYPOINTS_TO_SEARCH
        while waypoints_checked > 0:
            dist = dl(waypoints[prev_waypoint].pose.pose.position, vehicle_pose.position)
            if dist < closest_dist:
                closest_dist = dist
                closest_waypoint = prev_waypoint
            prev_waypoint = prev_waypoint - 1 if prev_waypoint - 1 >= 0 else len(waypoints) - 1
            waypoints_checked = waypoints_checked - 1

        return closest_waypoint

    def find_stop_line_waypoints(self):
        
        if self.waypoints and not self.stop_line_waypoints:
          
            stop_line_positions = self.config['stop_line_positions']
            
           
            self.stop_line_waypoints = []        
            for i in range(len(stop_line_positions)):
                pose = Pose()
                pose.position.x = stop_line_positions[i][0]
                pose.position.y = stop_line_positions[i][1]
                self.stop_line_waypoints.append(self.get_closest_global_waypoint(self.waypoints.waypoints, pose))



    def get_light_state(self, light=None):
        """Determines the current color of the traffic light

        Args:
            light (TrafficLight): light to classify

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        # TLClassifier takes a lot of time to initialize. Wait still (output RED) till it's ready
        if self.light_classifier is None:
            rospy.logwarn("TLDetector::get_light_state() - Classifier not ready!")
            return TrafficLight.RED

        if(not self.has_image):
            self.prev_light_loc = None
            return False

        cv_image = self.bridge.imgmsg_to_cv2(self.camera_image, "rgb8")

        rospy.loginfo("TL: classifier_result---0---      %s",[0])
        #Get classification
        # TODO: when classification is ready, replace it with:
        state = self.light_classifier.get_classification(cv_image)
        rospy.loginfo("TL: classifier_result---0---      %s",state)
        self.taffic_light_state.publish(state)
        return state





    def process_traffic_lights(self):
        """Finds closest visible traffic light, if one exists, and determines its
            location and color

        Returns:
            int: index of waypoint closes to the upcoming stop line for a traffic light (-1 if none exists)
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
	light_wp = -1
        light = None

        
        if(self.pose and self.waypoints):
            car_wp = self.get_closest_waypoint(self.waypoints.waypoints, self.pose.pose)

           
            if(self.waypoints):
                num_waypoints = len(self.waypoints.waypoints)
                
                
                self.find_stop_line_waypoints()
                
               
                min_offset = num_waypoints
                closest_line = -1
                light_wp = -1
                for i in range(len(self.stop_line_waypoints)):
                    line_wp = self.stop_line_waypoints[i]        
                    offset = (line_wp - car_wp) if (line_wp - car_wp) >= 0 else (line_wp - car_wp + num_waypoints)
                    if offset < min_offset:
                        min_offset = offset
                        closest_line = i
                        light_wp = line_wp
                
                #if closest_line >= 0:
                    #light = self.lights[closest_line]

        #if light:
        state = self.get_light_state()
        return light_wp, state
       # self.waypoints = None
       # return -1, TrafficLight.UNKNOWN

if __name__ == '__main__':
    try:
        TLDetector()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start traffic node.')
