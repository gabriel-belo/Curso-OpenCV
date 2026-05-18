# Curso-OpenCV
Curso do freeCodeCamp "OpenCV Python Course - Learn Computer Vision and AI"

1. O Mundo Digital (Pixels Absolutos)No ambiente digital (que é o que importa para o seu curso de OpenCV e processamento de imagens), a resolução é a quantidade total de pixels.Se você tem uma imagem com $1920 \times 1080$ pixels (Full HD), a resolução dela é a multiplicação desses dois valores: 2.073.600 pixels (ou aproximadamente 2 Megapixels).Quanto mais pixels, mais informação a matriz da imagem possui e mais detalhes o OpenCV consegue analisar.Neste cenário, mais pixels = maior resolução.

A resolução no mundo digital está diretamente ligada a quantidade de pixels que eu tenho em uma imagem, mas é diferente para o olho humano ver uma imagem em uma TV ou em uma tela de celular caso ela tenha a mesma quantidade de pixels.

Para o código OpenCV, é  indiferente (a matriz de dados é exatamente a mesma). Porém, para o olho humano (no mundo físico), não é indiferente. Na TV, a imagem parecerá ter "menos resolução visual" (ficará mais pixelada ou borrada) porque os mesmos pixels foram esticados em uma área gigante. No celular, os pixels ficam espremidos, dando uma sensação de nitidez muito maior.

***

1. Por que o Recorte (Crop) altera a resolução?
No OpenCV, uma imagem é uma matriz de pixels. Fazer um recorte significa, literalmente, extrair uma submatriz da imagem original.

Se você tem uma imagem original de 1000 x 1000 pixels (1 milhão de pixels no total) e faz um recorte quadrado bem no centro, pegando apenas a metade da largura e da altura, a sua nova imagem recortada terá 500 x 500 pixels (250 mil pixels).

Por que isso acontece?
Porque você jogou fora os pixels das bordas. Como a resolução digital é a contagem total de pixels, ao reduzir o tamanho da matriz, a resolução diminui proporcionalmente. Não há interferência destrutiva nos pixels que restaram; eles continuam idênticos. O que mudou foi que agora você tem menos dados totais.

2. O que é o Redimensionamento (Resize)?
Redimensionar é alterar o tamanho da matriz da imagem (suas dimensões de largura e altura) através de algoritmos matemáticos chamados interpolação.

Diferente do recorte (que joga pedaços fora), o redimensionamento esmaga ou estica a imagem inteira:

Downsampling (Diminuir): O algoritmo combina vários pixels vizinhos em um só para reduzir o tamanho do arquivo.

Upsampling (Aumentar): O algoritmo precisa "inventar" pixels onde eles não existem para preencher o novo espaço maior, baseando-se nos pixels vizinhos.

3. A relação entre Resolução e Redimensionamento no Recorte
Existe um mito de que é possível recortar uma imagem e "manter a resolução original" aumentando o recorte logo em seguida. Na prática, matematicamente, você sempre perde informação ao recortar.

Se você recortar uma imagem (reduzindo-a para 500x500) e depois usar um redimensionamento para esticá-la de volta para 1000x1000, você não recuperará a resolução real. A imagem ficará embaçada ou pixelada. Isso acontece porque o OpenCV terá que duplicar ou interpolar os pixels para preencher o espaço vazio, criando uma falsa resolução.

Como mitigar a perda visual (O Segredo da Interpolação)
Para que o seu recorte não pareça perder tanta qualidade quando você precisar redimensioná-lo, você deve escolher o algoritmo de interpolação correto no OpenCV através do parâmetro interpolation.

Aqui está como fazer isso no seu código:

Python
import cv2

###  1. Carrega a imagem original (Ex: 1920x1080)
img = cv2.imread("sua_imagem.jpg")

### 2. Faz o recorte (Crop) usando fatiamento de matrizes (Slicing)
Digamos que o recorte resulte em uma imagem pequena de 300x300

