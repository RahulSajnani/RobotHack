# LeRobot Hackathon 2025

Team members: Gauri Gandhi, Rahul Sajnani, Rohan Chacko, Gaurav Chaudhary

Problem statement: Autonomously remove debris from manholes on roads. 

## Tasks trained for 
1. Opening the manhole cover
2. Removing debris
3. Closing the manhole cover

## Model training
The model was trained on top of ![SmolVLA](https://huggingface.co/blog/smolvla) using the ACT policy.

### Model checkpoints (on Huggingface)
* Picking manhole lid: shubhgaurav10/act\_so101\_only\_pick\_lid\_single
* Picking debris from hole: shubhgaurav10/act\_so101\_remove\_debris

## Datasets
* ![Picking manhole lid](https://huggingface.co/datasets/rohanc007/record-only-pick-lid-single): Records a pick action by the robot arm. Number of episodes: 30.
* ![Picking debris from hole](https://huggingface.co/datasets/rohanc007/record-remove-debris): Records picking debris and placing on the side by the robot arm. Number of episodes: 30.

You can visualize the datasets on - ![LeRobot Dataset Visualizer](https://huggingface.co/spaces/lerobot/visualize_dataset)

#### Notes
* ACT training worked better than the SmolVLA policy.
* 30 episodes for a simple task without very minimal domain randomization trained using ACT seemed to work the best. 
* Finetuning the pi0 model might yield better results.
