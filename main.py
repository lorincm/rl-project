from __future__ import annotations
import argparse

from minigrid.wrappers import ImgObsWrapper, FullyObsWrapper
from gymnasium.wrappers import RecordVideo
from minigrid.manual_control import ManualControl

from stable_baselines3 import PPO

from feature_extract import MinigridFeaturesExtractor
from world import SimpleEnv


TRAIN = False
EVALUATION = not TRAIN
# MANUAL =  not TRAIN
MANUAL = False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true", help="training the model") 
    parser.add_argument("--video", action="store_true", help="creaiting a rendered video of the trained model")  
    parser.add_argument("--manual", action="store_true", help="allowing manual control for testing") 
    args = parser.parse_args()

    policy_kwargs = dict(
        features_extractor_class=MinigridFeaturesExtractor,
        features_extractor_kwargs=dict(features_dim=128),
    )

    print(args)

    if not args.train and not args.video and not args.manual:
        print("Please specify an argument before running. Type --help to see possible options")
        return

    # if using the manual arg, allow for human control and render 
    if args.manual:
        env = SimpleEnv(render_mode="human")
        manual_control = ManualControl(env, seed=42)
        manual_control.start()
    else:
        env = SimpleEnv(render_mode="rgb_array")

    #make the environment fully observable
    env = FullyObsWrapper(env)
    #obs, _ = env.reset()
    
    #only use image, no textual mission statement
    env = ImgObsWrapper(env)
    #obs, _ = env.reset()

    
    if args.video:
        env = RecordVideo(env, video_folder="ppo-grid", name_prefix="eval",
                    episode_trigger=lambda x: True)

        obs, _ = env.reset()

        try:
            model = PPO.load("PPO-grid")
            print("Model loaded!")
        except:
            print("Error while loading the model!")

        # recording agent behaviour
        for i in range(1000):
            action, _states = model.predict(obs)
            obs, _, _, _, _ = env.step(action)                
            env.render()

        env.close()
        
    if args.train:
        model = PPO("CnnPolicy", env, policy_kwargs=policy_kwargs, verbose=1)
        model.learn(2e5)

        try:
            model.save("PPO-grid")
            print("Model saved!")
        except: 
            print("Error while saving model!")
    
        

if __name__ == "__main__":
    main()
