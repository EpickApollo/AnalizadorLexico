import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"\nArchivo modificado: {event.src_path}")
            print("Reiniciando GUI...\n")
            os.system("python gui.py")  # Ejecuta tu GUI nuevamente

# Carpeta actual
path = "."
observer = Observer()
observer.schedule(ReloadHandler(), path, recursive=False)
observer.start()

print("Observando cambios en archivos .py... Presiona Ctrl+C para detener.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
