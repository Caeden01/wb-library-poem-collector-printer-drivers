# West Bloomfield Library Poem Collector Driver Port For Adafruit Printers

**Warning:** This code is currently untested. May be unstable!! 

## Software Setup Instructions

1. Make sure your GPIO ports are enabled on your Pi:
    ```bash
    sudo raspi-config
    ```
   Go to Interface Options and then to I2c. Enable I2c by selecting Yes.

2. Install necessary packages:
    ```bash
    sudo apt-get update
    sudo apt-get install git cups wiringpi build-essential libcups2-dev libcupsimage2-dev python3-serial python-pil python-unidecode
    ```

3. Clone the repository:
    ```bash
    cd ~/
    git clone -b "Adafruit-Driver" https://github.com/Caeden01/wb-library-poem-collector-printer-drivers/
    cd ./wb-library-poem-collector-printer-drivers
    ```

4. Update the constants in "main.py"
    ```bash
    nano ./main.py
    ```
5. Create and edit the init script:
    ```bash
    sudo nano /etc/init.d/poem_project
    ```
    Add the following content:
    ```bash
   # Function to check if the service is running
   is_service_running() {
       pgrep -f "/usr/bin/python3 -- /home/$USER/wb-library-poem-collector-printer-drivers/main.py" >/dev/null
   }
   
   case "$1" in
     start)
       start_service
       ;;
     stop)
       stop_service
       ;;
     restart)
       stop_service
       sleep 1
       start_service
       ;;
     status)
       if is_service_running
       then
           echo "$NAME is running"
           exit 0
       else
           echo "$NAME is not running"
           exit 1
       fi
       ;;
     *)
       echo "Usage: $SCRIPTNAME {start|stop|restart|status}" >&2
       exit 3
       ;;
   esac
   
   # Continuous monitoring and restarting loop
   while true
   do
       sleep 1
       if ! is_service_running
       then
           echo "$NAME has exited unexpectedly, restarting..."
           start_service
       fi
   done
   
   exit 0
    ```

6. Make the script executable and set it to run at startup:
    ```bash
    sudo chmod +x /etc/init.d/poem_project
    sudo update-rc.d poem_project defaults
    sudo reboot
    ```


