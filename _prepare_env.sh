mkdir /tmp/podman
mkdir /tmp/podman/test
mkdir /tmp/podman/test/src
mkdir /tmp/csv_data/

cp ./game_files/* /tmp/podman/test/src

# 拉取minecraft的容器
sudo podman pull platpus/javafx

# build snake的容器
sudo podman pull zzdflyz351/snake-edge
# cd snake_build_image
# sudo bash ./build.sh

# 拉取GA
sudo podman pull parkhi/gaminganywhere:16.04