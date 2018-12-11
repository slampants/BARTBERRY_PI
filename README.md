# BARTBERRY_PI
Bartberry Pi

The Bartberry Pi is a random video player that uses only a single button for all functionality. It automatically loads a main splash screen, at which a button press starts a random video from the specified directory. During play, a button press stops play by killing the subprocess, and returns the viewer to the main splash screen.

One thing to note is that the photos I took of the GPIO connections was before I switched the button's reference pin from BCM pin 4 to BCM pin 21. The rest of the pin connections are accurate, providing 5V to the LED inside the button, ground to both the button and its switch, and 3.3V to the switch.

I've done my best to include references to people and links who helped me on the project in the initial comments of the BARTBERRY_PI.py codebase.

Video of the project in action can be viewed here:

https://youtu.be/i7_SVK5yjSQ
