# Automated Container Recycling System

## Overview
This project is a real time recycling system that detects, classifies, and sorts containers using sensor data. It was built in Quanser and tested on a physical QBot to compare simulation vs real world performance.

## Features
- Real-time object detection and classification  
- Sensor fusion using IR and ultrasonic sensors  
- Autonomous bin sorting decisions  
- SIL (simulation) and HIL (hardware) testing  
- Python control logic for handling sensor data  

## How It Works
1. Sensors collect data about the object/bin
2. The system combines the data to figure out position and type  
3. A sorting decision is made  
4. The robot moves to the correct bin  

## Results
- ~88% accuracy in simulation  
- ~80% accuracy on hardware  
- <10% performance gap between simulation and real system  

## Challenges
- Messy sensor data  
- Lots of small timing and movement issues and refinements
- Matching simulation behavior to real hardware  
