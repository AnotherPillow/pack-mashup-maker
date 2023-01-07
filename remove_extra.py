import os, re, time, shutil
def remove_extra():
    startTime = time.time()

    INPUT_DIR = 'temp'

    #list all folders in INPUT_DIR
    folders = [f for f in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, f))]

    #go through each assets/minecraft folder in each folder
    for folder in folders:
        mcpatcherPath = os.path.join(INPUT_DIR, folder, 'assets', 'minecraft', 'mcpatcher')
        if os.path.exists(mcpatcherPath):
            print(f"Removing {mcpatcherPath}")
            shutil.rmtree(mcpatcherPath)

if __name__ == '__main__':
    remove_extra()