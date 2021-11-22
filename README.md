# Podman-Mig
This is a project conducting service migration using Podman

说明：
1. cpu, io, mem, tar, video 已经成功迁移
2. snake和minecraft 由于CRIU 对x socket还不支持(截止2021年11月，podman 3.4.2 CRIU 3.16.1-1)
   具体原因参看[podman issue](https://github.com/containers/podman/issues/12275)


# 使用方法：
1. 在source node 和destination node分别部署本项目代码
2. source node上启动src_test_rsync.py 和 run_measure.py
3. destination node上启动dst_test.py
4. 