// Game global config vars

var WALL_MARGIN = 80;
var DIR_CHANGE_MIN_TIME = 10;
var SHOOT_DELAY = 100;
var MIN_INVADERS = 4;
var INITIAL_INVADERS = 6;
var MIN_GENERATION_TIME = Phaser.Time.SECOND * 2;

// Extended sprite object for Invaders
Invader = function (ctx, genes, x, y) {

    var game = ctx.game;
    x = x || game.world.randomX;
    y = y || game.world.randomY % (game.world.height - WALL_MARGIN * 1.5) ;
    Phaser.Sprite.call(this, game, x, y, 'invader');
    game.physics.enable(this, Phaser.Physics.ARCADE);

    // Initialize genes by getting the default values from settings.json
    this.genes = genes || function () {
            var settings = ctx.settings;
            var genes = {};
            for(var gene in settings.genes){
                genes[gene] = game.rnd.realInRange(settings.genes[gene].min, settings.genes[gene].max);
            }
            return genes;
        }();

    this.anchor.setTo(0.5, 0.5);

    var alpha = Math.round(this.genes['alpha']);
    this.tint = Phaser.Color.getColor(alpha, alpha, alpha);
    this.body.velocity.x = this.genes['xvelocity'];
    this.body.velocity.y = this.genes['yvelocity'];
    this.scale.setTo(this.genes['scale'], this.genes['scale']);
    this.body.collideWorldBounds = true;
    this.body.bounce.set(1);

    // Used to control the probability of x-y change in direction
    this.lastTimeChanged = 0;

    // Create a shield
    var shield = this.game.make.graphics(0,0);
    shield.lineStyle(1, 0x15AFF0, 1);
    shield.drawCircle(-0.5, -0.5, 22);
    //shield.anchor.setTo(0.5, 0.5);
    this.addChild(shield);
    shield.visible = false;

    // Add the invader to the game (move this outside this class?)
    game.add.existing(this);
};

Invader.prototype = Object.create(Phaser.Sprite.prototype);
Invader.prototype.constructor = Invader;
Invader.prototype.update = function() {
    // Decide if it is time to change direction.
    if (this.game.time.now > this.lastTimeChanged + DIR_CHANGE_MIN_TIME) {
        this.lastTimeChanged = this.game.time.now;
        if (this.game.rnd.frac() < this.genes['x_prob_change_dir']) {
            this.body.velocity.x = -this.body.velocity.x;
        }
        if (this.game.rnd.frac() < this.genes['y_prob_change_dir']) {
            this.body.velocity.y = -this.body.velocity.y;
        }
    }
};
Invader.prototype.showField = function (show, color) {
    if (show == undefined) show = true;
    if (color == undefined) color = 0x15AFF0;
    this.getChildAt(0).tilt = color;
    this.getChildAt(0).visible = show;
};
Invader.prototype.freeze = function (freeze) {
    if (freeze == undefined) freeze = true;
    if (freeze){
        this.body.velocity.setTo(0, 0);
    } else {
        this.body.velocity.x = this.genes['xvelocity'];
        this.body.velocity.y = this.genes['yvelocity'];
    }
};



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

        for (var i = 0; i < INITIAL_INVADERS; i++) this.objects.invaders.push(new Invader(this));

        
        this.player = this.add.sprite(this.game.width / 2, this.game.height - 30, 'nao');
        this.player.anchor.setTo(0.5, 0.5);
        this.game.physics.enable(this.player, Phaser.Physics.ARCADE);
        this.player.body.collideWorldBounds = true;


        //var player = new Player(this);
        //this.game.add.existing(player);

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


        this.bullets = this.add.group();
        this.bullets.enableBody = true;
        this.bullets.physicsBodyType = Phaser.Physics.ARCADE;
        this.bullets.createMultiple(6, 'bullet');
        this.bullets.setAll('anchor.x', 0.5);
        this.bullets.setAll('anchor.y', 1);
        this.bullets.setAll('outOfBoundsKill', true);
        this.bullets.setAll('checkWorldBounds', true);


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

        this.game.physics.arcade.overlap(this.bullets, this.objects.invaders, function (invader, bullet) {
            bullet.kill();
            var alive = that.objects.invaders.filter(function (invader) {
                return invader.alive;
            }).length;
            if (alive > MIN_INVADERS){
                invader.kill();
            } else {
                // Draw circle?
                that.objects.invaders.forEach(function (invader) {
                    invader.showField(true);
                });
            }
        }, null, this);

        this.game.physics.arcade.collide(this.wall, this.objects.invaders);

        this.player.body.velocity.setTo(0, 0);

        
        if (this.cursors.left.isDown) {
            if (this.player.scale.x > 0){
                this.player.scale.x *= -1;
            }
            this.player.body.velocity.x = -250;
        }
        else if (this.cursors.right.isDown) {
            if (this.player.scale.x < 0){
                this.player.scale.x *= -1;
            }
            this.player.body.velocity.x = 250;
        }

        if (this.fireButton.isDown && this.readyToFire) {
            this.readyToFire = false;

            //  Grab the first bullet we can from the pool
            if (this.game.time.now > this.lastShootAt + SHOOT_DELAY) {
                this.lastShootAt = this.game.time.now;
                var bullet = this.bullets.getFirstExists(false);
                if (bullet) {
                    //  And fire it
                    var xpos;
                    if (this.player.scale.x < 0){
                        xpos = this.player.x - 21;
                    } else {
                        xpos = this.player.x + 21;
                    }
                    bullet.reset(xpos, this.player.y - 20);
                    bullet.body.velocity.y = -1200;
                }
            }
        }

        if (this.fireButton.isUp){
            this.readyToFire = true;
        }
        

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
