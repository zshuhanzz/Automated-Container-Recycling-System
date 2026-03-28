ip_address = 'localhost' # Enter IP Address here

# SERVO TABLE CONFIGURATION
short_tower_angle = 315 # enter the value in degrees for the identification tower 
tall_tower_angle = 90 # enter the value in degrees for the classification tower
drop_tube_angle = 180 # enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# BIN CONFIGURATION
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin. 

bin1_offset = 0.20 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin1_metallic = False

bin2_offset = 0.20
bin2_color = [0,1,0]
bin2_metallic = False

bin3_offset = 0.20
bin3_color = [0,0,1]
bin3_metallic = False

bin4_offset = 0.20
bin4_color = [1,1,1]
bin4_metallic = False
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
if project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
else:
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color],[bin1_metallic,bin2_metallic, bin3_metallic,bin4_metallic]]
    configuration_information = [table_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bot = qbot(0.1,ip_address,QLabs,project_identifier,hardware)


import time
global timer
timer=1

bot.activate_line_following_sensor()
bot.activate_color_sensor()

bot_position=bot.position()
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
        arm.move_arm(0.649, 0.0, 0.281) 
        time.sleep(1) 
        arm.control_gripper(45)
        time.sleep(1)
        arm.move_arm(0.0, -0.592, 0.492)
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
            time.sleep(2)
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
            print("bin id: ", bin_id)
            print("next container mass: ", last_mass)
            print("next container id: ", last_Bin)
            print ("timer: ",timer)
            return bin_id #returns the bin location that the q-bot will go to

        

    if count == 3: #If the count is now 3, the variables reset to allow the process to repeat when the q-bot returns 
        global next_time
        next_time = 0
        total_weight = 0
        print("bin id: ", bin_id)
        print ("timer: ",timer)
        return bin_id #returns the bin location that the q-bot will go to


def transfer_container(binid):
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
    rota=0
    t=0
    while a:
        left=bot.line_following_sensors()[0]
        right=bot.line_following_sensors()[1]

        if left==1 and right==1:
            bot.set_wheel_speed([0.1, 0.1])
        elif left<1 and right==1:
            bot.set_wheel_speed([0.1, 0.04])
        elif left==1 and right<1:
            bot.set_wheel_speed([0.04, 0.1])
        else:
            if rota==1:
                bot.rotate(2)
            elif rota==2:
                bot.rotate(-2)

        c=bot.read_color_sensor()[0]


        bot.forward_time(0.05)
        if left<1 and right==1:
            rota=1
        elif left==1 and right<1:
            rota=2

        if c== required_bin:
            t+=0.05
            if t>=0.2:
                bot.forward_distance(0.12)
                a=False
                print("correct bin found")


#Deposit container: 
def deposit_container(binid):
    bot.stop()
    time.sleep(1)
    bot.activate_linear_actuator()
    if binid=="Bin01" or binid=="Bin02":
        bot.rotate_hopper(70)
    elif binid=="Bin03" or binid=="Bin04":
        bot.rotate_hopper(60)
    time.sleep(2)
    bot.rotate_hopper(0)
    bot.deactivate_linear_actuator()


def return_home():
    rota=0
    
    p = bot.position()

    while p != bot_position:
    
        left=bot.line_following_sensors()[0]
        right=bot.line_following_sensors()[1]
        p = bot.position()


        if left==1 and right==1:
            bot.set_wheel_speed([0.1, 0.1])
        elif left<1 and right==1:
            bot.set_wheel_speed([0.1, 0.04])
        elif left==1 and right<1:
            bot.set_wheel_speed([0.04, 0.1])
        else:
            if rota==1:
                bot.rotate(4)
            elif rota==2:
                bot.rotate(-4)

        if ((bot_position[0]+0.05) > p[0] >(bot_position[0]-0.05) ) and ((bot_position[1]+0.05)> p[1]>(bot_position[1]-0.05) and ((bot_position[2]+0.05)> p[2] >(bot_position[2]-0.05) ) :

            bot.stop()
            bot.rotate(-5)
            print ("Cycle complete")
            
            break

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


bot.deactivate_line_following_sensor()
bot.deactivate_color_sensor()


    

    

