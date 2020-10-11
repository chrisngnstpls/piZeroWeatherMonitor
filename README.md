# piZeroWeatherMonitor
Small python script will work with the 1.12'' OLED display from pimoroni.com and the bme680 sensor also from pimoroni.com

check out all the necessary installs @ https://shop.pimoroni.com/products/1-12-oled-breakout?variant=12628508704851

and 

@ https://github.com/pimoroni/bme680-python

the install script installs pandas & glob3.

the measurement data is kept in the /data folder and is in .csv format
utils.py contains plotting tools for the data but you still have to call it independently. 
images produced from the plotting will be placed in the /images directory

there's a 5 minute heat-up time before the any actual measurement takes place.

cmdline.txt contains the command line with all the arguments needed to run the script. 

