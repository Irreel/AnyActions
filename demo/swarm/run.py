from swarm.repl import run_demo_loop
from agents import travel_agent

if __name__ == "__main__":
    run_demo_loop(travel_agent, stream=True)
