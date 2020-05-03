from AITools import MemoryHooker
import time
import numpy as np
import keyboard

pid     = 0x47E8
address = 0x09003FB8
fps = 60

inputs = np.zeros((1240), dtype=np.int8)

def main():
    hook = MemoryHooker.MemoryHooker(pid)
    #keyboard = MemoryHooker.Keyboard()
    while 1:
        value = hook.readInt32(address)
        x = (value-6)//8
        i = (x-13)//9

        if keyboard.is_pressed('w'):
            inputs[i] = 1

        if i>1240:
            break

        time.sleep(1/fps)

    hook.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass