
# Sistema Solar em Blender

Este script cria uma animação do Sistema Solar usando Blender, incluindo o Sol, os planetas e suas órbitas.

## Funcionalidades

- Cria o Sol e os oito planetas do Sistema Solar
- Anima as órbitas dos planetas
- Adiciona labels para cada corpo celeste
- Cria uma câmera animada que orbita o sistema
- Adiciona iluminação e um fundo de universo estrelado

## Requisitos

- Blender 4.2.2 ou superior
- Python 3.7 ou superior

## Como usar

1. Abra o Blender
2. Vá para a aba "Scripting"
3. Cole o código fornecido no editor de texto
4. Clique em "Run Script"

## Detalhes do script

O script realiza as seguintes operações:

1. Limpa a cena atual
2. Define a duração da animação e o FPS
3. Cria funções auxiliares para:
   - Criar esferas (planetas)
   - Adicionar emissão ao Sol
   - Criar órbitas animadas
   - Adicionar labels aos corpos celestes
4. Cria o Sol
5. Cria os planetas com suas respectivas órbitas
6. Cria e anima uma câmera que orbita o sistema
7. Adiciona uma luz do tipo 'SUN'
8. Cria um fundo de universo usando texturas procedurais

## Personalização

Você pode facilmente personalizar o sistema solar alterando os parâmetros dos planetas no dicionário `planetas`. Cada planeta tem as seguintes propriedades:

- nome: Nome do planeta
- raio: Tamanho relativo do planeta
- cor: Cor do planeta (RGBA)
- orbita: Distância da órbita em relação ao Sol
- tempo: Duração da órbita em frames

## Renderização

Após executar o script, você pode renderizar a animação usando as configurações de renderização padrão do Blender ou personalizá-las conforme necessário.