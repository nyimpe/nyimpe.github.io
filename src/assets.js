import tiles from "./assets/tiles.png";
import player from "./assets/player.png";
import platform from "./assets/platform.png";

export default {
  // 'audio': {
  //     score: {
  //         key: 'sound',
  //         args: ['assets/sound.mp3', 'assets/sound.m4a', 'assets/sound.ogg']
  //     },
  // },
  // 'image': {
  //     spikes: {
  //         key: 'spikes',
  //         args: ['assets/spikes.png']
  //     },
  // },
  spritesheet: {
    player: {
      key: "player",
      args: [
        player,
        {
          frameWidth: 80,
          frameHeight: 110,
        },
      ],
    },
    platforms: {
      key: "platforms",
      args: [
        platform,
        {
          frameWidth: 375,
          frameHeight: 96,
        },
      ],
    },
    tiles: {
      key: "tiles",
      args: [
        tiles,
        {
          frameWidth: 32,
          frameHeight: 32,
        },
      ],
    },
  },
};
