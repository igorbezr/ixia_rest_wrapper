INTRODUCTION

This simple pet project has been created for simplification my own
daily work with IxNetwork REST API. Its overall purpose is to make
a high-level abstraction wrap around IxNetwork API without adding
additional complexity. Such complexity and demand of knowing internal
API subtle detail which ixnetwork_restpy has, make me really unhappy.

Now it is under development and may significantly change over time. 

Everyone, if anyone anywhere will give some attention to this, can do
all things with that code (like GNU license says). But there is also
absolutely no warranty that it at least work :)

INSTALLATION

1. Ensure that you have git and docker on your workstation.
2. Cloning this repo into appropriate location
    git clone https://github.com/igorbezr/ixia_rest_wrapper
3. Build Docker image
    docker build -t ixia_rest_wrapper .
4. Start demo script and view nice log in stdout 
    docker run -ti ixia_rest_wrapper demo.py
5. Have fun !