crop_img = img[200:500, 400:700] 

### 3. Redimensiona o recorte para que ele fique maior sem perder tanta nitidez
Para AUMENTAR imagens, a melhor interpolação é a INTER_CUBIC ou INTER_LANCZOS4

largura_nova = 600
altura_nova = 600
dimensoes = (largura_nova, altura_nova)

recorte_ampliado = cv2.resize(crop_img, dimensoes, interpolation=cv2.INTER_CUBIC)

### Salva o resultado
cv2.imwrite("recorte_perfeito.jpg", recorte_ampliado)
Guia rápido de Interpolação no OpenCV:
Ao usar cv2.resize(), mude o final do código dependendo do seu objetivo:

cv2.INTER_NEAREST: Muito rápido, mas deixa a imagem pixelada (efeito escada).

cv2.INTER_LINEAR: É o padrão. Bom para redimensionamentos gerais.

cv2.INTER_CUBIC: Mais lento, porém excelente para aumentar o tamanho de recortes, pois analisa os 16 pixels ao redor para suavizar a imagem.

cv2.INTER_AREA: O melhor e mais recomendado para quando você precisa diminuir o tamanho de uma imagem.

## Resumo para fixar:
* Recorte (Crop): Diminui o tamanho da matriz (menos resolução total), mas preserva a qualidade original dos pixels que restaram.

* Downsampling (Diminuir): Diminui a resolução e perde detalhes reais da imagem.

* Upsampling (Aumentar): Aumenta a resolução (no papel/no arquivo), mas não cria detalhes novos, gerando uma imagem borrada por conta dos pixels artificiais.

***

## Para entender o porquê da soma mudar o brilho e não a cor, precisamos olhar para a matemática dos canais de cores.

### O Segredo: A Proporção entre os Canais
No padrão RGB (ou BGR no OpenCV), uma cor não é definida por um único número, mas sim pela proporção matemática entre os três canais.Imagine que você tem uma cor RGB pura, um Tom de Laranja:

* R = 200$ (Muito vermelho)
* G = 100$ (Metade de verde)
* B = 0$ (Nada de azul)

A "receita" do seu laranja é ter o dobro de Vermelho em relação ao Verde. Enquanto essa proporção existir, o cérebro humano identificará aquela cor como "laranja".

1. A Operação de Adição (Por que muda o Brilho?)Quando você soma um valor fixo (por exemplo, $+50$) a uma imagem colorida, o OpenCV soma esse valor em todos os três canais ao mesmo tempo:

* $R = 200 + 50 = 250$
* $G = 100 + 50 = 150$
* $B = 0 + 50 = 50$

Repare o que aconteceu: Todos os canais ganharam mais energia (chegaram mais perto do 255, que é o branco total). Como o pixel agora reflete mais luz em todas as frequências, o seu olho interpreta isso como um aumento de brilho.
A cor mudou? Um pouco (ela ficou mais "lavada" ou pastel porque adicionamos azul onde não tinha), mas a dominância ainda é do Vermelho e do Verde, mantendo a essência do "laranja, só que mais claro".

⚠️ A quebra da cor na Adição: A cor só muda drasticamente na adição por causa de um efeito chamado Estouro (Clipping). Se você somar $+100$ naquele pixel:


* $R = 200 + 100 = 300 \rightarrow$ Trava em 255 (limite do OpenCV)

* $G = 100 + 100 = 200$

* $B = 0 + 100 = 100$
    
Como o Vermelho bateu no teto (255) e não pôde crescer mais, a proporção matemática se quebrou. Agora a imagem começa a distorcer a cor real, caminhando para o branco.

2. A Operação de Multiplicação (Contraste)A multiplicação é a forma perfeita de alterar o Contraste ou a Intensidade sem distorcer a cor, porque ela preserva as proporções exatas.Se multiplicarmos o nosso laranja original $(200, 100, 0)$ por $1.2$ (aumento de 20%):

