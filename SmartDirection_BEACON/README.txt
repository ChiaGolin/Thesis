README SMARTDIRECTION_BEACON

Indoor navigation system able to help the user to arrive at a final destination. The directions are projected in the environment thanks to projectors. Beacon has to be carried as a smart bracalet or necklace to not cover its advertising messages

- Required packages:
	- sys
	- queue
	- datetime
	- keyboard
	- time
	- threading
	- paho.mqtt.client
	- bluez
	- json
	- pygame


- At the initialization of each raspberry it is required to set the name of it (my_MAIN.py). According the name there are different directions on xml map

- The user broker is provided by AWS 
	
- It is required a script that sends MQTT publish to start the system (prova3.py symulates Totem functions)--> wait 30 seconds before send the MQTT messagege (required display initialization time)
	
- The script will open the screen in fullscreen since the beginning. Press Z for closing the screen (after 30 seconds)

- Sometimes the bluetooth goes down, before restarting the execution run on comman prompt--> sudo hciconfig hci0 down && sudo hciconfig hci0 up 


Procedure to start the script at the raspberry opening:
	- open command prompt
	- digit: sudo crontab -e
	- add at the end of the file: @reboot sleep 10 && cd /pathDirectory && sudo python3 my_MAIN.py --->(substitute pathDirectory with the path of the smartDirection_Beacon folder


