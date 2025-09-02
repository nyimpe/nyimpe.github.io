import tiles from "./assets/tiles.png";
import platform from "./assets/platform.png";
import run from "./assets/run.png";
import jump2 from "./assets/jump2.png";
import jump from "./assets/jump.png";

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
    run: {
      key: "run",
      args: [
        run,
        {
          frameWidth: 80,
          frameHeight: 64,
        },
      ],
    },
    jump: {
      key: "jump",
      args: [
        jump,
        {
          frameWidth: 80,
          frameHeight: 64,
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