* $R = 200 \times 1.2 = 240$
* $G = 100 \times 1.2 = 120$
* $B = 0 \times 1.2 = 0$

Veja a mágica: $240$ continua sendo exatamente o dobro de $120$. A proporção da receita mudou? Não. A cor mudou? Não, continua sendo o mesmo tom de laranja. Porém, ela está com mais energia (mais intensa)

.Se multiplicarmos por $0.5$ (redução):

* $R = 200 \times 0.5 = 100$

* $G = 100 \times 0.5 = 50$

* $B = 0 \times 0.5 = 0$

A proporção de 2 para 1 continua intacta. É o mesmo laranja, só que mais "escuro" (menos intenso). O contraste se baseia nisso: pixels claros ficam mais claros, pixels escuros ficam mais escuros, afastando a distância entre eles.

E como eu mudo a COR diretamente então?

Se você quiser mudar a cor (transformar um carro azul em um carro verde no OpenCV) através de operações matemáticas, alterar o RGB diretamente é muito difícil porque você teria que recalcular proporções complexas.

É por isso que no processamento de imagens nós convertemos a imagem para outro padrão espacial chamado HSV (Hue, Saturation, Value / Matiz, Saturação, Valor):

* H (Matiz): É um canal que isola a COR puramente em um ângulo de 0 a 180 (no OpenCV). O vermelho está em um número, o verde em outro, o azul em outro.

* S (Saturação): É a pureza da cor (olha a multiplicação aqui de novo).

* V (Valor): É o brilho (olha a adição aqui).

Se você converter para HSV, você pode simplesmente somar $+30$ apenas no canal H. O OpenCV vai mudar a cor do pixel de azul para verde diretamente, sem mexer no brilho ou na sombra da imagem.

***

* Escala de Cinza: Cada pixel é apenas 1 número (0 a 255). Se você der print na imagem, verá uma matriz de números simples.

* RGB, BGR e HSV: Cada pixel é composto por um grupo de 3 números (canais). Se você der print em uma imagem dessas, verá uma matriz onde cada elemento é uma lista de três valores (ex: [200, 100, 50]). Eles precisam trabalhar juntos para que o computador saiba o que exibir ali.

Vamos desmistificar de vez como cada um desses três padrões define a cor e por que a adição/multiplicação mexe no brilho e no contraste, e não na cor em si.

### Parte 1: Como as cores são definidas em cada padrão?
1. RGB e BGR (Os "Aditivos" de Luz)
Eles funcionam exatamente da mesma forma, a única diferença é a ordem em que o OpenCV guarda as informações na memória.

* RGB: Guarda como [Vermelho, Verde, Azul]

* BGR: Guarda como [Azul, Verde, Vermelho] (Este é o padrão do OpenCV!)

Eles simulam o comportamento de três lâmpadas coloridas microscópicas brilhando juntas dentro de cada pixel da sua tela. Cada número (de 0 a 255) diz o quão "forte" aquela lâmpada específica está brilhando.

* [255, 0, 0] no padrão RGB significa: Lâmpada Vermelha no máximo, as outras apagadas. Resultado: Vermelho Puro.

* [255, 255, 255] significa: Todas as três lâmpadas no máximo. A mistura de todas as luzes gera o Branco.

* [0, 0, 0] significa: Todas as lâmpadas apagadas. Ausência de luz é o Preto.

2. HSV (O modo "Humano")
O HSV abandona a ideia de lâmpadas coloridas e separa a imagem em três conceitos que fazem mais sentido para nós:

* H (Hue / Matiz): É a COR puramente dita. No OpenCV, varia de 0 a 180 (representando um círculo de cores). Se você quer mudar de Vermelho para Azul ou Verde, você altera apenas esse primeiro número.

