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
screen = pygame.display.set_mode((320, 150))
done = False
font = pygame.font.SysFont("arial", 24)

# variables for stop button
stop_x = 10
stop_y = 10
stop_width = 50
stop_height = 100
stop_text = font.render("Quit", True, (255, 255, 255))

# variables for mark here button
here_x = 80
here_y = 10
here_width = 200
here_height = 100
here_text = font.render("Press Here to Record This Spot", True, (255, 255, 255))

def data_label(label):
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
    except KeyboardInterrupt:
		quit()
    except StopIteration:
		session = None
		print "GPSD has terminated"


is_stop_pressed = False

while not done:
    for event in pygame.event.get():
        # if window was closed, quit
        if event.type == pygame.QUIT:
            done = True
        # if stop button was pressed, quite
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if (x>stop_x and x<stop_x+stop_width and y>stop_y and y<stop_y+stop_height): 
                done = True
    
    # read in sensor data

    # draw stop button
    pygame.draw.rect(screen, (128, 12, 25), pygame.Rect(stop_x, stop_y, stop_width, stop_height))
    screen.blit(stop_text, (stop_x + 10, stop_y+50))

    # draw record here button
    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(here_x, here_y, stop_width, stop_height))
    screen.blit(here_text, (here_x, here_y))

    # now show everything on the screen
    pygame.display.flip()
