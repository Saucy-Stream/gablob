import pygame , sys
from pygame.locals import *

from math import sin, cos, tan, pi, atan as arctan, exp
from time import sleep, time
from random import uniform

class Misc():


   # varibles :
   window_width = 1240
   window_length = 800


   # arrays :
   population = [] # at the momment this array is not used , instead a hard coded array with the same name outside the class is used

   # report each frame
   def report(self,frame):
       # calculates combined mass
       blob_total_mass = 0
       for blob in population:

           blob_total_mass += blob.mass


       plant_total_mass = 0
       for plant in plant_pop:

           plant_total_mass += plant.mass


       total_mass = blob_total_mass + plant_total_mass
       biomass = 0
       for x in range(0,13):
           for y in range(0,8):
               biomass += ENV.chunks[x][y].biomass

       print("frame : ", frame, end = '')
       print("  blobs mass : ", int(blob_total_mass) / 1000, "k  plants mass : ", int(plant_total_mass) / 1000, "k  combined mass", int(total_mass) / 1000, "k", "combined biomass", int(biomass) / 1000, "k",end = '')
       print('')


class Colors:
   # colors are determend by the RGB pricipal, ranging from 0 to 255 [red,green,blue]
   black = [0,0,0]
   blue = [0,0,255]
   green = [0,128,0]
   lime = [0,255,0]
   teal = [0,128,128]


class Collision():


   def check_overlap(blob, plant_pop): # if blob is in eating distance of a plant, return index for plant

       eating = -1
       timer = 0
       for plant in plant_pop:


           dx = plant.x - blob.x
           dy = plant.y - blob.y


           distance = ((dx ** 2) + (dy ** 2)) ** 0.5
           total_r = blob.radius + plant.radius
           if distance < total_r / 2:
         
               eating = timer # gives the index of the plant to be eaten


           timer += 1

       return eating


   def check_sex(blob, mate):


       reproduction = "__false__"


       dx = mate.x - blob.x
       dy = mate.y - blob.y


       distance = ((dx ** 2) + (dy ** 2)) ** 0.5
       total_r = blob.radius + mate.radius
       if distance < total_r:
   
           reproduction = "__true__"


       return reproduction


class Ai():


   def hungry(self,blob):

       if blob.target_plant == 0:
           # tries to find food within a cetain radius
           timer = 0
           best_distance = blob.sight
           food = "__N/A__"
           for plant in plant_pop:


               dx = plant.x - blob.x
               dy = plant.y - blob.y


               distance = ((dx ** 2) + (dy ** 2)) ** 0.5


               if distance < best_distance:


                   best_distance = distance
                   food = timer


               timer += 1


           if food != "__N/A__":

               plant = plant_pop[food]
               blob.target_plant = plant

               dx = plant.x - blob.x
               dy = plant.y - blob.y


               alpha = arctan(dy/dx)


               if dx < 0:
               
                   alpha += pi

               blob.angle = pi/2 -alpha

           else:
               self.friend_search(blob)
       self.move(blob)

   def mate_search(self,blob):
       if blob.target_mate == 0:
           # tries to find love within a cetain radius
           timer = 0
           best_distance = blob.sight
           bride = "__N/A__"
           for partner in population:


               if partner is blob:
               
                   pass
               elif partner.ai_stance == "__mate_search__":


                   dx = partner.x - blob.x
                   dy = partner.y - blob.y


                   distance = ((dx ** 2) + (dy ** 2)) ** 0.5


                   if distance < best_distance:


                       best_distance = distance
                       bride = timer


               timer += 1


           #-----


           if bride != "__N/A__":


               partner = population[bride]
               blob.target_mate = partner


               dx = partner.x - blob.x
               dy = partner.y - blob.y

               alpha = arctan(dy/dx)


               if dx < 0:
               
                   alpha += pi

               blob.angle = pi/2 -alpha

           else:
               self.friend_search(blob)

       elif Collision.check_sex(blob, blob.target_mate) ==  "__true__":
           #child making
           blob.reproduce( blob.target_mate )


       self.move(blob)
    
   def friend_search(self, blob):
        timer = 0
        best_distance = blob.sight
        BFF = -1
        for friend in population:


           if friend is blob:
              
               pass
           
           else:

               dx = friend.x - blob.x
               dy = friend.y - blob.y


               distance = ((dx ** 2) + (dy ** 2)) ** 0.5


               if distance < best_distance:


                   best_distance = distance
                   BFF = timer

           timer += 1

        if BFF != -1:
            blob.angle = population[BFF].angle + uniform(-0.2,0.2)
        else:
            blob.angle += uniform(-0.2,0.2)

   def move(self,blob):
       blob.x += blob.velocity * sin( blob.angle )
       blob.y += blob.velocity * cos ( blob.angle )


