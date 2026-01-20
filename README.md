# Actuator-dynamics-identification

This repository contains tools and experiments for **actuator dynamics identification**, with a focus on elastic and robotic actuators.
It supports data-driven modeling, parameter estimation, and validation for model-based control and analysis.

The package can be used standalone or integrated as a submodule within larger ROS 2 workspaces (e.g. `mec_ws`).

---

## Repository structure

```
Actuator-dynamics-identification/
├── identification_process/   # Identification nodes and workflows
├── launch/                   # ROS 2 launch files
├── resource/                 # Configuration files, datasets, or resources
├── test/                     # Tests or example experiments
├── package.xml               # ROS package metadata
├── setup.py / setup.cfg      # Python package configuration
├── README.md                 # This file
└── LICENSE                   # Apache-2.0 license
```

---

## Purpose

The main objectives of this repository are:

* Collection and processing of experimental actuator data
* Identification of dynamic parameters (e.g. stiffness, damping, inertia, friction)
* Validation of actuator models against measured data
* Support for control design and simulation through identified models

---

## Requirements

* Linux (recommended)
* ROS 2 Humble
* `colcon` build system
* Standard ROS 2 dependencies for data processing and visualization

---

## Building the package

From a ROS 2 workspace:

```bash
colcon build
source install/setup.bash
```

---

## Running identification workflows (ROS 2 only)

All identification routines are exposed as **ROS 2 nodes**.

Example:

```bash
ros2 run actuator_dynamics_identification identification_node
```

Or via launch files:

```bash
ros2 launch actuator_dynamics_identification identification.launch.py
```

---

## Integration with mec_ws (Docker-based)

This repository is intended to be used as a **Git submodule** inside the `mec_ws` ROS 2 workspace, which provides a Docker-based development environment.

### Steps

1. **Start the mec_ws Docker container**

From the `mec_ws` repository root:

```bash
docker compose up --build
```

Or detached:

```bash
docker compose up -d
```

2. **Enter the container**

```bash
docker compose exec ros2-dev bash
```

3. **Initialize the submodule (inside the container)**

```bash
cd ~/colcon_ws/src
git submodule update --init --recursive
```

4. **Build the workspace**

```bash
cd ~/colcon_ws
colcon build
source install/setup.bash
```

This ensures that the actuator dynamics identification package is built and run **inside the same ROS 2 Docker environment** used by `mec_ws`.

---

## Notes

* The identification workflows are designed to run entirely **inside the ROS 2 Docker container**.
* Both offline (rosbag-based) and online identification approaches are supported.
* Identified models can be used to improve control performance and simulation fidelity.

---

## License

This project is licensed under the **Apache-2.0 License**.
