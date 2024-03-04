
import time
import matplotlib.pyplot as plt
import math
import random

class DVDLogo:
    
    def __init__(self, width, height, box_width, box_height, x0, y0, vx, vy) -> None: # Constructor.
        # This is needed, because if we didn't have this, then with box_width = 1 would actually be two spots wide.
        box_height -= 1
        box_width -= 1
        assert box_height >= 0
        assert box_width >= 0
        # These are the area width and height
        self.width = width
        self.height = height
        # These are the width and height of the actual dvd logo.
        self.box_width = box_width
        self.box_height = box_height

        # Sanity checking. The total erea must be smaller than the dvd logo
        assert self.width >= self.box_width
        assert self.height >= self.box_height 

        self.x0 = x0
        self.y0 = y0
        self.vx = vx
        self.vy = vy
        # This is the actual current position.
        self.x = x0
        self.y = y0

        # This is needed to make the plot interactive
        plt.ion()
    def check_coords(self) -> None: # This updates the stuff when we are about to go over the line.
        # First check for negative shit.
        box_right = self.x + self.box_width # This is the x coordinate of the right side of the box
        if self.x < 0: # Can not go negative. This is the left side.
            over_amount = abs(self.x) # How much do we go over?
            self.vx *= -1 # Bounce.
            self.x = over_amount # If we are just beside the wall, and we go towards the wall three units, then go backwards three units.
        elif box_right >= self.width:
            # Same thing.
            over_amount = (box_right)  - self.width + 1 # + 1 , because reasons.
            print("over_amount == "+str(over_amount))
            self.vx *= -1
            #self.x = self.width - over_amount
            self.x = self.x - over_amount - 1 # - 1 , because shit reasons
        #return
        # Now check the y shit.
        box_bottom = self.y + self.box_height
        if self.y < 0: # Can not go negative.
            over_amount = abs(self.y) # We went over by this amount.
            self.y = over_amount
            self.vy *= -1
        elif box_bottom >= self.height:
            over_amount = (box_bottom)  - self.height + 1
            self.vy *= -1
            self.y = self.y - over_amount - 1 # - 1 , because shit reasons
        return
    def update(self) -> None:
        # Goes forward in time for one unit of time (one time step)
        # Update position.
        self.x += self.vx
        self.y += self.vy
        # Check for x and y collision.
        self.check_coords()
    def to_bool_mat(self) -> None: # This returns a boolean matrix which is then rendered.
        matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        # Now draw the box.
        for y in range(self.y, self.y+self.box_height+1): # Go over each line.
            for x in range(self.x, self.x+self.box_width+1): # Go over each fucking shit.
                matrix[y][x] = 1 # Set as one.
        matrix = list(reversed(matrix)) # This is to make the y coordinate increment UPWARDS not downwards.
        return matrix
    def render(self) -> None:
        render_mat = self.to_bool_mat()
        plt.imshow(render_mat, cmap="gray")
        plt.show()
        plt.pause(0.01)
        plt.clf()
    def check_winning(self) -> bool: # This checks if the box is in the corner. We need to take into account that the velocity is greater than one. (We advance multiple spots.)
        pos = (self.x, self.y)
        winning_positions = [(0,0), (self.width - self.box_width - 1, self.height - self.box_height - 1), (0, self.height - self.box_height - 1), (self.width - self.box_width - 1, 0)]
        return pos in winning_positions


# This next function checks if the logo will actually hit the corner or not.

def check_satisfiability(width, height, box_width, box_height, x0, y0, vx, vy) -> bool: # This checks if the box will hit the corner.
    a = x0
    b = y0
    x = width
    y = height
    if vx >= 0:
        # x * k1 + y * k2 = a - b
        z = a - b
        # Diophantine equation solving.
        # Let x, y and z be integers.
        # Then if z is a multiple of gcd(x,y) in x * k1 + y * k2 = z , then a solution exists.
        #print("math.gcd(x,y) == "+str(math.gcd(x,y)))
        #print("z == "+str(z))
        if z % math.gcd(x,y) == 0:
            return True
    else:
        z = a + b
        if z % math.gcd(x,y) == 0:
            return True
    return False # Otherwise no solution.


#def cur_pos(t, width, height, x0, y0, vx, vy, box_width, box_height) -> tuple: # Returns the position after t time steps.

DELAY = 0.1

def main() -> int:

    area_width = 10
    area_height = 10
    x0 = 1
    y0 = 2
    vx = 1
    #vy = -1
    vy = 1
    box_width = 1
    box_height = 1

    # __init__(self, width, height, box_width, box_height, x0, y0, vx, vy)
    # check_satisfiability(width, height, box_width, box_height, x0, y0, vx, vy)

    # First just check the solution shit.


    sol = True

    sol = check_satisfiability(12, 8, 1, 1, 5, 3, 1, 1) # This should return us false.
    print("Here is sol: "+str(sol))
    assert sol == False # Sanity checking.
    
    #return

    sol = True
    
    '''
    while sol:
        # Generate new velocities.
        if area_width <= 0:
            area_width = 10
        if area_height <= 0:
            area_height = 10
        vx = random.randrange(0,area_width)
        vy = random.randrange(0,area_height)
        print("vx: "+str(vx))
        print("vy: "+str(vy))
        area_width = random.randrange(vx, vx+10)
        area_height = random.randrange(vy, vy+10)
        sol = check_satisfiability(area_width, area_height, box_width, box_height, x0, y0, vx, vy)

    '''


    
    #print("Here is the solution: "+str(sol))

    #print("Here is a start velocity which is not solvable: ")
    #print("v0 == "+str(vx))
    #print("vy == "+str(vy))
    #return

    logo = DVDLogo(area_width, area_height, box_width, box_height, x0, y0, vx, vy) # Create the object.
    # main loop
    while True:
        logo.render()
        logo.update()
        print("Here is the x coordinate: "+str(logo.x))
        time.sleep(DELAY)
        if logo.check_winning(): # Check if win
            print("Finished!")
            break

    return 0

if __name__=="__main__":
    exit(main())
