# BMS-for-Electric-Vehicles-

#*******************************************************#

Creating a Docker container on DigitalOcean:
1.	Create a DigitalOcean account: If you haven't already, create an account on DigitalOcean.
2.	Create a droplet: Click on the "Create Droplet" button and select the droplet size, region, and operating system you want to use.
3.	SSH into the droplet: Once the droplet is created, you will receive an email with the IP address, username, and password. Use a tool like PuTTY or the built-in terminal to SSH into the droplet.
4.	Install Docker: Once you are logged into the droplet, install Docker by running the following command:
-	sudo apt-get update
-	sudo apt-get install docker.io
5.	Pull a Docker image: After Docker is installed, you can pull a Docker image by running the following command:   
-	sudo docker pull <ceaf6a38181d  >
6.	Run the Docker container: Finally, run the Docker container by running the following command:  
-	sudo docker run -d -p 80:80 <ceaf6a38181d>
7.	Here, “-d” flag runs the container in the background, “-p” flag maps the port 80 on the droplet to the port 80 on the container, and <CBBMS > is the name of the Docker image you pulled.
  
 #***************************************************************#

