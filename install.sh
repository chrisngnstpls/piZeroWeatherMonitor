#!/bin/bash

echo -e "Make sure you have everything installed as described \n\nhere\n\n:https://github.com/pimoroni/bme680-python\n\nand\n\nhttps://shop.pimoroni.com/products/1-12-oled-breakout?variant=12628508704851"
read -n 1 -r -p "Press 'y' to continue or any key to exit..." key

if [ "$key" = 'y' ]; then
    # Space pressed, do something
	echo -e "\nInstalling dependencies...\n"
	pip3 install pandas
	pip3 install glob3
else
	echo -e "\nExiting...\n"
fi
