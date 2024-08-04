# West Bloomfield Library Poem Collector Printer Drivers

Printer Driver compatible with GB01, GB02, GB03, GT01, YT01, MX05, MX06, MX08, or MX10 Bluetooth thermal printers for the WB Library Poem Collector Project - [Project Repository](https://github.com/Caeden01/West-Bloomfield-Library-Poem-Collector)

Built on the: [Cat-Printer](https://github.com/NaitLee/Cat-Printer)

## Hardware Setup Instructions:

Follow the tutorial videos for disassembly:
- [Video 1](https://www.youtube.com/watch?v=bvEZYjWYKA4)
- [Video 2](https://www.youtube.com/watch?v=4dRGZEcAp38)

1. Solder wires to places listed in the image below. Plug the + wire into Raspberry Pi 5V GPIO Pin and negative to ground.

![Image of soldering locations](https://github.com/user-attachments/assets/2ffd0a9f-59f3-4566-b947-0ddc70f2dc63)

2. Solder a wire to the place circled in the image below. Plug the wire into GPIO Port 3.

![Image of circled location](https://github.com/user-attachments/assets/ffb7413e-ea23-4426-9c5f-7e48e029d45a)

3. Obtain an LED light. Wire the + side of the LED light to GPIO Port 14. Negative can plug into any ground GPIO port.

4. Stuff the Raspberry PI under the printer circuit board and reassemble.

   ![Armature photo of assembly](https://github.com/user-attachments/assets/3afc05e9-4a82-406d-9a03-2057b6c1da55)

**Tip:** Covering solder connections in hot glue helps maintain the connectivity of the joints in the long term. 

**Warning:** With this setup, the Raspberry Pi will only boot up if the printer is connected to power through the USB-C port. Additionally, because the Raspberry Pi is connected to the printer's power button, the printer will refuse to power off if power is removed from USB-C. To address this, consider soldering a separate print button that is independent of the printer’s main power button. If this arrangement doesn't pose a problem for you, you can simply follow the steps above.

## Software Setup Instructions

1. Make sure your GPIO ports are enabled on your Pi:
    ```bash
    sudo raspi-config
    ```
   Go to Interface Options and then to I2c. Enable I2c by selecting Yes.

2. Install necessary packages:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pil bluez bluez-tools python3-bleak python3-gpiozero python3-requests
    ```

3. Clone the repository:
    ```bash
    git clone https://github.com/Caeden01/wb-library-poem-collector-printer-drivers
    cd ./wb-library-poem-collector-printer-drivers
    ```
4. Update the constants in "main.py"
    ```bash
    nano ./main.py
    ```
5. Get the directory path (copy this pls!!):
    ```bash
    pwd
    ```
   
6. Create and edit the init script:
    ```bash
    sudo nano /etc/init.d/thermal_print_project
    ```
   Add the following content:

    ```bash
    #!/bin/sh
    ### BEGIN INIT INFO
    # Provides:          thermal_print_project
    # Required-Start:    $remote_fs $syslog
    # Required-Stop:     $remote_fs $syslog
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: Start thermal print project at boot time
    # Description:       Enable service provided by thermal print project.
    ### END INIT INFO

    PATH=/sbin:/usr/sbin:/bin:/usr/bin
    DESC="Thermal Print Project"
    NAME=thermal_print_project
    DAEMON=/usr/bin/python3
    DAEMON_ARGS="FILE_DIRECTORY_PWD_GAVE_YOU/main.py"
    PIDFILE=/var/run/$NAME.pid
    SCRIPTNAME=/etc/init.d/$NAME

    # Function to start the service
    start_service() {
        echo "Starting $DESC"
        start-stop-daemon --start --background --make-pidfile --pidfile $PIDFILE --exec $DAEMON -- $DAEMON_ARGS
    }

    # Function to stop the service
    stop_service() {
        echo "Stopping $DESC"
        start-stop-daemon --stop --pidfile $PIDFILE
    }

    # Function to check if the service is running
    is_service_running() {
        pgrep -x "$NAME" >/dev/null
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

7. Make the script executable and set it to run at startup:
    ```bash
    sudo chmod +x /etc/init.d/thermal_print_project
    sudo update-rc.d thermal_print_project defaults
    sudo reboot
    ```

# Printer In Action

https://github.com/user-attachments/assets/f5096c9a-a69f-4cb5-ac02-a710ecd7a329

## TO DO

- [ ] Improve startup procedure - The script often crashes the first time it runs at boot.
- [ ] Enhance error message response system - Add more LED error codes for better diagnostics.
- [ ] Implement server-side error reporting - Enable direct reporting of error issues to the poem collector site.
- [ ] Rewrite in Rust or C++ for added speed efficiency. 
- [ ] Write drivers for other printers
