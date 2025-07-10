import ships from './assets/ships.png';
import tiles from './assets/tiles.png';

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
    ships: {
      key: "ships",
      args: [
        ships,
        {
          frameWidth: 64,
          frameHeight: 64,
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