class Blob():


   def __init__(self): # when created


       # varibles - standard
       self.x = uniform(0,float(Misc.window_width))
       self.y = uniform(0,float(Misc.window_length))
       self.mass = float(1000)
       self.energi_drain_konstant = float(0.001)
       self.radius = int( ( self.mass / pi ) ** 0.5 )
       self.velocity = float(1)
       self.angle = float(pi / 2)
       self.ai_stance = "__hungry__"
       
       self.children = 0
       self.timer = 0
       self.target_plant = 0
       self.target_mate = 0

       # genes
       self.minimal_mass = float(10) # minimal mass before death
       self.hungry_bias = float(500) # not yet used
       self.sight = float(300)
       self.agility = float(1) # not yet used
       self.reproduce_child_size = float(0.2) # perentage of mass given to child during birth
       #self.reproduce_maximal_mass = float(1500)
       self.mass_to_reproduce = float(1000)

   def update(self): # each frame


       self.mass -= self.children + self.energi_drain_konstant * ( (self.mass * self.velocity ** 2) / 2 ) # lowers mas depending on energy used to move
       self.radius = int( ( self.mass / pi ) ** 0.5 ) 
       self.velocity = 1000/(self.mass+500)
      
       # coalitions

       if self.timer % 3 == 0:
           self.timer = 0
           food = Collision.check_overlap(self, plant_pop)
           if food != -1:

               self.eat(plant_pop[food])




       # momment (ai)
       if self.ai_stance == "__hungry__":

           Ai().hungry(self)

       elif self.ai_stance == "__mate_search__":

           Ai().mate_search(self)
        
       self.timer += 1
          
   def reproduce(self, partner):
      
       # creates the child
       child = Blob()
       child.mass = self.mass * self.reproduce_child_size + partner.mass * partner.reproduce_child_size

       child.x = ( self.x + partner.x ) * 0.5
       child.y = ( self.y + partner.y ) * 0.5
       
       child.mass_to_reproduce = ( self.mass_to_reproduce + partner.mass_to_reproduce ) / 2 + uniform(-10,10)
       
       child.reproduce_child_size = (self.reproduce_child_size + partner.reproduce_child_size ) / 2 + uniform(-0.01,0.01)


       population.append( child )


       # removes mass from parents equal
       self.mass -= self.mass * self.reproduce_child_size
       partner.mass -= partner.mass * partner.reproduce_child_size

       #Adds child to both parents
       self.children += 1
       partner.children += 1

       # change ai stance for both partners
       self.refresh_stance()
       partner.refresh_stance()

       self.target_mate = 0
       partner.target_mate = 0

       for blob in population:
           if blob.target_mate == partner or blob.target_mate == self:
               blob.target_mate = 0
               return
  

   def refresh_stance(self): #changes behaviour depending on mass
        ratio = self.mass / self.mass_to_reproduce
        num = 2 / (1+exp(-ratio))-1
        if num > uniform(0,1):
            self.ai_stance = "__mate_search__"
            self.target_mate = 0
        else:
            self.ai_stance = "__hungry__"
            self.target_plant = 0

   def eat(self, plant):
       self.mass += plant.mass
       ENV.chunks[plant.chunk_x][plant.chunk_y].plants -= 1
       plant_pop.remove(plant)
       self.refresh_stance()
      
       for blob in population:
           if blob.target_plant == plant:
               blob.rarget_plant = 0
               return

   def draw(self, window): # draws a circle into the window


       pygame.draw.circle(window, Colors.teal, (int(self.x), int(self.y)), self.radius)
       

       #pygame.draw.circle(window, [255,255,255],(int(self.x),int(self.y)),int(self.sight),1)
       #Shows vision


