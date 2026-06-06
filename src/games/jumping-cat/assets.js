import tiles from "./assets/tiles.png";
import platform from "./assets/platform.png";
import run from "./assets/run.png";
// import jump2 from "./assets/jump2.png";
import jump from "./assets/jump.png";
import power1 from "./assets/power1.png";
import power2 from "./assets/power2.png";
import power3 from "./assets/power3.png";
import power4 from "./assets/power4.png";
import power5 from "./assets/power5.png";
import power6 from "./assets/power6.png";
import power7 from "./assets/power7.png";

export default {
  // 'audio': {
  //     score: {
  //         key: 'sound',
  //         args: ['assets/sound.mp3', 'assets/sound.m4a', 'assets/sound.ogg']
  //     },
  // },
  image: {
    power1: { key: "power1", args: [power1] },
    power2: { key: "power2", args: [power2] },
    power3: { key: "power3", args: [power3] },
    power4: { key: "power4", args: [power4] },
    power5: { key: "power5", args: [power5] },
    power6: { key: "power6", args: [power6] },
    power7: { key: "power7", args: [power7] },
  },
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
