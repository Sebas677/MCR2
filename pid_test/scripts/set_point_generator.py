#!/usr/bin/env python
import rospy
import numpy as np
from pid_test.msg import set_point_msg
from std_msgs.msg import Float32

# Setup Variables, parameters and messages to be used (if required)

#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
 print("Stopping")


if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("Set_Point_Generator")

    #rospy.on_shutdown(stop)

    #Setup Publishers and subscribers here
    signal_pub=rospy.Publisher("signal",Float32, queue_size=10)
    #time_pub=rospy.Publisher("time",Float32, queue_size=10)
    setpoint_pub=rospy.Publisher("/setpoint_",set_point_msg,queue_size=10)
    rate = rospy.Rate(10)

    msg=set_point_msg()

    #Run the node
    while not rospy.is_shutdown():

      #Write your code here
      i=rospy.get_time() 
      no_opt = rospy.get_param("/no_case",0.0)
      set_p=rospy.get_param("/setpoint",3.0)
      opt_wave=rospy.get_param("/option", "sine")


      rospy.loginfo("The option %s at a setpoint of %f",opt_wave, set_p)

   
      if opt_wave=='sine':
         y=set_p*np.sin(np.pi*i)
         print("sine")
      elif opt_wave=='square':
         y=set_p
         print("square")
      else:
         y=no_opt
         print("receive %f", 1.0)
      
      rospy.loginfo(y)
      #rospy.loginfo(i)
      msg.setpoint_1 = set_p
      msg.option_1 = opt_wave
      
      signal_pub.publish(y)
      setpoint_pub.publish(msg)
      rospy.loginfo("The option_-_-_-_ %s at a setpoint of %f",msg.option_1, msg.setpoint_1)
      #time_pub.publish(i)
      rate.sleep()


