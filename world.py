from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal, Key, Wall
from minigrid.minigrid_env import MiniGridEnv

from DFSMaze import MazeGenerator

import numpy as np

class SimpleEnv(MiniGridEnv):
    def __init__(
        self,
        size=10,
        agent_start_pos=(1, 1),
        agent_start_dir=0,
        max_steps: int | None = None,
        **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        generator = MazeGenerator()
        self.maze = generator.generate_maze()

        self.key_available = [True, True]
        
        
        if max_steps is None:
            max_steps = 4 * size**2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs,
        )

    @staticmethod
    def _gen_mission():
        return ""

    def _gen_grid(self, width, height):        
        
        self.grid = Grid(width, height)
        
        #generate visuals from grid
        for i in range(0,10):
            for t in range(0,10):
                if self.maze[i][t] == 1:
                    self.grid.set(t, i, Wall())
                if self.maze[i][t] == 3:                    
                    self.grid.set(t, i, Key(COLOR_NAMES[0]))    
                    self.subgoal_pos = np.ndarray((2,), buffer=np.array([t, i]), dtype=int)                           
                if self.maze[i][t] == 4:
                    #maybe set door as well later on?
                    #self.grid.set(t, i, Door(COLOR_NAMES[0], is_locked=True))
                    pass
                if self.maze[i][t] == 5:                    
                    self.grid.set(t, i, Goal())                    
        
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "grand mission"
    
    # overload the step function, so we can add some rules and rewards
    def step(self, action):
        obs, reward, terminated, truncated, info = super().step(action)

        # store truth values whether the key is available for pickup,
        # as we will be behind a step
        self.key_available[0] = self.key_available[1]
        self.key_available[1] = self.grid.get(*self.subgoal_pos) is not None

        # if pickup action is used, and the key is available and the agent standing in front of it,
        # pick the key up 
        if (action == self.actions.pickup and 
            (self.front_pos == self.subgoal_pos).all() and 
            self.key_available[0]):

            reward = self._reward() / 1.5
        
        #prevent the agent to drop the key or toggle
        if action == self.actions.drop: #or action == self.actions.toggle:
            terminated = True

        return obs, reward, terminated, truncated, info




