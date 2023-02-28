#!/usr/bin/env python
import rospy
import numpy as np
from pid_test.msg import motor_output
from pid_test.msg import motor_input
from pid_test.msg import set_point_msg
from std_msgs.msg import Float32


#Setup parameters, variables and callback functions here (if required)
Kp=1.0
Ki=2.0
Kd=3.0
setpoint_data=0
outcome_data=0
out=0.0
ti=0.0
stat=" "
global last_time
last_time=0




Input=set_point_msg()
Input.setpoint_1=0.0
Input.option_1=" "

RES=motor_output()
RES.output=out
RES.time=ti
RES.status=stat


def set_point_callback(msg):
   global Input
   Input=msg
   rospy.loginfo("opt: %s set: %f",Input.option_1, Input.setpoint_1 )
   

def motor_output_callback(msg):
   global RES
   RES=msg
   rospy.loginfo("out1: %f", RES.output)
   rospy.loginfo("time: %f", RES.time)
   rospy.loginfo("time: %s", RES.status)
   rospy.loginfo("set: %f", Input.setpoint_1)
   
   last_error=0.0
   integral=0.0
   #calculate the error
   error=Input.setpoint_1-RES.output

   current_time=rospy.get_time()
   l_time=RES.time
   last_time=l_time+current_time
   dt=last_time-current_time
   rospy.loginfo("LastTime: %f", current_time)
   rospy.loginfo("Currtime: %f", last_time)
   integral+=error*dt
   derivative=(error-last_error)/dt

   output=Kp*error+Ki*integral+Kd*derivative

   input_msg=motor_input()
   input_msg.input=output
   input_msg.time=current_time
   rospy.loginfo(input_msg)
   motor_input_pub.publish(input_msg)
   rospy.loginfo("dt: %f", dt)
   rospy.loginfo("Out: %f", output)
   rospy.loginfo("Error: %f", error)
   rospy.loginfo("Integral: %f", integral)
   rospy.loginfo("Derivative: %f", derivative)


   last_error=error
   last_time=current_time
   rospy.loginfo("LAASTError: %f", last_error)
   rospy.loginfo("LASTtime: %f", last_time)



#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("controller")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)

    #Setup Publishers and subscribers here
    #control_pub=rospy.Publisher("")
    #error_pub=rospy.Publisher("")
    rospy.Subscriber("/setpoint_",set_point_msg,set_point_callback)
    rospy.Subscriber("/motor_output",motor_output, motor_output_callback)
    motor_input_pub=rospy.Publisher("/motor_input", motor_input,queue_size=10)
    start_time=rospy.get_time()
    #setpoint=1.0


    print("The Controller is Running")
    #Run the node
    while not rospy.is_shutdown():

        #Write your code here

        rate.sleep()