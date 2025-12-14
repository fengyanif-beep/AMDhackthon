#!/usr/bin/env python3
"""
Project Fox - Inference Script
AMD Robotics Hackathon 2025

This script loads a trained ACT policy and runs autonomous 
robot control on the SO101 follower arm.
"""

import sys
sys.path.insert(0, "/home/feng/lerobot/src")

import torch
import numpy as np
from lerobot.policies.act.modeling_act import ACTPolicy
from lerobot.robots.so101_follower import SO101Follower
from lerobot.robots.so101_follower.config_so101_follower import SO101FollowerConfig
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
import time

# Configuration
POLICY_PATH = "/home/feng/outputs/act_model/checkpoints/001500/pretrained_model"
# Or use Hugging Face: POLICY_PATH = "Foxc11/act-so101-model"

def main():
    print("=" * 50)
    print("Project Fox - Autonomous Robot Control")
    print("=" * 50)
    
    # Load trained policy
    print("\n[1/3] Loading ACT policy...")
    policy = ACTPolicy.from_pretrained(POLICY_PATH)
    policy.eval()
    print("Policy loaded successfully!")
    
    # Setup cameras
    print("\n[2/3] Setting up cameras...")
    config_top = OpenCVCameraConfig(index_or_path=4, fps=30, width=640, height=480)
    config_side = OpenCVCameraConfig(index_or_path=2, fps=30, width=640, height=480)
    
    # Connect robot
    print("\n[3/3] Connecting robot...")
    robot_config = SO101FollowerConfig(
        port="/dev/ttyACM1",
        cameras={"top": config_top, "side": config_side}
    )
    robot = SO101Follower(robot_config)
    robot.connect()
    print("Robot connected!")
    
    print("\n" + "=" * 50)
    print("Starting autonomous control...")
    print("Press Ctrl+C to stop")
    print("=" * 50 + "\n")
    
    try:
        step = 0
        max_steps = 300  # 10 seconds at 30 fps
        
        while step < max_steps:
            # Get observation from robot
            obs_dict = robot.get_observation()
            
            # Extract joint states
            joint_keys = ['shoulder_pan.pos', 'shoulder_lift.pos', 'elbow_flex.pos', 
                         'wrist_flex.pos', 'wrist_roll.pos', 'gripper.pos']
            state = np.array([obs_dict[k] for k in joint_keys], dtype=np.float32)
            
            # Format observation for policy
            obs = {
                "observation.images.top": torch.from_numpy(obs_dict['top']).permute(2,0,1).unsqueeze(0).float() / 255.0,
                "observation.images.side": torch.from_numpy(obs_dict['side']).permute(2,0,1).unsqueeze(0).float() / 255.0,
                "observation.state": torch.from_numpy(state).unsqueeze(0)
            }
            
            # Get action from policy
            with torch.no_grad():
                action = policy.select_action(obs)
            
            # Send action to robot
            action_array = action[0].cpu().numpy()
            action_dict = {
                joint_keys[i]: float(action_array[i]) 
                for i in range(len(joint_keys))
            }
            robot.send_action(action_dict)
            
            # Progress update
            step += 1
            if step % 30 == 0:
                print(f"Step {step}/{max_steps} - Robot executing autonomously...")
            
            time.sleep(0.033)  # 30 Hz control loop
            
    except KeyboardInterrupt:
        print("\n\nUser stopped execution.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        robot.disconnect()
        print("\nRobot disconnected. Done!")

if __name__ == "__main__":
    main()