* S (Saturation / Saturação): É a "vivacidade" da cor (0 a 255). 0 é totalmente sem cor (cinza) e 255 é a cor no seu estado mais vivo e purificado.

* V (Value / Brilho): É a quantidade de luz (0 a 255). 0 é totalmente escuro (preto) e 255 é a cor totalmente iluminada.


## Parte 2: Por que as operações alteram o Brilho/Contraste e não a Cor?
Para entender isso no RGB/BGR, imagine que as três lâmpadas (Vermelho, Verde e Azul) estão acesas em potências diferentes para formar uma cor. A cor que o seu olho enxerga depende do equilíbrio (proporção) entre elas.

Imagine um pixel com a cor [200, 100, 0] (Vermelho forte, Verde médio, Azul desligado). Isso gera um Laranja. A receita desse laranja é: O vermelho precisa ser o dobro do verde, e o azul não joga.

#### A Adição ($+$) altera o Brilho porque adiciona luz branca

Quando você faz imagem + 50, o OpenCV vai em cada pixel e soma 50 nas três lâmpadas ao mesmo tempo.

* O Laranja [200, 100, 0] vira [250, 150, 50].

#### O que aconteceu com a cor?

A lâmpada vermelha continua sendo a mais forte, a verde a do meio, e a azul a mais fraca. A "hierarquia" não mudou. Porém, como você injetou 50 de energia em todos os canais, o pixel agora emite muito mais luz no total. Além disso, você acendeu a lâmpada azul (que estava em 0), o que joga um pouco de luz branca na mistura. O resultado é o mesmo Laranja, só que mais iluminado (brilhante) e levemente mais "pastel".


#### A Multiplicação ($*$) altera o Contraste porque altera a distância entre os valores

O contraste é a diferença entre o que é claro e o que é escuro na imagem. Na multiplicação por uma constante (ex: imagem * 1.5), as proporções originais mudam de escala, mas mantêm a mesma relação matemática perfeita.
Imagine que você tem dois pixels na imagem (um Laranja claro e um Laranja escuro):
* Pixel Claro: [100, 50, 0] (O vermelho é 50 pontos maior que o verde)
* Pixel Escuro: [40, 20, 0] (O vermelho é 20 pontos maior que o verde)

Se multiplicarmos ambos por $2$:
* Pixel Claro vira: [200, 100, 0] (Agora o vermelho é 100 pontos maior que o verde)
* Pixel Escuro vira: [80, 40, 0] (Agora o vermelho é 40 pontos maior que o verde)

Veja o que a multiplicação fez:

1. Manteve a cor: $200$ ainda é o dobro de $100$, e $80$ ainda é o dobro de $40$. A receita do Laranja continua perfeitamente intacta. A cor não mudou de tom.
2. Aumentou o Contraste: Antes, a diferença de força entre o pixel claro e o escuro era pequena. Depois da multiplicação, o pixel claro ficou muito mais claro, e o escuro subiu bem menos. A distância entre eles aumentou. Isso é o aumento de contraste!

### Resumo definitivo:

Operações matemáticas comuns (soma e multiplicação) aplicadas nos três canais RGB/BGR alteram apenas a quantidade de luz (energia) que o pixel emite ou a distância entre as luzes dos pixels vizinhos. Como elas afetam os três canais juntos, elas preservam a "receita" básica daquela cor, mudando apenas sua intensidade (brilho) ou sua dinâmica na imagem (contraste).

* A Proporção entre os canais dita qual é a cor (a identidade dela: se é laranja, azul, roxo ou verde).

* A Quantidade (ou intensidade) dos valores dita as características/estados dessa cor (se ela está sob a luz, na sombra, se é vibrante ou opaca).

Quando você for criar um código para detectar, por exemplo, um objeto vermelho na câmera (usando cv2.inRange()), se você tentar fazer isso em BGR/RGB, o seu código vai falhar miseravelmente se o objeto passar por uma sombra, porque a quantidade de pixels vai cair e os números vão mudar.

