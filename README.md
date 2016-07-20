# CiTIUS Invaders

An old-style arcade game to learn evolutionary algorithms and genetic programming. [Play here!](https://citiususc.github.io/citius-invaders/)

## About

This game was created to explain the basic concepts of evolution and genetic programming to college students. The game starts with 4 invaders that mate themselves. Each invader has different genes that codify their behavior, such as speed, probability of changing direction, size, color... During evolution time, the invaders start mating in order to create new invaders that inherit the attributes of their parents. Best invaders (invaders with higher fitness) have more probability to be selected for mating. The fitness of an invader corresponds with the number of evolutions that it has survived. This mechanism allows the invaders to improve their behavior against the player over time by learning the best set of features that allows them to survive.

## How to play

Controls are very easy. Just use left/right arrow to move your robot and space to shot. The goal is to keep the number of invaders below 100, otherwise the game is over. There are always at least 4 invaders (elitism), which are protected with blue shields. The player earns 1 point for each evolution time.

## Code

There are two versions of the game, a [python version](https://github.com/citiususc/citius-invaders/tree/master/python) and a [HTML5 version](https://github.com/citiususc/citius-invaders/tree/master/js) made with [Phaser](http://phaser.io/). You can play the HTML5 version here: https://citiususc.github.io/citius-invaders

## Authors

This game was made by [Tomás Teijeiro](https://github.com/tomas-teijeiro) and [Pablo Rodríguez Mier](https://github.com/pablormier) because why not?

The music was composed by the amazing Constantino Antonio García Fernández, who, despite being involved in thousands of projects and activities, still find time to help his friends with this stupid things.

## Screenshots

### Main menu
![Main menu](https://github.com/citiususc/citius-invaders/blob/2481bac3c424a95fbb782de329dceb0f059e9a09/screenshots/main-menu.png?raw=true)

### Game screen
![Game screen](https://github.com/citiususc/citius-invaders/blob/2481bac3c424a95fbb782de329dceb0f059e9a09/screenshots/game.png?raw=true)

## License 

    The MIT License
    
    Copyright (c) 2016 CiTIUS, USC. http://citius.usc.es
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
