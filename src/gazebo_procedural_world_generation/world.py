from gazebo_procedural_world_generation import utils

#


class World():
    def __init__(self, config):
        super().__init__()
        self.config = config     


        self.start = f"""<?xml version="1.0" ?>
        <sdf version="1.6">
            <world name="{self.config["world"]["name"]}">

            <plugin name="gazebo_ros_state" filename="libgazebo_ros_state.so">
                <ros>
                    <namespace>/gazebo</namespace>
                </ros>

                <update_rate>1.0</update_rate>
            </plugin>

            <include>
            <uri>model://sun</uri>
            </include>

            <include> 
                <uri>model://ground_plane</uri> 
            </include> 

                
        <!-- ************************************************************************** -->
        """
        self.end = """
        <!-- ************************************************************************** -->

            </world>
        </sdf>
        """
        self.corpus = []
        self.nb_obstacles = 0

    def compute_world(self):
        world = self.start
        for obstacle_sdf in self.corpus:
            world += obstacle_sdf
        world += self.end
        return world

    def __repr__(self):
        return self.compute_world()
    
    def add_obstacle(self, obstacle_name, grid_pose, grid_scale):
        model_path = self.config["objects"][obstacle_name]["model_path"] # sdf file path

        world_obstacle_pose = f"{grid_pose[0]*grid_scale} {grid_pose[1]*grid_scale} 0 0 0 0"  # x y z roll pitch yaw
        
        obstacle_sdf = f"""
            <include>
                <name>{obstacle_name + str(self.nb_obstacles)}</name>
                <uri>model://{model_path}</uri>
                <pose>{world_obstacle_pose}</pose>
            </include>
        """
        self.corpus.append(obstacle_sdf)
        self.nb_obstacles += 1
        return

    def save_world(self, world_path = ""):
        world_str = self.compute_world()
        if world_path == "":
            pkg_path = utils.get_project_path()
            world_path = pkg_path + "/worlds/" + self.config["world"]["name"] + ".world"

        with open(world_path, 'w') as f:
            f.write(world_str)
        return