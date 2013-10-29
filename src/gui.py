"""
    Implements a custom version of box that draws the
    cities and journey
"""

from fltk import *
from Cities import Cities
from Population import Population
from random import Random
from threading import Lock
from thread import start_new_thread
from time import sleep

width = 500
height = 500

class TSPCanvas(Fl_Box):

    def __init__(self, gui, x, y, w, h):
        
        Fl_Box.__init__(self, x, y, w, h)
    
        # style the widget
        self.box(FL_DOWN_BOX)
        self.color(FL_WHITE)
    
        # save needed attribs
        self.gui = gui
        self.pop = gui.pop
    
        # best fitness so far
        self.bestSoFar = 10000000000000000000
    
    def draw(self):
        
        Fl_Box.draw(self)
        
        # now, show the cities and plot their journey
        self.showJourney()
    
    #Periodically shows the best journey
    def showJourney(self, *ev):
        
        self.gui.lock.acquire()
    
        # get the best
        best = self.gui.best
        
    
        fitness = self.gui.fitness
    
        cityList = self.gui.cities.getCities()
    
        # draw the city names
        fl_color(FL_BLACK)
        for city in cityList:
            fl_draw(city.getName(), int(city.getLocation()[0]), int(city.getLocation()[1]))
            fl_rectf(int(city.getLocation()[0])-5,int(city.getLocation()[1])-5 ,5,5,0,0,0)      
    
        print "best=%s" % fitness
   
        # choose a colour according to whether we're improving, staying the same,
        # or getting worse
        if fitness < self.bestSoFar:
            fl_color(FL_GREEN)
            self.bestSoFar = fitness
        elif fitness == self.bestSoFar:
            # equal best - plot in blue
            fl_color(FL_BLUE)
        else:
            # worse - plot in red
            fl_color(FL_RED)
        
        # get the cities in order
        order = best.getCityTour()
        lastCity = 0
        nextCity = order[0].getConnection1()
        
        #draw the line connecting the city.
        for city in xrange(len(cityList)):
            fl_line(int(cityList[lastCity].getLocation()[0])-5, int(cityList[lastCity].getLocation()[1])-5, 
                    int(cityList[nextCity].getLocation()[0])-5, int(cityList[nextCity].getLocation()[1])-5)
            
            #figure out if the next city in the list is [0] or [1]
            if lastCity != order[nextCity].getConnection1():
                lastCity = nextCity
                nextCity = order[nextCity].getConnection1()
            else:
                lastCity = nextCity
                nextCity = order[nextCity].getConnection2()
    
        self.gui.lock.release()



"""
Implementation of the travelling salesman problem (TSP)
"""


class TspGui(object):
    
    x = 100
    y = 100
    w = width + 10
    h = height + 50
    
    updatePeriod = 0.1
    
    #Creates the graphical interface
    def __init__(self,numberOfCities=20,populationSize=100,groupSize=5, mutation_rate= 0.03, maxGenerations=1000,chancesCloseCities=0.90,closeCities=5):
        
        #Creates the initial empty population
        print "Initializing the population"
        self.cities = Cities(numberOfCities)
        self.cities.calculateCityDistances(closeCities)
        self.pop = Population()
        self.maxGenerations = maxGenerations
        self.mutation_rate = mutation_rate
        self.groupSize = groupSize
        self.pop.createRandomPopulation(populationSize,self.cities, Random(),chancesCloseCities)
        self.best = self.pop.getBestTour()
        
        self.updated = True
        
        # lock for drawing
        self.lock = Lock()

        # build the gui
        self.win = Fl_Window(
            self.x, self.y,
            self.w, self.h,
            "PyTravelling Salesman solver v0.1")

        self.xdraw = 5
        self.ydraw = 5
        self.wdraw = self.w - 10
        self.hdraw = self.h - 90
        
        # bring in our custom canvas
        self.draw_canvas = TSPCanvas(
            self,
            self.xdraw, self.ydraw,
            self.wdraw, self.hdraw,
            )
        
        # add in some fields
        self.fld_numgen = Fl_Output(120, self.h-84, 50, 20, "Generations: ")
        self.fld_numimp = Fl_Output(320, self.h-84, 50, 20, "Improvements: ")
        
        # add a chart widget
        self.chart = Fl_Chart(5, self.h - 60, self.w - 10, 60)
        self.chart.color(FL_WHITE)
        self.chart.type(FL_LINE_CHART)
        self.win.end()
        
        # this flag allows for original generation to be displayed
        self.firsttime = True
        self.fitness = self.pop.getBestTour().getFitness()
        
        self.ngens = 0
        self.nimp = 0
        self.bestFitness = 9999999999999999999
    
    #Runs the population    
    def run(self):
        
        # put up the window
        self.win.show()
    
        # start the background thread
        start_new_thread(self.threadUpdate, ())
    
        # schedule periodical updates
        Fl.add_idle(self.update)
    
        # hit the event loop
        Fl.run()
    
    #Checks for updates
    def update(self, *args):
        # and let the thread run
        sleep(0.0001)
    
        if self.updated:
    
            self.lock.acquire()
    
            # now draw the current state
            self.draw_canvas.redraw()    
            
            # plot progress on graph
            self.chart.add(self.fitness)
            
            # update status fields
            self.ngens += 1
            self.fld_numgen.value(str(self.ngens))
                
            if self.fitness < self.bestFitness:
                self.nimp += 1
                self.fld_numimp.value(str(self.nimp))
                self.bestFitness = self.fitness
    
            self.updated = False
            
            self.lock.release()
            
    #Create and display generation.        
    def threadUpdate(self):
        print "threadUpdate starting"
    
        while True:
    
            self.pop.makeChildren(self.groupSize,self.mutation_rate,self.cities,Random())
    
            print "generated"
    
            self.lock.acquire()
    
            self.best = self.pop.getBestTour()
            self.fitness = self.best.getFitness()
            self.updated = True
            self.lock.release()
            
            if self.ngens >= self.maxGenerations:
                break
        
    

#########################################################
def main():
    
    # build and run the gui    
    gui = TspGui(populationSize=10000,maxGenerations=10000,numberOfCities=20)

    gui.run()

if __name__ == '__main__':
    main()

