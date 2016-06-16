var invadersApp = invadersApp || {};

invadersApp.Player = function (ctx, shootDelay) {

    this.shootDelay = shootDelay;
    if (this.shootDelay === undefined) { this.shootDelay = 150; }
    this.ctx = ctx;
    this.game = ctx.game;

    Phaser.Sprite.call(this, this.game, this.game.width / 2, this.game.height - 30, 'nao');
    this.game.physics.enable(this, Phaser.Physics.ARCADE);
    this.anchor.setTo(0.5, 0.5);
    this.game.physics.enable(this, Phaser.Physics.ARCADE);
    this.body.collideWorldBounds = true;


    // Create a pool of bullets
    this.bullets = this.game.add.group();
    this.bullets.enableBody = true;
    this.bullets.physicsBodyType = Phaser.Physics.ARCADE;
    this.bullets.createMultiple(6, 'bullet');
    this.bullets.setAll('anchor.x', 0.5);
    this.bullets.setAll('anchor.y', 1);
    this.bullets.setAll('outOfBoundsKill', true);
    this.bullets.setAll('checkWorldBounds', true);

    this.readyToFire = true;
    this.lastShootAt = 0;

};

invadersApp.Player.prototype = Object.create(Phaser.Sprite.prototype);
invadersApp.Player.prototype.constructor = invadersApp.Player;

invadersApp.Player.prototype.update = function () {

    if (this.game.physics.arcade.isPaused) return;

    this.body.velocity.setTo(0, 0);
    
    if (this.ctx.cursors.left.isDown) {
        if (this.scale.x > 0){
            this.scale.x *= -1;
        }
        this.body.velocity.x = -500;
    }
    else if (this.ctx.cursors.right.isDown) {
        if (this.scale.x < 0){
            this.scale.x *= -1;
        }
        this.body.velocity.x = 500;
    }

    
    if (this.ctx.fireButton.isDown && this.readyToFire) {
        this.readyToFire = false;

        //  Grab the first bullet we can from the pool
        if (this.game.time.now > this.lastShootAt + this.shootDelay) {
            this.lastShootAt = this.game.time.now;
            var bullet = this.bullets.getFirstExists(false);
            if (bullet) {
                //  And fire it
                var xpos;
                if (this.scale.x < 0){
                    xpos = this.x - 21;
                } else {
                    xpos = this.x + 21;
                }
                bullet.reset(xpos, this.y - 20);
                bullet.body.velocity.y = -2000;
            }
        }
    }

    if (this.ctx.fireButton.isUp){
        this.readyToFire = true;
    }
};

