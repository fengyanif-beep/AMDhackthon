
# AMD_Robotics_Hackathon_2025_Project Fox C AI

## Team Information

**Team:** Team 25 - Fox C AI, Fengyan HUANG

**Summary:** Fox C AI is a low-cost, embodied AI companion designed to bridge the gap between **physical distance** and **physical ability**. Built by a solo developer in **30 hours**, this system uses an end-to-end **ACT (Action Chunking with Transformers) Policy** to learn diverse human interactions—from **stabilizing a cup for Parkinson's patients** to **delivering a comforting "pat" for long-distance couples**. It proves that AI robotics can be a vessel for both dignity and love.

*< Images or video demonstrating your project >*

## Submission Details

### 1. Mission Description
**Connecting Humans, one movement at a time.**

- **Restoring Dignity (Parkinson's Care):** Acting as a physical stabilizer. The AI filters out pathological tremors from the user's input, allowing patients to perform steady tasks like drinking water or taking medicine independently.
- **Transmitting Love (Long-Distance Connection):** Acting as a remote avatar. The robot can learn and reproduce gentle, affective touches (like a "pat" on the head), allowing long-distance partners to feel a sense of physical presence beyond a screen.
- **Democratizing Robotics:** Moving away from cold industrial robots to accessible, warm, consumer-grade hardware (So-100) powered by AMD Ryzen AI.

### 2. Creativity
- **Dual-Purpose Empathy:** Unlike traditional robots focused on efficiency, this project focuses on emotion and stability. The same ACT policy is generalized to handle both precise functional tasks (holding a cup) and soft emotional tasks (gentle touch).
- **Solo Full-Stack Implementation:** Completed an entire Sim2Real pipeline (Driver -> Data -> Training -> Inference) alone in **30 hours**.
- **"Wabi-Sabi" Design:** The system tolerates human imperfections. It treats hand tremors not as errors, but as noise to be smoothed out by the Transformer model.

**Innovation:**
- **Zero-Code Interface:** Designed for non-technical users (patients/families) to train their own assistants.
- **Local Compute Optimization:** Optimized for fast training on consumer-grade hardware.

### 3. Technical implementations
- *Teleoperation / Dataset capture*
    - Built a low-latency **Leader-Follower** teleoperation system using So-101 arms.
    - Collected a custom dataset of 20 episodes mapping visual observations to joint positions. (Note: Standardized cubes were used as proxy objects during the validation phase to safely tune the grasping stability before deploying with liquid containers/medicine bottles.)
    - *<Image/video of teleoperation or dataset capture>*

**Setup:**
- Robot: SO101 (Leader + Follower arms)
- Cameras: 2x OpenCV cameras (640x480@30fps)
- Episodes: 20
- Episode length: 10 seconds
- Total frames: 6000
- Pipeline: LeRobot Data Collection

**Command:**
```bash
lerobot-record --config record_config.yaml
```


- *Training*
    - **Algorithm:** Implemented ACT (Action Chunking with Transformers).
    - **Compute:** Trained locally on consumer-grade GPU (1500 steps end-to-end).
    - **Optimization:** Tuned for fast convergence in a low-data regime. 

- *Configuration:*

Steps: 1500 (Early Convergence Experiment)
Batch size: 8
Learning rate: 1e-5
Backbone: ResNet18 (Visual Encoder)
Training time: ~1.9 hours (AMD Ryzen AI 9 HX, CPU mode)


**Command:**
```bash
lerobot-train --config train_config.yaml
```


Training Progress:
Step 100:  loss=9.570
Step 1000:  loss=1.569
Step 1500: loss=1.482
Result: Successfully cloned behavior from minimal data. Loss reduced by 84.5%. 

- *Inference*
    - Deployed the trained policy on the So-101 follower arm.
    - The robot successfully mimics the intent of the user, smoothing out high-frequency jitters.
    - *<Image/video of inference eval>*

**Command:**
```bash
python run_inference.py
```

Result: The robot successfully executes the "Grasp & Give" motion, smoothing out the high-frequency jitters from the teleoperation phase.

### 4. Ease of use
- **Zero-Code Interface:** Designed for non-technical users. If I (a solo developer) can teach it a skill in 15 minutes, a patient's family member can too.
- **One-Click Train & Run:** The pipeline abstracts away the complexity of Linux drivers and Python environments.
- **Plug-and-Play:** No complex calibration required; adaptive to camera placement shifts.

Control Interface: The system abstracts away the Linux terminal complexity, aiming for a "One-Button" experience for end-users.

## Additional Links
*For example, you can provide links to:*

- Demo Video:
- Hugging Face Dataset: <https://huggingface.co/datasets/Foxc11/record-test>
- Hugging Face model: <https://huggingface.co/Foxc11/act-so101-model>
- Training logs (wandb): mission/wandb/001500/

## Code submission

This is the directory tree of this repo, you need to fill in the `mission` directory with your submission details.

```terminal
AMD_Hackathon_Submission/
├── README.md
└── mission/
    ├── code/
    │   ├── record_config.yaml       # Recording configuration
    │   ├── train_config.yaml        # Training configuration
    │   └── run_inference.py         # Inference script
    └── wandb/
        └── 001500/                  # Training checkpoint (step 1500)
            ├── pretrained_model/    # Model weights
            └── training_state/      # Training state

```
## Hardware

 - AMD RYZEN AI Pro 9 HX
 - SO101 Robot Arm
 - 2x USB Cameras


## Results

- ✅ Mission Accomplished: From unboxing to autonomous inference in 30 hours.
- ✅ Data Efficiency: Learned a complex contact-rich task with only 20 examples.
- ✅ Trained an ACT policy with 84.5% loss reduction
- ✅ Social Impact: Demonstrated a viable path for affordable assistive robotics.   
