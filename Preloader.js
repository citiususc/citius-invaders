
invadersApp.Preloader = function (game) {

	this.background = null;
	this.preloadBar = null;
	this.ready = false;

};

invadersApp.Preloader.prototype = {

	preload: function () {

		
		//	These are the assets we loaded in Boot.js
		//  this.background = this.game.add.tileSprite(0, 0, this.game.width, this.game.height, 'preloaderBackground');
		//var loadingText = this.add.bitmapText(this.game.width / 2, this.game.height / 2 - 60, 'minecraftia', 'Loading...');
		var loadingText = invadersApp.utils.addText(this, this.game.width / 2, this.game.height / 2 - 60, 'Loading...', 3);

		//loadingText.anchor.x = 0.5;
		//loadingText.anchor.setTo(0.5, 0.5);

		this.preloadBar = this.add.sprite(this.game.width / 2, loadingText.y + 40, 'preloaderBar');
		this.preloadBar.anchor.setTo(0.5, 0.5);
        //this.preloadBar.tint =

		//	This sets the preloadBar sprite as a loader sprite.
		//	What that does is automatically crop the sprite from 0 to full-width
		//	as the files below are loaded in.
		this.load.setPreloadSprite(this.preloadBar);

		//	Here we load the rest of the assets our game needs.
		//	As this is just a Project Template I've not provided these assets, swap them for your own.
		this.load.image('titlepage', 'assets/title.png');
		//this.load.atlas('playButton', 'images/play_button.png', 'images/play_button.json');
		this.load.audio('titleMusic', ['assets/audio/bodenstaendig_2000_in_rock_4bit.ogg']);
		

		//	+ lots of other required assets here
		this.load.image('nao', 'assets/nao.png');
		this.load.image('invader', 'assets/invader.png');
		this.load.image('bullet', 'assets/player_bullet.png');
        this.load.image('title', 'assets/title-3.png');
		this.load.image('logo', 'assets/citius-logo-8bit.png');
        

		// Read game settings
        this.load.json('settings', 'settings.json');
	},

	create: function () {

		//	Once the load has finished we disable the crop because we're going to sit in the update loop for a short while as the music decodes
		this.preloadBar.cropEnabled = false;

	},

	update: function () {
		
		if (this.cache.isSoundDecoded('titleMusic') && this.ready == false)
		{
			this.ready = true;
			this.state.start('MainMenu');
		}

	}

};
