import signal, sys
from time import sleep

def terminated(signum,frame):
    print(f"received signal: {signum}")

signal.signal(signal.SIGTERM, terminated) # Capture Ctrl+C
signal.signal(signal.SIGINT, terminated) # Capture termination signal

print("Running... Press Ctrl+C to interrupt")

try:
    while True:
        siginfo = signal.sigwaitinfo({signal.SIGINT,signal.SIGTERM})
        with open("terminated.txt", "w") as f:
            f.write("Process terminated by:\n")
            f.write(f"Signal number (si_signo): {siginfo.si_signo}\n")
            f.write(f"Signal code (si_code): {siginfo.si_code}\n")
            f.write(f"Sending process PID (si_pid): {siginfo.si_pid}\n")
            f.write(f"Sending user UID (si_uid): {siginfo.si_uid}\n")

        sys.exit(0)
except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")

print("Terminación por defecto. OK")