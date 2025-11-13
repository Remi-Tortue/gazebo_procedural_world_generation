# gazebo_procedural_world_generation

This python package is dedicate to the creation of random gazebo maps.
The goal is to be able to test detection and navigation algorithms on a variety of maps.

## Install

```bash
cd gazebo_procedural_world_generation
pip install -e .
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:"$(pwd)/src/gazebo_procedural_world_generation/models"
```

## How it works

- Generate de grid.
- File it with collision spaces.
- Tile those spaces with obstacles.
- Generate a world map by placing obstacles accordingly to the grid.

Visualize the map via :
```bash
gazebo worlds/procedural_world.world 

```


## Overview

## Contributors
- **Rémi Porée**