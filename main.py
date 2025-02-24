import pyxel
from random import randint

#constantes
TITLE = "snake"
WIDTH = 200
HEIGHT = 160
CASE = 20
FRAME_REFRESH = 10

pyxel.init(WIDTH, HEIGHT, title=TITLE)

def reset_game():
    """
    Redémarre le jeu
    
    return: rien
    """
    global score, direction, snake, food, game_over, high_score
    score = 0
    direction = [1, 0]
    snake = [[3, 3], [2, 3], [1, 3]]
    food = [8,3]
    game_over = False
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())
        
reset_game()

def update_high_score():
    """
    Met à jour le high score
    
    return: rien    
    """
    global score, high_score
    if score > high_score:
        with open("high_score.txt", "w") as f:
            f.write(str(score))
            high_score = score

def draw():
    """
    Dessine les éléments à l’écran
    
    return: rien
    """
    #effacer puis remplir de noir l'écran
    pyxel.cls(0)
    
    #message de game over
    if game_over:
        pyxel.text(WIDTH // 2 - 20, HEIGHT // 2 - 15, "GAME OVER", 8)
        pyxel.text(WIDTH // 2 - 60, HEIGHT // 2, "Appuyez sur R pour recommencer", 7)
        return

    #dessiner le corps en vert
    for anneau in snake[1:]:
        x, y = anneau[0], anneau[1]
        #11 = couleur verte
        pyxel.rect(x * CASE, y * CASE, CASE, CASE, 11)
        
    #dessiner la tête en orange
    x_head, y_head = snake[0]
    #9 = couleur orange
    pyxel.rect(x_head * CASE, y_head * CASE, CASE, CASE, 9)
    
    #la nourriture
    x_food, y_food = food
    #8 = couleur rose
    pyxel.rect(x_food * CASE, y_food * CASE, CASE, CASE, 8)
    
    #score
    #7 = couleur blanche
    pyxel.text(4, 4, f"SCORE : {score}", 7)
    
    #high score
    pyxel.text(4, 12, f"HIGH SCORE : {high_score}", 7)

    
def update():
    """
    Met à jour l'état du jeu 30 fois par seconde
    
    return: rien
    """
    global direction, score, food, game_over
    
    if game_over:
        update_high_score()
        if pyxel.btn(pyxel.KEY_R):
            reset_game()
        return
    
    if pyxel.frame_count % FRAME_REFRESH == 0:
        #la nouvelle tête est l'ancienne, déplacée dans la direction
        head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        #on l'insère au début
        snake.insert(0, head)
        if head != food:
            snake.pop(-1)
        
        #mort du serpent?
        #s'il touche son corps ou s'il quitte l'écran
        if head in snake[1:]\
                or head[0] < 0\
                or head[0] > WIDTH/CASE - 1\
                or head[1] < 0\
                or head[1] > HEIGHT/CASE - 1:
            game_over = True
            
        #serpent mange la pomme?
        #si sa tête touche la pomme
        if head == food:
            score += 1
            update_high_score()
            while food in snake:
                food = [randint(0,WIDTH//CASE - 1),randint(0,HEIGHT//CASE - 1)]
        
    #on écoute les interactions du joueur (30x par seconde)
    if pyxel.btn(pyxel.KEY_ESCAPE):
        pyxel.quit()
    elif pyxel.btn(pyxel.KEY_RIGHT) and direction in ([0,1], [0, -1]):
        direction = [1,0]
    elif pyxel.btn(pyxel.KEY_LEFT) and direction in ([0,1], [0, -1]):
        direction = [-1,0]
    elif pyxel.btn(pyxel.KEY_UP) and direction in ([1,0], [-1, 0]):
        direction = [0,-1]
    elif pyxel.btn(pyxel.KEY_DOWN) and direction in ([1,0], [-1, 0]):
        direction = [0,1]

pyxel.run(update, draw)