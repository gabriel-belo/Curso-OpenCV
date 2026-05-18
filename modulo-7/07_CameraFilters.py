import cv2
# Uma biblioteca nativa do Python usada para interagir com o sistema operacional. 
# No código, ela serve para verificar se você passou algum argumento via linha de 
# comando ao executar o script (como especificar o índice de uma câmera externa).
import sys
import numpy

PREVIEW  = 0   # Preview Mode
BLUR     = 1   # Blurring Filter
FEATURES = 2   # Corner Feature Detector
CANNY    = 3   # Canny Edge Detector

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.2,
                       minDistance = 15,
                       blockSize = 9)

# webcam embutida no PC é o número 0, então por padrão vamos usar 0
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

image_filter = PREVIEW
alive = True

win_name = 'Camera Filters'
# Cria uma janela gerenciada pelo OpenCV para exibir o resultado. O modo 
# WINDOW_NORMAL permite que você clique nas bordas da janela e a redimensione livremente na tela.
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
result = None

#Define para fazer a captura através dessa câmera
source = cv2.VideoCapture(s)

while alive:
    has_frame, frame = source.read() #source.read() pega a foto atual da câmera
    if not has_frame:
        break
    
    # Inverte a imagem horizontalmente (o argumento 1 faz o flip no eixo Y). Isso 
    # serve para gerar o "efeito espelho", tornando a experiência de olhar para a 
    # webcam muito mais natural.
    frame = cv2.flip(frame,1)

    if image_filter == PREVIEW:
        result = frame
    elif image_filter == CANNY:
        result = cv2.Canny(frame, 80, 150)
    elif image_filter == BLUR:
        result = cv2.blur(frame, (13,13))
    elif image_filter == FEATURES:
         result = frame
         frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         corners = cv2.goodFeaturesToTrack(frame_gray, **feature_params)
         if corners is not None:
             for x, y in numpy.float32(corners).reshape(-1, 2):
                 cv2.circle(result, (x,y), 10, (0, 255 , 0), 1)

    # Atualiza a janela que criamos no início, mostrando o frame final processado 
    # para o usuário.
    cv2.imshow(win_name, result)


    # A função cv2.waitKey(1) fica esperando 1 milissegundo por uma reação sua no teclado.

    # - Se você apertar C, o filtro muda para Canny.

    # - Se apertar B, muda para Blur.

    # - Se apertar F, ativa o detector de quinas (Features).

    # - Se apertar P, volta para o Preview normal.

    # - Se apertar Q ou a tecla ESC (código 27), o loop quebra e o programa fecha de 
    # forma segura.

    key = cv2.waitKey(1)
    if key == ord('Q') or key == ord('q') or key == 27:
        alive = False
    elif key == ord('C') or key == ord('c'):
        image_filter = CANNY
    elif key == ord('B') or key == ord('b'):
        image_filter = BLUR
    elif key == ord('F') or key == ord('f'):
        image_filter = FEATURES
    elif key == ord('P') or key == ord('p'):
        image_filter = PREVIEW

# Desliga a câmera e libera o hardware para que outros aplicativos 
# do seu computador possam usá-la.
source.release()
# Fecha a janela aberta pelo OpenCV e limpa a memória do sistema.
cv2.destroyWindow(win_name)

# Os Filtros de Imagem

# Modo CANNY (Detector de Bordas)
# cv2.Canny(frame, 80, 150): Transforma o frame em um mapa de linhas pretas e brancas
# realçando os contornos físicos dos objetos. Os números 80 e 150 são os limiares 
# (thresholds) mínimo e máximo que o algoritmo usa para decidir se um gradiente de 
# pixel é uma borda real ou apenas ruído.

# Modo BLUR (Suavização/Desfoque)
# cv2.blur(frame, (13,13)): Aplica um filtro de 
# desfoque (Blur Médio). O argumento (13,13) é o tamanho do Kernel (uma caixinha de 
# $13 \times 13$ pixels). O OpenCV passa essa caixinha por toda a imagem, calcula a 
# média dos pixels ali dentro e substitui o pixel central por essa média. 
# Quanto maior esse número, mais embaçada a imagem fica.


# Modo FEATURES (Detector de Quinas / Cantos)
# Este é o bloco mais complexo do código. Ele tenta achar pontos de interesse na 
# imagem (quinas de móveis, os cantos dos olhos/boca, etc.) que são ideais para 
# algoritmos de rastreamento de objetos.

# cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY): Converte a imagem colorida (BGR) para 
# Escala de Cinza. Algoritmos de detecção matemática quase sempre exigem imagens de 
# 1 canal só para rodar mais rápido e focar apenas nas mudanças de intensidade de cor.

# cv2.goodFeaturesToTrack(...): Aplica o algoritmo de Shi-Tomasi para encontrar as 
# quinas mais proeminentes na imagem baseando-se no dicionário feature_params 
# (procurando no máximo 500 cantos, com nível de qualidade de 0.2 e distância mínima 
#  de 15 pixels entre eles).

# numpy.float32(corners).reshape(-1, 2): O OpenCV retorna os cantos em uma matriz 
# tridimensional complexa. Esse comando do NumPy reorganiza os dados para uma lista 
# simples de coordenadas flutuantes (x, y).

# cv2.circle(result, (x,y), 10, (0, 255, 0), 1): Desenha um círculo geométrico em 
# cima do frame original. Ele usa a coordenada (x,y) do canto detectado como centro, 
# define o raio em 10 pixels, a cor em (0, 255, 0) (Verde puro no padrão BGR) e a 
# espessura da linha em 1.