É por isso que, para detecção de cores por IA ou visão computacional, nós sempre convertemos para HSV antes. Como o HSV separa a proporção (Matiz/Hue) da quantidade de luz (Value) e da pureza (Saturation), você pode dizer ao OpenCV: "Ignore as variações de iluminação e saturação, foque apenas no ângulo da cor".

***
A multiplicação crua (global) mexe tanto no contraste quanto no brilho. Você está certíssimo na sua linha de raciocínio matemático. Se multiplicarmos todos os pixels por $1.2$, os pixels escuros sobem um pouco e os pixels claros sobem muito, jogando todo mundo mais perto do $255$ (branco).

No entanto, no processamento de imagens profissional e no OpenCV, nós separamos esses dois conceitos através de uma fórmula matemática clássica para que o contraste não destrua o brilho original da imagem (e vice-versa).

A fórmula padrão para ajustar brilho e contraste ao mesmo tempo é uma equação linear:

$$g(x, y) = \alpha \cdot f(x, y) + \beta$$

Onde:

* $f(x, y)$ é o pixel original.
* $g(x, y)$ é o pixel final modificado.
* $\alpha$ (alfa) é o ganho que controla o contraste (multiplicação).
* $\beta$ (beta) é o bias que controla o brilho (adição/subtração).


O problema de usar apenas o $\alpha$ (Multiplicação Pura)

Se você usar apenas o $\alpha = 1.2$, acontece exatamente o que você descreveu: a imagem inteira ganha energia e fica mais clara (o brilho médio sobe).

Para corrigir esse efeito colateral e aumentar o contraste mantendo o brilho equilibrado, os desenvolvedores usam um truque matemático: eles mudam o "ponto de ancoragem" da multiplicação para o meio do caminho (o cinza médio, valor $127$), em vez do zero.

A lógica ideal para alterar o contraste puro seria:

1. Subtrai $127$ do pixel (leva o meio da imagem para o zero).

2. Multiplica pelo fator de contraste ($1.2$).

3. Soma $127$ de volta.

Dessa forma, os valores acima de $127$ ficam ainda mais altos (vão para o branco) e os valores abaixo de $127$ ficam ainda mais baixos (vão para o preto). O brilho médio da imagem permanece estático, mas os extremos se afastam!

#### O Histograma de Cores

Para visualizar perfeitamente o que você deduziu, os professores costumam mostrar o Histograma da imagem (um gráfico que mostra a distribuição dos pixels do 0 ao 255).

* Quando você soma (Brilho): O gráfico inteiro "desliza" para a direita (em direção ao 255) ou para a esquerda (em direção ao 0), mantendo o mesmo formato.

* Quando você multiplica por $> 1$ (Contraste Puro): O gráfico "estica" e se expande. As colunas se afastam umas das outras. Como você bem notou, ele se expande empurrando a massa de dados para a direita, aumentando também o brilho geral se não for compensado por um valor negativo de $\beta$.

***

A limiarização (ou Thresholding, em inglês) é uma das técnicas de segmentação mais antigas, simples e fundamentais no processamento de imagens com OpenCV.

O objetivo principal dela é isolar o que importa na imagem (o "objeto" ou foreground) do que não importa (o "fundo" ou background), transformando uma imagem complexa em uma imagem puramente binária (preto e branco).

### Como funciona a lógica matemática?
Para aplicar a limiarização, a imagem original obrigatoriamente precisa estar em escala de cinza (onde os pixels variam de 0 a 255).

Você, como programador, define um valor de corte chamado Limiar (Threshold). O OpenCV vai varrer a imagem pixel por pixel e aplicar uma regra simples:

* Se o valor do pixel for menor que o limiar, ele vira Preto (0).

* Se o valor do pixel for maior que o limiar, ele vira Branco (255).

