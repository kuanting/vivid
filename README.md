# VIVID - Virtual Environment for Visual Deep Learning

VIVID (VIrtual environment for VIsual Deep learning) is a photo-realistic simulator that aims to facilitate deep learning for computer vision. 
VIVID supports four different characters: robot (mannequin), simple drone, AirSim drone and automobile. Twelve large, diversified indoor and outdoor scenes are included. 
In addition, we create NPC with simulated human actions to mimic real world events, such as gun shooting and forest fire rescue. 
VIVID is based on [Unreal Engine](https://www.unrealengine.com) and [Microsoft AirSim](https://github.com/Microsoft/AirSim).
Since 2018, we have developed many interesting simulation environments for traffic and drone simulation. More information can be found on AIoT Lab's website [www.aiotlab.org](https://www.aiotlab.org).

<a href="https://www.youtube.com/watch?v=7ScHTpC2gQg"><img src="http://img.youtube.com/vi/7ScHTpC2gQg/0.jpg"/></a> | <a href="https://www.youtube.com/watch?v=K3xT1oNaNSI"><img src="http://img.youtube.com/vi/K3xT1oNaNSI/0.jpg"/></a>
:-----------------------------------------:|:-------------------------------------------------------:
<a href="https://www.youtube.com/watch?v=u0avZv6DCbw"><img src="http://img.youtube.com/vi/u0avZv6DCbw/0.jpg"/></a> | <a href="https://www.youtube.com/watch?v=8Yk7ITc3amo"><img src="http://img.youtube.com/vi/8Yk7ITc3amo/0.jpg"/></a>

## Download Simulation Games
We have developed 3 drone related games: Drone Resue, Drone vs Tank, Human vs Drone.
The games can be downloaded via the link below:
- [AIoTLab Drone Games](https://onedrive.live.com/?redeem=aHR0cHM6Ly8xZHJ2Lm1zL2YvcyFBaS1VdFhaNWc4OGxtTzFkWW93ZFRSR0lsTEx3RlE%5FZT16RGlzNEo&id=25CF837976B5942F%21407261&cid=25CF837976B5942F).


## Citations

If you like our work, please cite the papers below:
```
@inproceedings{lai2018vivid,
  title={Vivid: Virtual environment for visual deep learning},
  author={Lai, Kuan-Ting and Lin, Chia-Chih and Kang, Chun-Yao and Liao, Mei-Enn and Chen, Ming-Syan},
  booktitle={Proceedings of the 26th ACM international conference on Multimedia},
  pages={1356--1359},
  year={2018}
}
```
```
@inproceedings{lin2023traffic,
  title={Traffic Object Detection in Virtual Environments},
  author={Lin, Bo-Yi and Huang, Chih-Sheng and Lin, Jia-Ming and Liu, Pin-Hsuan and Lai, Kuan-Ting},
  booktitle={2023 International Conference on Consumer Electronics-Taiwan (ICCE-Taiwan)},
  pages={245--246},
  year={2023},
  organization={IEEE}
}
```
```
@INPROCEEDINGS{10227067,
  title={Augmented Reality for Real Object Detection}, 
  author={You, Wei-Xuan and Huang, Chih-Sheng and Hu, Kai-Ming and Liu, Tzu-Hsin and Lai, Kuan-Ting},
  booktitle={2023 International Conference on Consumer Electronics - Taiwan (ICCE-Taiwan)}, 
  year={2023},
  pages={803-804},
  organization={IEEE},
```


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
