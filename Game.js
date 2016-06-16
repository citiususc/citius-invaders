// Game global config vars [MOVE TO SETTINGS]

var WALL_MARGIN = 80;
var DIR_CHANGE_MIN_TIME = 10;
var SHOOT_DELAY = 100;
var MIN_INVADERS = 4;
var INITIAL_INVADERS = 6;
var MIN_GENERATION_TIME = Phaser.Timer.SECOND * 2;


invadersApp.Game = function (game) {
    
    // Auto-injected properties

    this.game;      //  a reference to the currently running game (Phaser.Game)
    this.add;       //  used to add sprites, text, groups, etc (Phaser.GameObjectFactory)
    this.camera;    //  a reference to the game camera (Phaser.Camera)
    this.cache;     //  the game cache (Phaser.Cache)
    this.input;     //  the global input manager. You can access this.input.keyboard, this.input.mouse, as well from it. (Phaser.Input)
    this.load;      //  for preloading assets (Phaser.Loader)
    this.math;      //  lots of useful common math operations (Phaser.Math)
    this.sound;     //  the sound manager - add a sound, play one, set-up markers, etc (Phaser.SoundManager)
    this.stage;     //  the game stage (Phaser.Stage)
    this.time;      //  the clock (Phaser.Time)
    this.tweens;    //  the tween manager (Phaser.TweenManager)
    this.state;     //  the state manager (Phaser.StateManager)
    this.world;     //  the game world (Phaser.World)
    this.particles; //  the particle manager (Phaser.Particles)
    this.physics;   //  the physics manager (Phaser.Physics)
    this.rnd;       //  the repeatable random number generator (Phaser.RandomDataGenerator)

    // Stores the reference to game elements
    this.objects = {};
    this.settings;

    this.player;
    this.bullets;
    this.cursors;
    this.fireButton;

    this.lastShootAt = 0;
    this.readyToFire = true;
};

invadersApp.Game.prototype = {

    create: function () {

        var that = this;

        this.currentGenerationTime = Phaser.Timer.SECOND * 5;
        this.currentGeneration = 0;
        this.lastGenerationTime = this.game.time.now;

        // Load game config
        this.settings = this.game.cache.getJSON('settings');

        // Initialize basic physics
        this.game.physics.startSystem(Phaser.Physics.ARCADE);

        // Group of invaders
        this.objects.invaders = this.add.group();
        this.objects.invaders.enableBody = true;
        this.objects.invaders.physicsBodyType = Phaser.Physics.ARCADE;
        for (var i = 0; i < INITIAL_INVADERS; i++) this.objects.invaders.add(new invadersApp.Invader(this));

        // Create and add the main player
        this.player = new invadersApp.Player(this);
        this.game.add.existing(this.player);

        // Create a white, immovable wall with physics enabled
        this.createWall();

        this.cursors = this.game.input.keyboard.createCursorKeys();
        this.fireButton = this.game.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);


        // New generation event, check for every second
        this.game.time.events.loop(Phaser.Timer.SECOND, this.createGeneration, this);


        // Gargabe collect killed invaders. If the invaders are
        // destroyed on a bullet hit, it may produce an exception
        // from physics module if there is a concurrent collision
        // detection going on
        this.game.time.events.loop(Phaser.Timer.SECOND * 5, function () {
            this.objects.invaders.forEachDead(function (invader) {
                invader.destroy();
            }, this);
        }, this);


        // Start the game paused with the message READY!
        var readyText = invadersApp.utils.addText(this, this.game.width / 2, this.game.height / 2, 'READY!', 5);
        this.game.input.keyboard.onDownCallback = function () {
            that.game.paused = false;
            if (readyText.visible) readyText.kill();
        };
        this.game.paused = true;
    },

    update: function () {

        var that = this;

        // If physics are paused, skip all
        if (this.game.physics.arcade.isPaused) return;

        this.game.physics.arcade.collide(this.wall, this.objects.invaders);
        this.game.physics.arcade.overlap(this.player.bullets, this.objects.invaders, function (bullet, invader) {
            bullet.kill();
            var living = that.objects.invaders.countLiving();
            if (living > MIN_INVADERS) invader.kill();
            if (living == MIN_INVADERS + 1) {
                that.objects.invaders.forEachAlive(function (invader) {
                    invader.showField();
                }, that);
            }
        }, null, this);
    },

    quitGame: function (pointer) {

        //  TODO: Stop music, delete sprites, purge caches, free resources...

        //  Then let's go back to the main menu.
        this.state.start('MainMenu');

    },

    pausePhysics: function (pause) {
        if (pause == undefined) pause = true;
        this.game.physics.arcade.isPaused = pause;
    },
    
    createGeneration: function () {
        var that = this;

        if (this.game.time.now > this.lastGenerationTime + this.currentGenerationTime) {
            this.lastGenerationTime = this.game.time.now;

            // The number of invaders
            var alive = this.objects.invaders.countLiving();

            var aliveInvaders = this.objects.invaders.filter(function(child, index, children) {
                return child.alive;
            }, true);

            aliveInvaders.callAll('increaseFitness');

            // The number of new individuals is determined by a box-cox
            // transformation with lambda=0.6.
            var numPairs = Math.floor((Math.pow(alive, 0.6) - 1) / 0.6);
            
            var pool = invadersApp.evolution.pool(aliveInvaders.list, numPairs);
            var offspring = invadersApp.evolution.evolve(pool, this.settings.genes);

            // Start an animation

            // Draw a line https://codepen.io/codevinsky/pen/dAjDp
            offspring.forEach(function (p) {
                var x = (p[0].x + p[1].x)/2;
                var y = (p[0].y + p[1].y)/2;
                that.objects.invaders.add(new invadersApp.Invader(that, p[2], x, y));
            });

            this.currentGeneration++;

            // Disable shields
            aliveInvaders.callAll('showField', false);

            // Decrease next generation time
            if (this.currentGenerationTime > MIN_GENERATION_TIME) {
                this.currentGenerationTime -= 150;
                console.log(this.currentGenerationTime);
            }
        }

    },

    createWall: function () {
        // create a new bitmap data object
        var wallBmp = this.game.add.bitmapData(this.game.width, 3);

        // draw the wall
        wallBmp.ctx.beginPath();
        wallBmp.ctx.rect(0,0,this.game.width,3);
        wallBmp.ctx.fillStyle = '#ffffff';
        wallBmp.ctx.fill();

        // use the bitmap data as the texture for the sprite
        this.wall = this.add.sprite(0, this.game.height - WALL_MARGIN, wallBmp);
        this.game.physics.enable(this.wall, Phaser.Physics.ARCADE);
        this.wall.body.immovable = true;
    }

};