Imagine que você quer extrair o texto preto de uma folha de papel branca amassada. O papel (claro) terá pixels perto de 200, e as letras (escuras) terão pixels perto de 50. Se você definir um limiar de 127 (o meio do caminho):

* Tudo que for menor que 127 (as letras) vira 0 (Preto absoluto).

* Tudo que for maior que 127 (o papel) vira 255 (Branco absoluto).

* Resultado: As sombras e amassados do papel somem, restando apenas o texto perfeito.


### Os Tipos de Limiarização no OpenCV
O OpenCV oferece diferentes maneiras de reagir ao limiar. A função base é a cv2.threshold(). Veja as três mais utilizadas no mercado:

1. Limiarização Binária Simples (cv2.THRESH_BINARY)
É a regra padrão que explicamos acima. Se passar do limiar vira branco, se for menor vira preto. É excelente quando a iluminação da imagem é perfeita e uniforme.

2. Limiarização Inversa (cv2.THRESH_BINARY_INV)
Faz exatamente o oposto: o que é menor que o limiar vira branco, e o que é maior vira preto. Na visão computacional, a maioria dos algoritmos de IA (como detectores de contorno) procura por objetos brancos em fundos pretos. Se o seu objeto original for escuro, você usa o tipo inverso para "acendê-lo".

3. Limiarização Adaptativa (cv2.adaptiveThreshold)
Essa é a solução para o mundo real. Em ambientes práticos, a iluminação nunca é perfeita (há sombras, reflexos, lâmpadas mais fortes de um lado). Um único limiar global (como 127) vai falhar nas partes sombreadas da imagem.

A limiarização adaptativa não usa um limiar fixo. Ela calcula um limiar diferente para cada região minúscula da imagem, baseando-se na média dos pixels vizinhos.

***
Razões  pela qual gostariamos de aplicar blur a uma imagem, se você tiver um ruído na imagem, é possível aplicar uma pequena quantidade de desfoque(blur) e ainda assim obter um resultado esteticamente agradável, mas, mais importante ainda, em visão computacional e processamento de imagens que frequentemente usamos desfoque como etapa de pré-processamento para realizar extração de características e a razão para isso é que a maioria dos algoritmos de extração usa algum tipo de gradiente numérico e execução numérica. Os gradientes em dados de pixels brutos podem ser bastante barulhentos e podem nãoo se comportar bem, então suavizar a imagem antes de realizar gradientes, acaba sendo muito mais robusto e um bom comportamento

No universo da Visão Computacional e do Processamento de Imagens, o pré-processamento é uma das etapas mais críticas de todo o pipeline. O objetivo principal dele não é deixar a imagem "bonita" para o olho humano, mas sim limpar o ruído, destacar estruturas importantes e reduzir a complexidade dos dados para que os algoritmos matemáticos (ou redes neurais) consigam tomar decisões com maior precisão e velocidade.


## 1. O Uso de Blur (Suavização) no Pré-Processamento
Para o olho humano, uma imagem borrada parece ter menor qualidade. Para a Visão Computacional, o blur (também chamado de suavização ou filtragem passa-baixa) é uma ferramenta essencial para redução de ruído e eliminação de detalhes irrelevantes.

#### Por que usamos Blur antes de outras técnicas?
Se você tentar aplicar um detector de bordas (como o Canny que você viu no código anterior) diretamente em uma foto digital bruta, o algoritmo vai encontrar milhares de "falsas bordas". Isso acontece por causa do ruído digital da câmera (aqueles pontinhos granulados em fotos escuras) ou texturas muito finas (como os poros da pele ou fios de um tapete).

O blur age "espalhando" a intensidade dos pixels vizinhos. Isso elimina as variações bruscas e isoladas (ruído de alta frequência), deixando apenas as transições suaves e as formas estruturais grandes da imagem.

