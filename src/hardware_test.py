ip_address = '172.17.42.73' # Enter your IP Address here


import sys
sys.path.append('../')
from Common.hardware_project_library import *

hardware = True
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
if project_identifier == 'P3A':
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    table = servo_table(ip_address,QLabs,None,hardware)
else:
    speed = 0.1 # in m/s
    bot = qbot(speed,ip_address,QLabs,project_identifier,hardware)

#begin


import time
global timer
timer = 1

#activates the sensors
bot.activate_line_following_sensor()
bot.activate_color_sensor()

#assigns the bots initial position to a variable
bot_position = bot.position()
print (bot_position)


#dispense container: Takes input of container number, dispenses the container, prints and returns the containers properties
def dispense_container(container):  

    properties = table.dispense_container(container,True)
    material = properties[0]
    container_mass = properties[1]
    BIN = properties[2]

    print (properties)

    return properties 
    


#Load container: Dispenses a container using dispense_container function, assigns variables to the different container properties, using q-arm picks up container and loads it onto q-bot, reapeats the cycle if proper conditions are met
def load_container(timer):

    global last_mass 
    global last_Bin
    global next_time


    if timer == 1:
        count = 0
    else:
        count = 4
    
    if count == 0:

        m_p = dispense_container(random.randint(1,6))
        material = m_p[0]
        container_mass = m_p[1]
        BIN = m_p[2]

        #Moves arm to pickup location, picks up container, brings it to the position for first bottle, drops container, arm returns home
        arm.move_arm(0.652, 0.0, 0.278) 
        time.sleep(1) 
        arm.control_gripper(45)
        time.sleep(1)
        arm.move_arm(0.0, -0.600, 0.492)
        time.sleep(2) 
        arm.control_gripper(-45)
        time.sleep(2)
        arm.home() 

        bin_id = BIN  #Assigns the bin location of first container to the bin_id variable
        count += 1 #Increases count to keep track of bottles on q-bot
        total_weight = container_mass #Adds the mass of first container to the total weight


    time.sleep(2)

    if count == 4:
        mass = last_mass

        #Moves arm to pickup location, picks up container, brings it to the position for first bottle, drops container, arm returns home
        arm.move_arm(0.652, 0.0, 0.278) 
        time.sleep(1) 
        arm.control_gripper(45)
        time.sleep(1)
        arm.move_arm(0.0, -0.592, 0.492)
        time.sleep(2) 
        arm.control_gripper(-45)
        time.sleep(2)
        arm.home() 

        bin_id = last_Bin  #Assigns the bin location of first container to the bin_id variable
        total_weight = mass #Adds the mass of first container to the total weight

        count = 1
        time.sleep(2)

    if count == 1:  #Next step occurs if one bottle is already in the q-bot
    #Dispenses a container, assigns variables to the different container properties
        m_p1 = dispense_container(random.randint(1,6))
        material = m_p1[0]
        container_mass = m_p1[1]
        Bin = m_p1[2]

        time.sleep(2)

        if Bin == bin_id and total_weight < 90: #Checks if the bin location of second container matches the location the q-bot is going to
            arm.move_arm(0.652, 0.0, 0.278) 
            time.sleep(1) 
            arm.control_gripper(45)
            time.sleep(1)
            arm.move_arm(0.018, -0.514, 0.550)
            time.sleep(2) 
            arm.control_gripper(-45)
            time.sleep(2)
            arm.home()
            
            count += 1
            total_weight = total_weight + container_mass 


        else: #If the bin location does not match the bin location of the q-bot then the servo table rotates and increases count
            last_mass = container_mass 
            last_Bin = Bin
            next_time = 1
            print("bin id: ", bin_id)
            print("next container mass: ", last_mass)
            print("next container id: ", last_Bin)
            print ("timer: ",timer)
            return bin_id #returns the bin location that the q-bot will go to  

    time.sleep(2)

    if count == 2: #Next step occurs if 2 bottles are in the q-bot

        m_p2 = dispense_container(random.randint(1,6))
        material = m_p2[0]
        container_mass = m_p2[1]
        BIn = m_p2[2]

        time.sleep(2)

        if BIn == bin_id and total_weight < 90: #Checks if the bin location of the container matches the location the q-bot is going to
            arm.move_arm(0.652, 0.0, 0.278) 
            time.sleep(1) 
            arm.control_gripper(45)
            time.sleep(1)
            arm.move_arm(0.016, -0.453, 0.525)
            time.sleep(2) 
            arm.control_gripper(-45)
            time.sleep(2)
            arm.home()

            count += 1
            total_weight = total_weight + container_mass

        else: #If the bin location does not match the bin location of the q-bot then the servo table rotates and increases count
            last_mass = container_mass 
            last_Bin = BIn
            next_time = 1
            print("bin id: ", bin_id)
            print("next container mass: ", last_mass)
            print("next container id: ", last_Bin)
            print ("timer: ",timer)
            return bin_id #returns the bin location that the q-bot will go to

        

    if count == 3: #If the count is now 3, the variables reset to allow the process to repeat when the q-bot returns 
        next_time = 0
        total_weight = 0
        print("bin id: ", bin_id)
        print ("timer: ",timer)
        return bin_id #returns the bin location that the q-bot will go to

    
        
