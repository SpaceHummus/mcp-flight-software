'''
This is the main function to be executed by linux computer.
It runs as a "single shot". Collects telemetry, decides what is the next thing to do, then dies.
'''

from git_update_code import git_update_code

if __name__ == "__main__":
    print("Hello World")
    # Finally, update code for next run
    git_update_code()