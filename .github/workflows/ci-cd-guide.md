
# CI/CD Guide

<img width="1068" height="381" alt="Image" src="https://github.com/user-attachments/assets/5829ac5e-1258-4e99-8c96-b36d1bf997e5" />

The project provides two self-hosted runners to deploy the app:
- @kingazm's Raspberry Pi 4B
- the Raspberry Pi 5 we've been given for the time of the course

This guide lets anyone reproduce the set up for a Raspberry Pi device.

## Prerequisites
Have a Raspberry Pi with an operating system installed and an internet access available.
Make sure the Raspberry Pi is connected to a power source.
To follow the next steps on your Raspberry Pi, you need to either 
- have a keyboard, monitor and a mouse connected to it,
- `ssh` into the device from your computer, using `ssh <username_of_the_raspberry_pi>@<ip address>` (ensure your device allows ssh and you have adequate credentials)

## Create the self-hosted runner

1. Go to `Actions` section in the repository
<img width="626" height="114" alt="image" src="https://github.com/user-attachments/assets/9ea240e5-b7c0-45d4-a2e3-cf51115bdfec" />
<br>
<br>

2. Go to `Runners`

3. Create a new runner

Follow the steps indicated by GitHub. Make sure to choose `Linux` as an operating system and `ARM64` as architecture, to guarantee compatilibilty with this CI/CD and the devices types it was tested on.


## Install Docker on the Raspberry Pi
Follow the [official instructions](https://docs.docker.com/engine/install/raspberry-pi-os/)

Ensure your user has adequate permissions by running
```bash
sudo usermod -aG docker $USER
```

Reboot to make sure the changes propagate.
```bash
sudo reboot
```

## Trigger the CI/CD workflow 
Do it for the first time by making changes to the repository, or re-running previous runs.

Make sure the runner is indeed running (the Raspberry Pi is plugged in and run `./run.sh` from the directory where you have your runner configured (typically `actions-runner`). 
Do not abort the process until deployment is completed.

GitHub Actions section will show you the progress of the workflow.

Use ```docker ps``` and browser on the indicated ports on your Raspberry Pi to verify the successfull deployment.

## Troubleshooting

```bash
 Failed to create a session. The runner registration has been deleted from the server, please re-configure.
```

Important note: once not used for 14 days, self-hosted runners require re-configuring, as GitHub removes unused runners to save resources. 
To re-configure the runner, simply follow the `./config.sh (...)` part of the **setting up self-hosted runner** section.

```bash
Run cd docker
unable to get image 'ros:rolling': permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.51/images/ros:rolling/json": dial unix /var/run/docker.sock: connect: permission denied
```

Ensure you followed the granting permissions step of the docker set up on your Raspberry Pi, and that you did the reboot after before trying to use the runner.

```bash
System.IO.IOException: No space left on device : ...
```

Check whether you have space left on your device. Make sure the logs and diagnostics are cleaned up, and if you delete and re-install your runner, make sure you follow steps indicated by GitHub when clicking `delete runner` in your runners section (use `./config.sh` to clean up properly)
In case none of the above helps, reformat the SD card and install Raspberry Pi operating system once more, and follow the steps from the top.


```bash
The job has exceeded the maximum execution time while awaiting a runner for 24h0m0s
```

This message indicated that your runner is not running. Access it and check whether the `./run.sh` is running. If not, simply run `./run.sh` from the directory where you have your runner configured (typically `actions-runner`)
