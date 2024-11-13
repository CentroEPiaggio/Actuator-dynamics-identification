import numpy as np
import yaml
import rclpy
from rclpy.node import Node
from pi3hat_moteus_int_msgs.msg import JointsCommand, JointsStates, PacketPass
from sensor_msgs.msg import  Imu, JointState
from geometry_msgs.msg import Twist
import math 


""" get up the robot by sending refernces interpolating from current to default pos """

class Impulse(Node):
    def __init__(self):
        super().__init__('impulse_test')

        # Topic names
        self.declare_parameter('joint_target_pos_topic', '/joint_controller/command')
        self.joint_target_pos_topic = self.get_parameter('joint_target_pos_topic').get_parameter_value().string_value
        
        self.clock = self.get_clock()
        self.start_node = self.time_to_s(self.clock.now(), 0.0)

        self.simulation = False
       
        
        
        
        self.time = 0.04 #amplitude 1.0 impulso
        self.amplitude = 1.0
        self.rate = 500
    
        self.default_dof = np.array([
            np.nan
        ]) 

        # Initialize joint publisher/subscriber
        self.njoint = 1

        self.joint_names=(
            'HIP',   # flip

        )

     
        self. i = 0
        self.start_pos = np.array([
            np.nan,     # flip
        
 
        ]) 
        self.init_pos = {self.joint_names[i]:0.0 for i in range(self.njoint)}

        self.init_torque = np.array([
            0.0,     # flip
        ]) 
        
        self.declare_parameter('joint_state_topic', '/state_broadcaster/joints_state')
        self.joint_state_topic = self.get_parameter('joint_state_topic').get_parameter_value().string_value

        # if self.simulation:
        # self.joint_state_topic = '/joint_states'
        #     self.joint_target_pos_topic = '/PD_control/command'
        #     self.joint_target_pos_pub = self.create_publisher(JointState, self.joint_target_pos_topic, 10)
        #     self.joint_sub  = self.create_subscription(JointState, self.joint_state_topic, self.joint_state_callback, 10)
        # else:
        self.joint_target_pos_pub = self.create_publisher(JointsCommand, self.joint_target_pos_topic, 10)
        self.joint_sub  = self.create_subscription(JointsStates, self.joint_state_topic, self.joint_state_callback, 10)
        
        self.default_acquired = False

        rclpy.logging.get_logger('rclpy.node').info('GetUp started, waiting for joint state_qui') 


    def getup_callback(self):
        WARMUP_ZONE = 10   
        start_pos = self.start_pos
        
        if self.i < WARMUP_ZONE:
            self.joint_pos =  self.start_pos
            self.torque = self.init_torque
        else:
            # interpolate from current to default pos
            # t = ((self.i - WARMUP_ZONE)/ (self.time * self.rate))
            self.t = self.time_to_s(self.clock.now(),self.start_node)
            
            # linear interpolation:
            # self.joint_pos = self.default_dof
            # self.torque = 2 * np.sin(self.w * t
            
            self.torque = np.array([self.amplitude])
            rclpy.logging.get_logger('rclpy.node').info(f'joint pos: {self.torque}') 


        # rclpy.logging.get_logger('rclpy.node').info(f'joint pos: {self.joint_pos}') 
        # rclpy.logging.get_logger('rclpy.node').info(f'i: {self.i}') 

        self.i += 1
        
        # SATURATE WARMPU_ZONE
        if self.i > WARMUP_ZONE +  self.time * self.rate:
            self.i = WARMUP_ZONE +  self.time * self.rate
            self.joint_pos = self.default_dof
            self.torque = self.init_torque

        joint_msg = JointsCommand()


        joint_msg.header.stamp = rclpy.clock.Clock().now().to_msg()
        joint_msg.name = self.joint_names
        joint_msg.position = (self.joint_pos).tolist()
        joint_msg.velocity = np.zeros(self.njoint).tolist()
        # joint_msg.effort = np.zeros(self.njoint).tolist()
        joint_msg.effort = (self.torque).tolist()
        # if not self.simulation:
        joint_msg.kp_scale = np.zeros(self.njoint).tolist()
        joint_msg.kd_scale = np.zeros(self.njoint).tolist()

        self.joint_target_pos_pub.publish(joint_msg)


    def joint_state_callback(self, msg):
        if self.default_acquired:
            return
        rclpy.logging.get_logger('rclpy.node').info('{}'.format((msg.position[:].tolist())))
        for i in range(self.njoint):
            self.init_pos[msg.name[i]] = msg.position[i]

        self.default_acquired = True
        rclpy.logging.get_logger('rclpy.node').info('Joints acquired, starting getup') 

        self.timer = self.create_timer(1.0 / self.rate, self.getup_callback)

    def time_to_s(self, time, start):
        [sec, ns] = time.seconds_nanoseconds()
        now = float(sec + ns/pow(10, 9))
        return (now - start)



def main(args=None):
    rclpy.init(args=args)
    impulse_test = Impulse()
    rclpy.spin(impulse_test)
    impulse_test.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()