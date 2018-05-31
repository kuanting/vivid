# VIVID - Virtual Environment for Visual Deep Learning

VIVID (VIrtual environment for VIsual Deep learning) is a photo-realistic simulator that aims to facilitate deep learning for computer vision. 
VIVID supports four different characters: robot (mannequin), simple drone, AirSim drone and automobile. Twelve large, diversified indoor and outdoor scenes are included. 
In addition, we create NPC with simulated human actions to mimic real world events, such as gun shooting and forest fire rescue. 
VIVID is based on [Unreal Engine](https://www.unrealengine.com) and [Microsoft AirSim](https://github.com/Microsoft/AirSim).
Documentation and tutorials can be found in our [WiKi page](https://github.com/kuanting/vivid/wiki). 

![Samba dance](/images/zoe_sambe_dance.gif)|![Fly in a ruined school](/images/drone_fly_in_ruin.gif)
:-----------------------------------------:|:-------------------------------------------------------:
![Forest fire](/images/robot_run_in_forest_fire.gif)|![Gun shooting detection](/images/drone_in_gun_shooting.gif)

## Architecture
The architecture of VIVID is shown below. Our system is powered by Unreal and leverages AirSim plugin for hardware simulation and control. 
The remote procedure call (RPC) is used to communicate with external programming languages. Currently VIVID supports four different characters: robot, simple drone, AirSim drone and automobile.
User can select characters and scenes by using in-game menu.

![](/images/vivid_arch.png)

## Documentation
The documents and tutorials are in our [GitHub WiKi](https://github.com/kuanting/vivid/wiki).


## Human Actions
Some examples of human actions in VIVID. The actions from left to right are shooting, dying, jumping, walking, surrendering, moaning in pain, running, police running with rifle, crouching and dancing.
Most action models can be downloaded from [Maximo](https://www.mixamo.com).
![Human Action Examples](/images/action_examples.png)


## Download Source Code
The source code and UE4 project file can be downloaded from source folder [/source](/source). Note that you need to install UE4 editor first. We only support Windows now. Linux version is coming soon. 


## Download Binaries
The pre-compiled binary files can be downloaded here:

- [Windows](https://drive.google.com/open?id=18EMYzQpfd-VRArLR0OVhL_2SSWgLGNrS)


## Python Controls
See examples in [/python_client](/python_client)
