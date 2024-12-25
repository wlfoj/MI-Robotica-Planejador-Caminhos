
# Sistema de Planejamento de Caminhos

Este projeto foi desenvolvido por Washington, Nirvan e Carlos na disciplina de Robótica da Universidade Estadual de Feira de Santana (UEFS). O objetivo do projeto é criar um sistema de planejamento de caminhos para um robô, utilizando uma interface gráfica para controle e visualização. O caminho foi gerado aplicando os Campos de Potenciais.

## Descrição do Ambiente

O local onde o robô se movimenta é um ambiente estruturado. Neste tipo de espaço, pode-se fazer uso de mapas baseados na planta do prédio. A figura 1 ilustra um exemplo do espaço de armazenamento. O robô inicialmente está carregado e deve se deslocar para deixar sua carga em uma das estações existentes no mapa da figura 1. Ele deve ser capaz de se locomover seguindo uma trajetória previamente calculada. Deste modo, a equipe Runaway Desenvolvimento foi destacada para projetar e implementar um sistema de planejamento e navegação do robô.

### Restrições do Projeto

Devido à configuração da indústria e da plataforma robótica disponível, o projeto apresenta as seguintes restrições:
- O sistema de geração de trajetória deverá ser desenvolvido em computador externo ao robô;
- Inicialmente se conhece o mapa do ambiente e a posição do robô;
- O usuário arbitra a posição inicial do robô;
- A posição final deve ser dentro de uma das estações;
- O programa desenvolvido deverá ser capaz de colocar obstáculos virtuais no espaço de trabalho;
- Caso o robô encontre um obstáculo sobre a trajetória planejada, ele deve desviar e retornar à trajetória;
- O robô executa uma trajetória recebida por meio de comunicação sem fio.

## Estrutura do Projeto

O projeto está organizado nas seguintes pastas:

- `robot/`: Contém o código relacionado ao robô.
- `supervisor/`: Contém o código da interface gráfica e lógica de controle.

## Código do Robô

### Arquivo: `robot/BCP.h`

Este arquivo contém funções para comunicação e formatação de mensagens entre o robô e o supervisor. Algumas das funções principais incluem:

- `sendMessage`: Envia uma mensagem ao supervisor.
- `readMessage`: Lê uma mensagem recebida.
- `getSupervisorMessage`: Obtém uma mensagem do supervisor.
- `readDataMessage`: Lê uma mensagem de dados.
- `formatMessage`: Formata uma mensagem com um código específico.
- `formatDataMessage`: Formata uma mensagem com coordenadas x e y.

### Arquivo: `robot/main.nxc`

Este arquivo contém o código principal que controla o robô, incluindo a lógica de movimentação e comunicação com o supervisor.

## Código da Interface (Supervisor)

### Arquivo: `supervisor/interface.py`

Este arquivo contém a implementação da interface gráfica e a lógica de controle do robô. A interface foi desenvolvida utilizando PyQt5. Algumas das classes e funções principais incluem:

- `RobotArea`: Uma classe que herda de `QFrame` e é responsável por desenhar o robô, obstáculos, objetivos e trajetórias na interface.
  - `update_robot_position`: Atualiza a posição do robô na interface.
  - `paintEvent`: Desenha os elementos na interface.
  - `mousePressEvent` e `mouseReleaseEvent`: Tratam eventos de clique do mouse para desenhar obstáculos e definir objetivos e posições iniciais.
  - `add_objective`: Adiciona um objetivo na interface.
  - `add_pos`: Define a posição inicial do robô.
  - `set_rect_size`: Ajusta o tamanho dos retângulos desenhados.

- `SupervisorInterface`: Uma classe que herda de `QWidget` e é responsável por criar e gerenciar os elementos da interface.
  - `__init__`: Inicializa a interface, criando botões e layouts.
  - `control_interface`: Controla a ativação e desativação do robô.
  - `path_planning`: Realiza o planejamento de caminho utilizando um campo potencial.
  - `close_application`: Fecha a aplicação.

### Arquivo: `supervisor/constants.py`

Contém constantes utilizadas na interface e na lógica de controle.

### Arquivo: `supervisor/trajetoria.py`

Contém funções relacionadas ao cálculo de trajetórias para o robô.

### Arquivo: `supervisor/SupervisorClient.py`

Contém a lógica de comunicação entre o supervisor e o robô.

## Como Executar

1. Certifique-se de ter o Python e o PyQt5 instalados.
2. Navegue até a pasta `supervisor/`.
3. Execute o arquivo `interface.py` para iniciar a interface gráfica.

```sh
python interface.py
```