#the function to transfer containers to the bins  
def transfer_container(binid):

    #checks for the required bin and assigns a color to it
    required_bin = [0, 0, 0]
    if binid=="Bin01":
        required_bin= [1, 0, 0]
    elif binid=="Bin02":
        required_bin= [0, 1, 0]
    elif binid=="Bin03":
        required_bin= [0, 0, 1]
    elif binid=="Bin04":
        required_bin= [1, 1, 1]
        
    a = True
    #helps rotate the bot based on the previous 
    rota=0
    t=0
    while a:
        #reads the line following sensors
        left=bot.line_following_sensors()[0]
        right=bot.line_following_sensors()[1]

        #if left and right both read the line set both wheels same speed
        if left==1 and right==1:
            bot.set_wheel_speed([0.1, 0.1])
        #if only the right sensor reads the line, set right wheel speed higher than the left
        elif left<1 and right==1:
            rota=1
            bot.set_wheel_speed([0.1, 0.04])
        #if only the left sensor reads the line, set left wheel speed higher than the right
        elif left==1 and right<1:
            rota=2
            bot.set_wheel_speed([0.04, 0.1])
        #if the line is not read at all, rotate the bot
        else:
            if rota==1:
                bot.rotate(2)
            elif rota==2:
                bot.rotate(-2)
        #reads the color sensor
        c=bot.read_color_sensor()[0]

        #moves the bot forward

        #checks to see if the bot has reache the required bin
        if c== required_bin:
            t+=0.05
            #code differs based on the bins locations due to bin 1 and 3 existing immediately after a turn
            if t>=0.1 and (binid=="Bin02" or binid=="Bin04"):
                bot.forward_distance(0.15)
                a=False

            if t>=0.3 and (binid=="Bin01" or binid=="Bin03"):
                bot.forward_distance(0.05)
                a=False

#the function to dump the containers into the bin using an actuator
def deposit_container(binid):
    print("correct bin found")
    #stops the bot's movement
    bot.stop()
    time.sleep(1)
    #activates the bots linear actuator to dump the containers in the bin
    bot.activate_linear_actuator()

    #moves the actuator incrementally to ensure all the containers are dumped properly
    bot.rotate_hopper(30)
    time.sleep(1)
    bot.rotate_hopper(50)
    time.sleep(1)
    bot.rotate_hopper(90)
    time.sleep(2)
    #returns the actuator's rotation back to 0
    bot.rotate_hopper(0)
    bot.deactivate_linear_actuator()

#the function to return the q bot to the original position
def return_home():
    #checks to see which way to rotate 
    rota=0
    
    p = bot.position()

    #checks if the bot has returned 
    while p != bot_position:

        #checks for line sensor readings
        left=bot.line_following_sensors()[0]
        right=bot.line_following_sensors()[1]
        p = bot.position()


        #same movement code as transfer_container function
        if left==1 and right==1:
            bot.set_wheel_speed([0.1, 0.1])
        elif left<1 and right==1:
            bot.set_wheel_speed([0.1, 0.04])
        elif left==1 and right<1:
            bot.set_wheel_speed([0.04, 0.1])
        #rotates the bot if lines are not found
        else:
            if rota==1:
                bot.rotate(4)
            elif rota==2:
                bot.rotate(-4)
        #checks if the bot has returned to the original position with a margin of error
        if ((bot_position[0]+0.05) > p[0] >(bot_position[0]-0.05) ) and ((bot_position[1]+0.05)> p[1]>(bot_position[1]-0.05))  and ((bot_position[2]+0.05)> p[2] >(bot_position[2]-0.05) ) :

            #forwards the bot slightly to ensure original position
            bot.forward_distance(0.04)
            bot.stop()
            #rotates the bot slightly to ensure original orientation
            bot.rotate(-5)
            print ("Cycle complete")
            #breaks the movement while loop
            break
    #moves the bot forward at the end of each iteration
    bot.forward_time(0.05)

    
while True:
    binid=0  
    binid=load_container(timer)
    transfer_container(binid)
    deposit_container(binid)
    print ("Returning home")
    return_home()
    if next_time == 0:
        timer = 1
    else:
        timer += 1
    print (timer)
    time.sleep(2)

#After running the program, deactivate all the sensors
bot.deactivate_line_following_sensor()
bot.deactivate_color_sensor()

    

