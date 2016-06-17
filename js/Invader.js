var invadersApp = invadersApp || {};

// Extended sprite object for Invaders

invadersApp.Invader = function (ctx, genes, x, y) {

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
    this.scaleValue = this.genes['scale'];
    this.scale.setTo(this.scaleValue, this.scaleValue);
    this.body.collideWorldBounds = true;
    this.body.bounce.set(1);

    // Used to control the probability of x-y change in direction
    this.lastTimeChanged = 0;

    this.fitness = 0;

    // Create a shield
    this.shieldGraphics = this.game.make.graphics(0,0);
    
    // Add the invader to the game (move this outside this class?)
    game.add.existing(this);
};

invadersApp.Invader.prototype = Object.create(Phaser.Sprite.prototype);
invadersApp.Invader.prototype.constructor = invadersApp.Invader;
invadersApp.Invader.prototype.update = function() {
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
invadersApp.Invader.prototype.drawShield = function (color) {
    this.shieldGraphics.clear();
    this.shieldGraphics.lineStyle(1, color, 1);
    this.shieldGraphics.drawCircle(-0.5, -0.5, 15 * this.scaleValue);
    this.addChildAt(this.shieldGraphics, 0);
    this.shieldGraphics.visible = true;
    this.shieldGraphics.scale.setTo(1.5/this.scaleValue, 1.5/this.scaleValue);
};
invadersApp.Invader.prototype.hideShield = function (color) {
    this.shieldGraphics.clear();
    this.shieldGraphics.visible = false;
    //this.removeChildAt(0);
};
invadersApp.Invader.prototype.increaseFitness = function () {
  this.fitness++;
};
