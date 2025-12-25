import cv2
import numpy as np
import random
import os

# Affiche le dossier courant et son contenu
print("Dossier courant :", os.getcwd())
print("Contenu :", os.listdir())

# Chargement des cascades Haar
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

if face_cascade.empty() or smile_cascade.empty():
    raise SystemExit("Cascade Haar introuvable")

# Chargement des images utilisées dans le projet
img_hat = cv2.imread("mimi.jpeg")        # chapeau
img_moustache = cv2.imread("m.jpeg")     # moustache
img_glasses = cv2.imread("l.jpeg")       # lunettes
img_snow = cv2.imread("neige.png")       # flocon de neige

if img_hat is None or img_moustache is None or img_glasses is None or img_snow is None:
    raise SystemExit("Image introuvable")

# États des options du menu
use_filter = True
use_hat = True
use_glasses = True
use_moustache = True
use_snow = True

# Ouverture de la webcam (spécifique macOS)
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
if not cap.isOpened():
    raise SystemExit("Webcam non accessible")

ret, frame = cap.read()
H, W = frame.shape[:2]

# Création de la fenêtre OpenCV
WINDOW_NAME = "TD7 - Projet Traitement d'Images"
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME, 960, 720)

# Initialisation des flocons de neige
snowflakes = []
for _ in range(15):
    snowflakes.append({
        "x": random.randint(0, W),
        "y": random.randint(-H, 0),
        "speed": random.randint(3, 6),
        "size": random.randint(25, 40)
    })

# Fonction pour appliquer un filtre sépia
def sepia(frame):
    kernel = np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]
    ])
    out = cv2.transform(frame, kernel)
    return np.clip(out, 0, 255).astype(np.uint8)

# Fonction pour incruster une image avec fond noir
def overlay_image(bg, fg, x, y, w, h):
    H, W = bg.shape[:2]
    if x < 0 or y < 0 or x + w > W or y + h > H:
        return

    fg = cv2.resize(fg, (w, h))
    gray = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    roi = bg[y:y+h, x:x+w]
    bg_part = cv2.bitwise_and(roi, roi, mask=mask_inv)
    fg_part = cv2.bitwise_and(fg, fg, mask=mask)

    bg[y:y+h, x:x+w] = cv2.add(bg_part, fg_part)

# Variables pour stabiliser la détection du sourire
smile_counter = 0
SMILE_THRESHOLD = 6

# Boucle principale
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Application du filtre si activé
    if use_filter:
        frame = sepia(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    face_box = None
    smile_detected = False

    # Détection du visage
    for (x, y, w, h) in faces:
        face_box = (x, y, w, h)

        # Zone de détection du sourire
        roi_smile = gray[y + int(0.6*h): y + h, x: x + w]
        smiles = smile_cascade.detectMultiScale(
            roi_smile, 1.7, 25, minSize=(30, 30)
        )

        if len(smiles) > 0:
            smile_counter += 1
        else:
            smile_counter = max(0, smile_counter - 1)

        if smile_counter >= SMILE_THRESHOLD:
            smile_detected = True

        # Incrustations sur le visage
        if use_hat:
            overlay_image(frame, img_hat, x, y - int(0.5*h), w, int(0.5*h))

        if use_glasses:
            overlay_image(frame, img_glasses,
                          x + int(0.05*w), y + int(0.25*h),
                          int(0.9*w), int(0.3*h))

        if use_moustache:
            overlay_image(frame, img_moustache,
                          x + int(0.2*w), y + int(0.6*h),
                          int(0.6*w), int(0.25*h))

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        break

    # Animation des flocons de neige
    if use_snow:
        for flocon in snowflakes:
            flocon["y"] += flocon["speed"]

            if flocon["y"] > H:
                flocon["y"] = random.randint(-100, 0)
                flocon["x"] = random.randint(0, W)

            fx, fy, fs = flocon["x"], flocon["y"], flocon["size"]

            collision = False
            if face_box:
                x, y, w, h = face_box
                if fx < x+w and fx+fs > x and fy < y+h and fy+fs > y:
                    collision = True

            if collision:
                cv2.circle(frame, (fx+fs//2, fy+fs//2), fs//2, (0,0,255), -1)
            else:
                overlay_image(frame, img_snow, fx, fy, fs, fs)

    # Affichage d’un objet si l’utilisateur sourit
    if smile_detected:
        cv2.rectangle(frame,
                      (W//2 - 70, H - 150),
                      (W//2 + 70, H - 60),
                      (255, 200, 120), -1)

    # Texte du menu clavier
    cv2.putText(frame,
        "[f]Filtre [h]Chapeau [g]Lunettes [m]Moustache [n]Neige [q]Quitter",
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    cv2.imshow(WINDOW_NAME, frame)

    # Gestion du menu clavier
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    elif key == ord('f'): use_filter = not use_filter
    elif key == ord('h'): use_hat = not use_hat
    elif key == ord('g'): use_glasses = not use_glasses
    elif key == ord('m'): use_moustache = not use_moustache
    elif key == ord('n'): use_snow = not use_snow

cap.release()
cv2.destroyAllWindows()
