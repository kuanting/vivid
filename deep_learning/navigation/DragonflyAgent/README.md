# Dragonfly Agent

## Environment Settings

### Client Side (tested on Ubuntu 17.04)

1. Clone this repository

2. Install the following packages:
    * python 3.6
    * pytorch 0.3.0
    * numpy 1.14.0
    * scipy 1.0.0
    * gym 0.9.4
    * msgpack-rpc-python 0.4
    * tensorboardX 0.8
    * pillow 5.0.0
    * imageio 2.2.0
    * tensorflow-tensorboard 0.1.6 (Optional)

3. Download `pspnet50_ADE20K.pth`
[here](https://drive.google.com/open?id=1lB-ABBLghNvhrZQ2ziAjypmRaMD-oFHw)
and store in `pspnet/models/` directory.

### Server Side (tested on Windows 10)

1. Download Dragonfly simulator
[here](https://drive.google.com/open?id=1idzBbvPZXj-lQab8H29p00hGiYootIet)
and unzip it.
This folder should contains a `FlyingTest.exe` executable.

2. Download `launch.bat`
[here](https://drive.google.com/open?id=1E0Ddf_Rho-qGiBffVmEPV_r80gErLXPa)
and put it in the same folder as `FlyingTest.exe`

## Training

1. On Windows machine, click `launch.bat` and specify the number of environments.
This script will automatically start multiple simulators on consecutive ports
starting from 16660.
For example, to train A3C on 4 agents, you need to start 5 simulators
(one for testing).

2. Make sure you have created the following directories:
    ```shell
    cd $DragonflyAgent_ROOT
    mkdir checkpoints # for a3c model checkpoint
    mkdir runs # for tensorboard log
    ```

3. In `settings.json`, change the ip address to point to your Windows machine.

4. Run the training scripts:
    ```shell
    python main.py --num-process <number of training agent> 
    ```

5. (Optional) Start tensorboard to watch the training progress:
    ```shell
    tensorboard --logdir runs
    ```

## Testing

1. Download `best.pth`
[here](https://drive.google.com/open?id=1TSENceE5d_tVDXunMctU5bRp3ytJiWpF).
You can also use your own checkpoints.

2. Run the testing scripts:
    ```shell
    python testing.py <path to model checkpoint>
    ```
   Results will be saved in `original.gif` and `segmented.gif`.

## References

* Dragonfly simulator: https://github.com/kuanting/dragonfly
* PSPNet pytorch implementation: https://github.com/kazuto1011/pspnet-pytorch
* A3C pytorch implementation: https://github.com/ikostrikov/pytorch-a3c
