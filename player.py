import vlc
import tkinter as tk
from tkinter import ttk

class StreamPlayer:
    def __init__(self):
        # Configurar VLC con un buffer mínimo
        self.instance = vlc.Instance("--network-caching=100")  # 100 ms de buffering
        self.player = self.instance.media_player_new()
        self.current_audio_device = None  # Dispositivo de audio seleccionado

    def get_audio_devices(self):
        # Recuperar la lista de dispositivos de salida de audio
        devices = []
        audio_output_module = self.instance.audio_output_list_get()
        for device in audio_output_module:
            devices.append(device)
        return devices

    def play_stream(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()

    def stop(self):
        self.player.stop()

    def toggle_play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            return "Play"
        else:
            self.player.play()
            return "Pause"

    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))
    
    def select_audio_device(self, device_index):
        """Seleccionar un dispositivo de audio por índice de la lista"""
        if 0 <= device_index < len(self.audio_devices):
            device = self.audio_devices[device_index]
            self.current_audio_device = device
            self.player.audio_output_device_set(device)
            print(f"Dispositivo de audio seleccionado: {device}")
        else:
            print("Índice de dispositivo no válido")

    def get_available_audio_devices(self):
        """Mostrar los dispositivos de audio disponibles"""
        return self.audio_devices


class AudioPlayerApp(tk.Tk):
    def __init__(self, player):
        super().__init__()

        self.player = player

        self.title("Reproductor de Audio Stream")
        self.geometry("400x200")

        # Etiqueta para mostrar los dispositivos de audio disponibles
        self.label = tk.Label(self, text="Selecciona el dispositivo de salida de audio:")
        self.label.pack(pady=10)

        # Crear un combobox (menú desplegable) con los dispositivos de audio
        self.device_selector = ttk.Combobox(self, values=self.player.get_available_audio_devices())
        self.device_selector.pack(pady=10)
        
        # Configurar el valor por defecto en el primer dispositivo si existe
        if self.player.get_available_audio_devices():
            self.device_selector.set(self.player.get_available_audio_devices()[0])

        # Botón para aplicar la selección de salida de audio
        self.select_button = tk.Button(self, text="Seleccionar Dispositivo", command=self.select_audio_device)
        self.select_button.pack(pady=10)

        # Botón para reproducir/pausar
        self.toggle_button = tk.Button(self, text="Play", command=self.toggle_play_pause)
        self.toggle_button.pack(pady=10)

    def select_audio_device(self):
        # Obtener el dispositivo seleccionado y establecerlo en el reproductor
        selected_device = self.device_selector.get()
        if selected_device:
            device_index = self.player.get_available_audio_devices().index(selected_device)
            self.player.select_audio_device(device_index)
            print(f"Dispositivo seleccionado: {selected_device}")

    def toggle_play_pause(self):
        # Alternar entre reproducir y pausar
        status = self.player.toggle_play_pause()
        self.toggle_button.config(text=status)

    def update(self):
        # Actualizar la interfaz gráfica (requerido para mantener la UI respondiendo)
        self.after(100, self.update)


if __name__ == "__main__":
    # Crear la instancia del reproductor
    player = StreamPlayer()

    # Crear la instancia de la aplicación con la UI
    app = AudioPlayerApp(player)

    # Mostrar la ventana de la aplicación
    app.mainloop()