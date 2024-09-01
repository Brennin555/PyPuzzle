import cv2
import os

def splitImage(path_img, path_puzzle, n, target_size=(300, 300)):
    images_names = []
    images = []

    # Verifica se a pasta existe, se não, cria a pasta
    if not os.path.exists(path_puzzle):
        os.makedirs(path_puzzle)

    # Carrega as imagens e redimensiona para o tamanho alvo
    for filename in os.listdir(path_img):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            images_names.append(filename)
            img = cv2.imread(os.path.join(path_img, filename))
            if img is not None:  # Verifica se a imagem foi carregada corretamente
                resized_img = cv2.resize(img, target_size)
                images.append(resized_img)
            else:
                print(f"Erro ao carregar a imagem: {filename}")

    # Divide as imagens redimensionadas
    for index, img in enumerate(images):
        faseNumber = index + 1
        
        # Pegando as dimensões da imagem redimensionada
        h, w = img.shape[:2]
        # Dividindo a imagem em nxn
        h = h // n
        w = w // n
        for i in range(n):
            for j in range(n):
                # Pegando a parte da imagem
                piece = img[i*h:(i+1)*h, j*w:(j+1)*w]

                # Salvando a imagem
                ext = os.path.splitext(images_names[index])[1]  # Obtém a extensão do arquivo
                save_path = os.path.join(path_puzzle, f"{n}x{n}/{faseNumber}")
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                cv2.imwrite(os.path.join(save_path, f"{i}x{j}{ext}"), piece)

# Exemplo de uso
splitImage("teste/imagens", "teste/fases", 3)
splitImage("teste/imagens", "teste/fases", 4)
splitImage("teste/imagens", "teste/fases", 8)