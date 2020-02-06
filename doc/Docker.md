

# Setting up Docker on Ubuntu


This should work to setup docker on Ubuntu 18.04 and enable docker access for user `tiedeman`

```
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo usermod -a -G docker tiedeman
sudo apt-get install docker-compose
sudo systemctl restart docker
```
