import pygame
import random
import math
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)

Decisions = ['right','down','up','left','None'] # movement choices

wind = pygame.display.set_mode((500, 700)) #set the game window

direction = 1
Gen = []

len_gen = 500 #how many bots in a generation


#----------------------------------------------------------------------------------------

def distance(x1,y1,x2,y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

#----------------------------------------------------------------------------------------
'''

Collison detection between Bots and obstacles

'''
def Around(bot,circle):
    if (bot.x+15>=circle.x>=bot.x and bot.y+15>=circle.y>=bot.y):
        return True
    elif (bot.x+15>=circle.x+15>=bot.x and bot.y+15>=circle.y>=bot.y):
        return True
    elif (bot.x+15>=circle.x>=bot.x and bot.y+15>=circle.y+15>=bot.y):
        return True
    elif (bot.x+15>=circle.x+15>=bot.x and bot.y+15>=circle.y+15>=bot.y):
        return True
    else:
        return False

#----------------------------------------------------------------------------------------
   
class bot:

    def __init__(self,life,dna = None):
        if(dna == None):
            self.x = 235
            self.y = 680
            self.bot_moves = []
            self.hit = False
            self.fitness = 0
            self.life = life
            self.count = 0

            for i in range(self.life):
                Direction = random.choice(Decisions) #fills botmoves with random moves: right left up down
                self.bot_moves.append(Direction)
        else:
            self.x = 235
            self.y = 680
            self.bot_moves = dna
            self.hit = False
            self.fitness = 0
            self.life = life
            self.count = 0

            if(self.life > len(dna)): # if the previous generation reach a checkpoint then the new gen get more health but there dna isnt long enough
                                     #fix this by extending their dna by adding random movements to the end of it
                for i in range(self.life - len(dna)):
                    Direction = random.choice(Decisions)
                    self.bot_moves.append(Direction)
       
       
    def draw(self):
        colour = (255,0,0)
        
        pygame.draw.rect(wind,colour,(self.x,self.y,20,20))
    
    def move(self):
        if self.bot_moves[self.count] == "right":
            if(self.x + 2 < 480):
                self.x+=2
        elif self.bot_moves[self.count] == 'left':
            if(self.x - 2 > 20):
                self.x-=2
        elif self.bot_moves[self.count] == "up":
            if(self.y - 2 > 20):
                self.y-=2
        elif self.bot_moves[self.count] == "down":
            if(self.y + 2 < 680):
                self.y+=2
        else:
            pass


        self.draw()

#-----------------------------------------------------------------------------

class circle:
    def __init__(self,x,y,speed):
       self.x = x
       self.y = y
       self.speed = speed
    def draw(self):
        pygame.draw.ellipse(wind,(255, 0, 238),pygame.Rect(self.x,self.y,17,17))
    def slide(self):
        global direction

        self.x+=self.speed

        if(self.x + 20 >= 500):
            self.speed = self.speed*-1
        if(self.x - 20 <= 0):
            self.speed = self.speed*-1

        self.draw()


#---------------------------------------------------------------------------
'''
Makes bots for the next generation
(Gene_pool and life) == None at start of simulation

'''
        
def make_bots(Gene_pool = None,Life = None):

    if(Gene_pool == None):
        for i in range(len_gen):
            B = bot(1500)
            Gen.append(B)

    else:
        for i in range(len_gen):
            dna = []
            parent = random.choice(Gene_pool)

            for i in range(len(parent)):
                mutate = random.uniform(0,1)
                if(mutate > 0.99):
                    parent[i] = random.choice(Decisions) #mutates to choose random action
                dna.append(parent[i])


            B = bot(Life,dna)

            Gen.append(B)


#---------------------------------------------------------------------------
                   
def main():
    
    running = True
    Fps = 1000

    C = circle(20,505,1.25)
    C2 = circle(40,50,1)
    C3 = circle(25,574,1.25)
    C4 = circle(400,440,1)
    C5 = circle(25,550,0)
    C6 = circle(25,250,0.5)
    C7 = circle(20,350,1)
    make_bots()
    time = 1
    Num_gen = 1
    health = 1500
    curr_best_alltime = 1000 #arbitrary large number
    prev_best_alltime = 0
    spot = 0
    best_y = []
    

    while running:
        
        Avg_dist = 0
        Avg_y = 0
        Gene_pool = []
   
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Fps += 100
                if event.key == pygame.K_RIGHT:
                    Fps -= 100
            if event.type == pygame.QUIT:
                running = False
        
        wind.fill((255,255,255))


        for i in range(len(Gen)):

            if(Gen[i].hit == False): #if the bot isnt hit yet
                Gen[i].move() # does one move from the list of botmoves
                Gen[i].count+=1 #iterates threw the botmoves list, this insures the bots do one move per frame while they are alive
            
            if(Around(Gen[i],C) or Around(Gen[i],C2) or Around(Gen[i],C3) or Around(Gen[i],C4) or Around(Gen[i],C5) or Around(Gen[i],C6) or  Around(Gen[i],C7)): #collision detection
                Gen[i].hit = True
                
           
        if(time == Gen[0].life): #current Generation ended, code under here gives traits to new generation
            
            prev_best_alltime = curr_best_alltime

            for i in range(len(Gen)):
                Avg_dist = Avg_dist + Gen[i].fitness #calculating average distance
                Avg_y = Avg_y + Gen[i].y
                if(Gen[i].y < curr_best_alltime):
                    curr_best_alltime = Gen[i].y
                    spot = i

            if(Num_gen%5 == 0): #every 5 generations a health boost is given
                health+=100  
                 
            Avg_dist = Avg_dist/len_gen
            Avg_y = Avg_y/len_gen
            best_y.append(Avg_y)

            Avg_y = min(best_y)# considers the best all_time average as average 
            
            print("Avg_dist: ",Avg_dist, " | Avg y", Avg_y, "| best all time: ",curr_best_alltime," | Generation: ",Num_gen)
 
            for i in range(len(Gen)):

                Gen[i].fitness = 0
                Efficiency = round((1000/(Gen[i].y + Gen[i].count))*100) - 30 #determines how efficient bot was in getting to goal
                
                if(Avg_y - Gen[i].y > 0):#if it is closer to the goal than average
                    Gen[i].fitness += 15

                if(Avg_y - Gen[i].y > 5):#if it is 5 closer to the goal then average
                    Gen[i].fitness += 20
                   
                if(Avg_y - Gen[i].y > 15): # samething as above except 15
                    Gen[i].fitness += 25
                   
                if(Avg_y - Gen[i].y > 20):
                    Gen[i].fitness += 75
                
                if(Avg_y - Gen[i].y < 0): #if it is farther from the goal than average
                    Gen[i].fitness = 1

                if(Efficiency > 40):
                    Gen[i].fitness+=50

                for j in range(Gen[i].fitness):
                    Gene_pool.append(Gen[i].bot_moves) #appends the genes DNA the same amount as its fitness


            Num_gen+=1
            del Gen[:]
            make_bots(Gene_pool,health) #creates new bots, for next generation
	
            C = circle(20,505,1.25)
            C2 = circle(40,50,1)
            C3 = circle(25,574,1.25)
            C4 = circle(400,440,1)
            C5 = circle(25,550,0)
            C6 = circle(25,250,0.5)
            C7 = circle(20,350,1)
            time = 0


        textsurface = myfont.render('Speed: ' + str(Fps) + " - Life span: " + str(health) + " - Generation: " + str(Num_gen) + " - Health: " + str(health) , False, (0, 0, 0))

        #reset the obstacles back to original position     
        C.slide()
        C2.slide()
        C3.draw()
        C3.slide()
        C4.draw()
        C4.slide()
        C5.draw()
        C6.slide()
        C7.slide()
        
        pygame.draw.rect(wind,(0,255,0),(0,20,500,20))
        wind.blit(textsurface,(30,30))
         
        time+=1

        pygame.display.update()
        pygame.time.Clock().tick(Fps)
        
        
main()      


