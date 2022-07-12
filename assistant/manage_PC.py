import os 


class mng_work_space:
    def block_display() -> None:
        os.system("Rundll32.exe user32.dll, LockWorkStation")
    
    def reboot() -> None:
        os.system("shutdown -r -t 0")

    def shutdown() -> None:
        os.system("shutdown -s -t 0")