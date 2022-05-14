from msilib.schema import SelfReg
import random, pygame, sys


# colors
blue = (0,0,120)
white = (200,200,200)

# Inicialização
pygame.init()
clock = pygame.time.Clock()

# Configurando a janela
screenWidth = 980
screenHeight = 660
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('The ping Pong')

# Objetos
ball = pygame.Rect(screenWidth / 2 - 15, screenHeight / 2 - 15, 30, 30)
player = pygame.Rect(screenWidth - 20, screenHeight / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screenHeight / 2 - 70, 10, 140)

# variaveis
ballSpeedX = 0.5  # 500 pixels por segundo
ballSpeedY = 0.5
opponentSpeed = 2
playerSpeed = 0

# Placar
playerScore = 0
opponentScore = 0

 

#load font
font = pygame.font.SysFont('freesansbold.ttf', 25)
bigFont = pygame.font.SysFont('freesansbold.ttf', 50)

# Start and Finish Screen Flag
onStartScreen = True
onGameOverScreen = False

def inputs():
    global onStartScreen
    # Processando as entradas (eventos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP and onStartScreen:
            onStartScreen = False
          
    (x, y) = pygame.mouse.get_pos()
    player.y = y


def draw():

    global opponentScore, playerScore

    screen.fill((0, 0, 0))

    if onStartScreen:
        pressAnyKeyText = font.render(str("Press any key to start, when any reach 10, the game end"), True, white)
        screen.blit(pressAnyKeyText, (screenWidth / 2 - 200, screenHeight/2 +50) )
        pygame.display.flip()
    
    else:
        # Desenho
        pygame.draw.ellipse(screen, (200, 200, 200), ball)
        pygame.draw.rect(screen, (200, 200, 200), player)
        pygame.draw.rect(screen, (200, 200, 200), opponent)
        pygame.draw.line(screen, white, (screenWidth / 2, 0), (screenWidth / 2, screenHeight), 5)

        # Atualizando a janela 60fps
        pygame.display.flip()

        # Render Text
        # Opponent Score
        opponentScoreText = font.render(str(opponentScore), True, white)
        screen.blit(opponentScoreText, (screenWidth / 2 - 65, 50))
        # Player Score
        playerScoreText = font.render(str(playerScore), True, white)
        screen.blit(playerScoreText, (screenWidth / 2 + 40, 50))

    pygame.display.update()

def resetBall():
    global ballSpeedX, ballSpeedY
    ball.center = (screenWidth / 2, screenHeight / 2)
    ballSpeedX = random.choice((-1, 1))


def update(dt):
    global ballSpeedX, ballSpeedY, opponentScore, playerScore, onGameOverScreen, opponentSpeed

    ball.x += ballSpeedX * dt
    ball.y += ballSpeedY * dt

    # Opponent AI
    if opponent.bottom < ball.y and ball.x < screenWidth/2:
        opponent.y += opponentSpeed
    if opponent.top > ball.y and ball.x < screenWidth/2:
        opponent.y -= opponentSpeed

    # Bound
    if ball.top <= 0 or ball.bottom >= screenHeight:
        ballSpeedY *= -1

    # Score Marks
    if ball.left >= screenWidth:
        opponentScore += 1
        resetBall()
        Score_time = pygame.time.get_ticks()
        
    if ball.right <= 0:
        playerScore += 1
        resetBall()
        Score_time = pygame.time.get_ticks()

    # Game Over
    if playerScore == 10 or opponentScore == 10:
        pygame.quit()
        sys.exit()

    # Colision opponent and ball
    if ball.colliderect(opponent):
        ballSpeedX *= -1.0
    # Colision player and ball
    if ball.colliderect(player):
        ballSpeedX *= -1.0
    # Max Ball Speed
    if(ballSpeedX>1.0):
        ballSpeedX = 1.0


previous = pygame.time.get_ticks()
lag = 0
FPS = 500
MS_PER_UPDATE = 1000/FPS

while True:
    current = pygame.time.get_ticks()
    elapsed = current - previous
    previous = current
    lag += elapsed

    #Entradas
    inputs()
    while lag >= MS_PER_UPDATE:
        # Atualização
        update(MS_PER_UPDATE)
        lag -= MS_PER_UPDATE

    #Desenho
        draw()