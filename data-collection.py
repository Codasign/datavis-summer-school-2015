#!/usr/bin/python
import pygame, csv, time
import gps
import HTU21DF as htu

# start gps by listening on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


# open csv files
current_datetime = time.strftime("%Y-%m-%d-%H-%M-%S")
filename = current_datetime +'-locations.csv'
locations_csv = open(filename, 'wb')
locations_writer = csv.writer(locations_csv)

filename = time.strftime("%Y-%m-%d-%H-%M-%S")+'-path.csv'
path_csv = open(filename, 'wb')
path_writer = csv.writer(path_csv)

# set up window
pygame.init()
screen = pygame.display.set_mode((320, 180))
done = False
font = pygame.font.SysFont("arial", 24)
font_small = pygame.font.SysFont("arial", 16)

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
group_text = font.render("Group Orange", True, (255, 255, 255) )
here_text_1 = font.render("Touch Here to Record", True, (255, 255, 255))

# other variables
current_location = 1
date_time = ''
lat = 0.0
lon = 0.0
temp = 0.0
humid = 0.0

# note the current location and sensor data
# for the locations csv file
def record_here():
    global current_location, date_time, lat, lon, temp, humid
    locations_writer.writerow([current_location, date_time, lat, lon, temp, humid])
    current_location+=1

def read_sensors():
    global session, date_time, lat, lon, temp, humid
    try:
        report = session.next()
        # Wait for a 'TPV' report and display the current time
        # To see all report data, uncomment the line below
        if report['class'] == 'TPV':
            if hasattr(report, 'time'):
                #print 'time\t\t', report.time
                date_time = report.time
            if hasattr(report, 'lat'):
                #print 'latitude\t', report.lat
                lat = report.lat
            if hasattr(report, 'lon'):
                #print 'longitude\t', report.lon
                lon = report.lon
            #print 'temperature\t', htu.read_temperature()
            #print 'humidity\t', htu.read_humidity()
            temp = htu.read_temperature()
            humid = htu.read_humidity()
            path_writer.writerow([date_time, lat, lon, temp, humid])
    
    except KeyError:
        pass
    except StopIteration:
        session = None
        print "GPSD has terminated"

# other variables
is_stop_pressed = False


while not done:
    # read in sensor data
    read_sensors()
       
    for event in pygame.event.get():
        # if window was closed, quit
        if event.type == pygame.QUIT:
            locations_csv.close()
            path_csv_close()
            done = True
        # if mouse was pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
           # if stop button was pressed, quit
            if (x>stop_x and x<stop_x+stop_width and y>stop_y and y<stop_y+stop_height): 
                locations_csv.close()
                path_csv.close()
                done = True
            # if record button was pressed
            if(x>here_x and x<here_x+here_width and y>here_y and y<here_y+here_height):
                record_here()
                print "record"
   

    # draw stop button
    pygame.draw.rect(screen, (128, 12, 25), pygame.Rect(stop_x, stop_y, stop_width, stop_height))
    screen.blit(stop_text, (stop_x+4, stop_y+70))

    # draw record here button
    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(here_x, here_y, here_width, stop_height))
    screen.blit(group_text, (here_x+3, here_y+5))
    screen.blit(here_text_1, (here_x+3, here_y+30))
    here_text_2 = font.render("Location  "+ str(current_location), True, (255, 255, 255))
    screen.blit(here_text_2, (here_x+40, here_y+57))
    lat_text = font_small.render("%.4f latitude" %(lat), True, (255, 255, 255))
    screen.blit(lat_text, (here_x+40, here_y+80))
    lon_text = font_small.render("%.4f longitude" %(lon), True, (255, 255, 255))
    screen.blit(lon_text, (here_x+40, here_y+95))
    temp_text = font_small.render("%.2f degrees" %(temp), True, (255, 255, 255))
    screen.blit(temp_text, (here_x+40, here_y+110))
    humid_text = font_small.render("%.2f%% humidity" %(humid), True, (255, 255, 255))
    screen.blit(humid_text, (here_x+40, here_y+125))    

    # now show everything on the screen
    pygame.display.flip()