#### Principais Técnicas de Blur no OpenCV
* Blur Médio (cv2.blur ou cv2.boxFilter): Pega uma matriz de tamanho $N \times N$ (Kernel), calcula a média aritmética simples de todos os pixels ali dentro e substitui o pixel central por essa média. É rápido, mas tende a borrar as bordas reais dos objetos de forma muito agressiva.

* Blur Gaussiano (cv2.GaussianBlur): Em vez de uma média simples, ele usa uma curva Gaussiana (uma distribuição em forma de sino). Os pixels mais próximos do centro do Kernel têm um peso maior na média do que os pixels das bordas da caixinha. O resultado é um desfoque muito mais natural que preserva melhor a estrutura geométrica original do que o blur médio. É o mais utilizado antes de detectores de bordas.

* Filtro Bilateral (cv2.bilateralFilter): É o "santo graal" do pré-processamento. Ele consegue aplicar o desfoque para reduzir o ruído, mas não borra as bordas dos objetos. Ele faz isso analisando não apenas a distância espacial dos pixels, mas também a diferença de cor (intensidade) entre eles. Se houver uma mudança brusca de cor (uma borda), ele interrompe o desfoque naquela direção. É muito usado em filtros de embelezação de rostos e segmentação médica.

## 2. Outros Métodos Cruciais de Pré-Processamento
Além do desfoque, um pipeline típico de Visão Computacional utiliza uma combinação das seguintes técnicas:

#### A. Conversão de Espaço de Cores
* Teoria: Como você já compreendeu, imagens coloridas (BGR/RGB) possuem 3 canais, o que exige três vezes mais processamento e adiciona a complexidade da variação de iluminação.

* Técnica: Converter para Escala de Cinza (cv2.COLOR_BGR2GRAY) reduz a matriz de 3D para 2D, focando apenas na luminância (brilho), o que é ideal para detecção de formas, contornos e faces. Converter para HSV (cv2.COLOR_BGR2HSV) isola o canal da cor (Hue) dos canais de iluminação, ideal para segmentação por cor.

#### B. Equalização de Histograma (Ajuste de Contraste)
* Teoria: Imagens muito escuras ou muito claras dificultam a extração de características pelos algoritmos. A equalização redistribui as intensidades dos pixels para que o histograma ocupe toda a faixa de 0 a 255 uniformemente.

* Técnica: O OpenCV possui o cv2.equalizeHist() para imagens globais e o CLAHE (Contrast Limited Adaptive Histogram Equalization - cv2.createCLAHE()), que melhora o contraste localmente em pequenas partes da imagem, evitando estourar o brilho em áreas que já eram claras.


#### C. Operações Morfológicas (Erosão e Dilatação)
* Teoria: Aplicadas geralmente em imagens binárias (preto e branco) após a limiarização. Elas usam um elemento estruturante (uma pequena máscara) para modificar a forma dos objetos com base na vizinhança.

* Técnicas:Erosão (cv2.erode): "Encolhe" as áreas brancas da imagem. Serve para eliminar ruídos brancos isolados (pontinhos soltos).Dilatação (cv2.dilate): "Expande" as áreas brancas. Útil para juntar partes quebradas de um mesmo objeto (como uma linha interrompida ou uma letra mal escaneada).Abertura e Fechamento (cv2.morphologyEx): Combinações de erosão e dilatação para limpar caminhos ou tapar buracos internos em objetos.D. Redimensionamento e NormalizaçãoTeoria: Redes neurais de Deep Learning (como redes convolucionais) exigem que todas as imagens de entrada tenham exatamente o mesmo tamanho físico de matriz (ex: $224 \times 224$ pixels). Além disso, modelos de IA funcionam melhor com números pequenos.Técnica: Usa-se cv2.resize() com interpolação adequada (como cv2.INTER_AREA para reduzir). A normalização transforma os valores de 0 a 255 para uma escala de ponto flutuante entre 0.0 e 1.0 (dividindo a matriz por 255.0) ou centralizando a média em 0.