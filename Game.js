// Game global config vars

var WALL_MARGIN = 80;
var DIR_CHANGE_MIN_TIME = 10;
var SHOOT_DELAY = 100;
var MIN_INVADERS = 4;
var INITIAL_INVADERS = 6;
var MIN_GENERATION_TIME = Phaser.Time.SECOND * 2;


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
    this.currentGenerationTime = Phaser.Time.SECOND * 5;
};

invadersApp.Game.prototype = {

    create: function () {

        var that = this;

        // Load game config
        this.settings = this.game.cache.getJSON('settings');

        // Initialize basic physics
        this.game.physics.startSystem(Phaser.Physics.ARCADE);

        // Group of invaders
        this.objects.invaders = this.add.group();
        this.objects.invaders.enableBody = true;
        this.objects.invaders.physicsBodyType = Phaser.Physics.ARCADE;


        // Initialize
        this.objects.invaders = [];

        for (var i = 0; i < INITIAL_INVADERS; i++) this.objects.invaders.push(new invadersApp.Invader(this));

        this.player = new invadersApp.Player(this);
        this.game.add.existing(this.player);

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


        this.cursors = this.game.input.keyboard.createCursorKeys();
        this.fireButton = this.game.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);

        var readyText = invadersApp.utils.addText(this, this.game.width / 2, this.game.height / 2, 'READY!', 5);

        this.game.input.keyboard.onDownCallback = function () {
            that.game.paused = false;
            if (readyText.visible){
                readyText.kill();
            }
        };

        this.game.paused = true;

        //this.pausePhysics();

    },

    update: function () {

        // If physics are paused, skip all
        if (this.game.physics.arcade.isPaused) return;

        var that = this;

        this.game.physics.arcade.overlap(this.player.bullets, this.objects.invaders, function (invader, bullet) {
            bullet.kill();
            var alive = that.objects.invaders.filter(function (invader) {
                return invader.alive;
            }).length;
            if (alive > MIN_INVADERS){
                invader.kill();
            } else {
                that.objects.invaders.forEach(function (invader) {
                    invader.showField(true);
                });
            }
        }, null, this);

        this.game.physics.arcade.collide(this.wall, this.objects.invaders);

    },

    quitGame: function (pointer) {

        //  TODO: Stop music, delete sprites, purge caches, free resources...

        //  Then let's go back to the main menu.
        this.state.start('MainMenu');

    },

    pausePhysics: function (pause) {
        if (pause == undefined) pause = true;
        this.game.physics.arcade.isPaused = pause;
    }

};