class Plant():

    def __init__(self):

        self.x = uniform(0,float(Misc.window_width))
        self.y = uniform(0,float(Misc.window_length))
        self.mass = float(20)
        self.max_mass = float(1000)
        self.radius = int( ( self.mass / pi ) ** 0.5 )
        self.photosynthesis = float(10)
        self.children = 0

        self.chunk_x = 0
        self.chunk_y = 0

        self.minimal_mass = 10

        # possible toxicty
        # possible colors depending on other factors

        #genes
        self.seed_spread = uniform(0,150) # for reproduction
        self.mass_to_reproduce = float(750) 
        self.reproduce_child_size = float(0.2)

    def update(self):
        new_mass = self.photosynthesis * (1 - self.mass/self.max_mass) * ENV.chunks[self.chunk_x][self.chunk_y].biomass/1000 - self.children
        #calculates mass based on current mass, max mass, biomass in chunk and photosynthesis

        self.mass += new_mass #adds mass to plant

        ENV.chunks[self.chunk_x][self.chunk_y].biomass -= new_mass #removes mass from chunk

        self.radius = int( ( self.mass / pi ) **  0.5 )

        if self.mass > self.mass_to_reproduce:
            self.reproduce()


    def draw(self, window): # draws a circle into the window

        pygame.draw.circle(window, Colors.green, (int(self.x), int(self.y)), self.radius)


    def reproduce(self):
        angle = uniform(0,2*pi)
        sapling = Plant()
        sapling.mass = self.mass * self.reproduce_child_size 

        sapling.x = self.x + self.seed_spread * sin(angle)
        sapling.y = self.y + self.seed_spread * cos(angle)
        
        sapling.find_chunk(ENV)
        ENV.chunks[sapling.chunk_x][sapling.chunk_y].plants += 1

        #Copies genes to sapling (+ mutation)
        sapling.seed_spread = self.seed_spread * uniform(0.99,1.01)
        sapling.mass_to_reproduce = self.mass_to_reproduce * uniform(0.99,1.01)
        sapling.reproduce_child_size = self.reproduce_child_size * uniform(0.99,1.01)
        sapling.max_mass = self.max_mass * uniform( 0.99,1.01)

        self.mass -= sapling.mass + self.seed_spread/2
        plant_pop.append(sapling)

        self.children += 1


    def find_chunk(self, Environment):
        for x in range(0,13):
            for y in range(0,8):
                if self.x < Environment.chunks[x][y].x +100 and self.y < Environment.chunks[x][y].y+100:
                    self.chunk_x = x
                    self.chunk_y = y
                    return


class Chunk():

    def __init__(self):
        self.width = int(100)
        self.biomass = int(1000)
        self.max_biomass = int(10000)
        self.growth = int(3)
        self.x = 0
        self.y = 0
        self.color = pygame.Color(0,0,0)
        self.plants = 0

    def update(self):
        self.biomass += self.growth * (1 - self.biomass/self.max_biomass) - self.plants / 5

        #Update color to see biomass
        #self.color.g = int(255*self.biomass/self.max_biomass)
        
    def draw(self,window):
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width, self.width))


class Environment():


    def __init__(self):

        self.chunks = []
        for x in range(0,13): # window_length / chunk.width
            temp = []
            for y in range(0,8): # window_width / chunk.width
                TC = Chunk()
                TC.x = x*( TC.width )
                TC.y = y*( TC.width )
                temp.append(TC)
            self.chunks.append(temp)


    def update(self):
        pass
    
    # planned :
    # day and night cycle
    # summer and winter cycle
                          

class Visual():


   def __init__(self):


        pygame.init() # creates all the important event which we don't need to program ourself
        self.window = pygame.display.set_mode(( Misc().window_width , Misc().window_length )) # creates the window
        pygame.display.set_caption('Big Blob Stockholm') # the window title


        self.timer = 0 # for counting frames
        self.running = True


        while self.running == True: # infinite loop


            for event in pygame.event.get(): # this allows for the closing of the window by ending the loop


                if event.type == QUIT:


                    self.running = False


            self.window.fill(Colors.black) # clears the screen
            

            # prints the map on the surfece

            # uppdates and draws objects

            if self.timer % 60 == 0:
                PL = Plant()
                PL.find_chunk(ENV)
                plant_pop.append(PL)

            for x in range(0,13):
                for y in range(0,8):
                    ENV.chunks[x][y].update()
                    #ENV.chunks[x][y].draw(self.window)
            

            for plant in plant_pop:


                plant.update()
                if plant.mass < plant.minimal_mass:
                    ENV.chunks[plant.chunk_x][plant.chunk_y].plants -= 1
                    plant_pop.remove(plant)

                plant.draw(self.window)


            for blob in population:


                blob.update()
                if blob.mass < blob.minimal_mass:


                    population.remove(blob)


                blob.draw(self.window)
            
            
    
            pygame.display.update() # display the new frame


            Misc().report(self.timer)
            self.timer += 1
      #      sleep(0.0166)


        print("---end---")




# --- hardcode --- #
ENV = Environment()


plant_pop = [Plant()]
population = [Blob()]
for i in range(0,7):
    PL = Plant()
    PL.find_chunk(ENV)
    plant_pop.append(PL)

for i in range(0,4):
    population.append(Blob())

# --- -------- --- #


Visual() # start the game mode
pygame.quit() # exit properly (pygame)
sys.exit # exit properly (operating system)
