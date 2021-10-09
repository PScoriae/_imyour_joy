# This project has been deprecated in favor of the [Node.js rewrite](https://github.com/PScoriae/imyour_joy).

The discord.py implementation of this project has been deprecated since discord.py has ceased development. Its lead developer's announcement regarding the situation can be found [here](https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1).

The project will continue but will instead be using Node.js through the discord.js library. [Hikari](https://github.com/hikari-py/hikari), another Python library for the Discord API, was considered, however I have decided to rewrite the project in with discord.js due to its **speed**, **documentation** and my plans for **future projects**.

I was unsatisfied with the time it took for the bot to respond with images. The Node.js implementation has already proved to alleviate this issue since, presumably, it's because it's inherently faster than Python. Moreover, from what I've read and tried so far, discord.js' documentation and guide is far superior to discord.py's. Finally, I do have a future webapp project in mind, so migrating to JavaScript is certainly not a bad idea to improve my skills.

# imyour_joy_py

A simple Kpop discord.py bot.

In its current state, this is a Joy (Red Velvet) themed Discord bot that with features that appeal to Kpop fans.

You can simply clone this repository, configure it with your own credentials and deploy it.

The suggested method of deployment is through the use of Docker containers. Furthermore, a privately hosted registry for the Docker image is strongly recommended since the image contains the key to your bot.

## Commands

| Syntax         | Description                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------- |
| `jpic {name}`  | Returns a randomly chosen image of the person/thing from kpop.asiachan.com.                       |
| `jprof {name}` | Returns an embed with a picture and short description of the GG, BG or member from kprofiles.com. |
| `jgit`         | Links to this GitHub repo.                                                                        |
| `jhello`       | Links to Joy's Hello music video.                                                                 |

**Note:** In actual use, name arguments should **not** be enclosed in curly brackets. They are only presented here to demonstrate the syntax.

# Installation and Configuration

## Installation

In your desired location, simply run the following in the terminal:

    $ git clone https://github.com/PScoriae/imyour_joy_py

## Configuration

If you have a look at the `.gitignore` file, you'll notice that `token.txt` has been excluded so that my bot's token isn't publicized.

Hence, the first step is to create a file called `token.txt` in the root directory. Then, simply paste your bot's token in the file.

If you choose to deploy this bot using Docker, that's all the setup that's needed! `docker build` will take care of the rest.

However, if you wish to run the bot outside of Docker, see [Running the Bot Outside of Docker](##running-the-bot-outside-of-docker)

# Deployment

These instructions and the included script are meant for *nix based systems. However, the deployment process can be replicated on Windows systems provided you understand the intents behind these actions and adjust them accordingly.

## Running the Bot Outside of Docker

You'll need to install some libraries with `pip`:

    $ pip install discord.py beautifulsoup4 requests lxml

Then, simply run the `bot.py`

    $ python bot.py

That's all you need to do. The instructions below are for deploying it to a server hosting a private registry.

## Setting Up A Private Registry

These instructions are largely based on the [official guide](https://docs.docker.com/registry/).

1.  On the server, pull the official registry image.
        
        $ docker pull registry

2.  Run the image in detached mode and open it on your preferred ports.
        
        $ docker run -d -p 5000:5000 --name registry registry

## Creating and Pushing the Docker Image

Special thanks to botjtib for providing a [solution](https://stackoverflow.com/questions/38695515/can-not-pull-push-images-after-update-docker-to-1-12) for pushing to a private regisry.

1. On the computer that will push the Docker image, ensure your server's IP:port is added as an insecure registry to `/etc/docker/daemon.json`. Its contents should include a line like this:

        {"insecure-registries":["192.168.0.154:5000"]}

2. Restart the Docker daemon.

        $ sudo systemctl restart docker

3. Edit `docker.sh`'s variables to fit your needs.

4. Run `docker.sh` to automatically **build**, **tag** and **push** the image to your private registry.

## Deploying the Image

1. On your server, pull the image from your registry.

        $ docker pull localhost:5000/imyourjoy

2. Finally, run the image in detached mode.

        $ docker run -d imyourjoy

# Enjoy

Thanks for reading and I hope you enjoy the bot!
