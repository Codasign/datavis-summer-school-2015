import pygame
import gps
import HTU21DF as htu

# start gps by listening on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


# read in and display temperature
def read_temp():
    t = htu.read_temperature()


# set up window
pygame.init()
screen = pygame.display.set_mode((320, 180))
done = False
font = pygame.font.SysFont("arial", 24)

# variables for stop button
stop_x = 10
stop_y = 10
stop_width = 55
stop_height = 160
stop_text = font.render("Quit", True, (255, 255, 255))

# variables for mark here button
here_x = 75
here_y = 10
here_width = 240
here_height = 160
here_text_1 = font.render("Touch Here to Record", True, (255, 255, 255))

# other variables
current_location = 1

# note the current location and sensor data
# for the locations csv file
def record_here():
    global current_location
    current_location+=1


def read_sensors():
    global session
    try:
        report = session.next()
        # Wait for a 'TPV' report and display the current time
        # To see all report data, uncomment the line below
        if report['class'] == 'TPV':
            if hasattr(report, 'time'):
                print 'time\t\t', report.time
            if hasattr(report, 'lat'):
                print 'latitude\t', report.lat
            if hasattr(report, 'lon'):
                print 'longitude\t', report.lon
            print 'temperature\t', htu.read_temperature()
            print 'humidity\t', htu.read_humidity()
    
    except KeyError:
        pass
    except StopIteration:
        session = None
        print "GPSD has terminated"

# other variables
is_stop_pressed = False


while not done:
    for event in pygame.event.get():
        # if window was closed, quit
        if event.type == pygame.QUIT:
            done = True
        # if mouse was pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
           # if stop button was pressed, quit
            if (x>stop_x and x<stop_x+stop_width and y>stop_y and y<stop_y+stop_height): 
                done = True
            # if record button was pressed
            if(x>here_x and x<here_x+here_width and y>here_y and y<here_y+here_height):
                record_here()
                print "record"
    
    # read in sensor data
    read_sensors()

    # draw stop button
    pygame.draw.rect(screen, (128, 12, 25), pygame.Rect(stop_x, stop_y, stop_width, stop_height))
    screen.blit(stop_text, (stop_x+4, stop_y+70))

    # draw record here button
    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(here_x, here_y, here_width, stop_height))
    screen.blit(here_text_1, (here_x+3, here_y+50))
    here_text_2 = font.render("Location  "+ str(current_location), True, (255, 255, 255))
    screen.blit(here_text_2, (here_x+20, here_y+77))
    
    # now show everything on the screen
    pygame.display.flip()
