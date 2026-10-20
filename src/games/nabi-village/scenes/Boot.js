import Phaser from "phaser";
import { text, C } from "../ui.js";

const files = import.meta.glob("../assets/*.{png,wav,ogg}", { eager: true, query: "?url", import: "default" });
const url = (name) => files[`../assets/${name}`];

// sprite sheets: key -> [file, frameWidth, frameHeight]
const SHEETS = {
  nabi: ["nabi.png", 22, 17],
  dokkaebi: ["dokkaebi.png", 16, 16],
  oldman: ["oldman.png", 16, 16],
  mob: ["mob.png", 16, 16],
  spirit: ["spirit.png", 16, 16],
  dog: ["dog.png", 16, 16],
  toad: ["toad.png", 16, 16],
  donkey: ["donkey.png", 16, 16],
  "boss-idle": ["boss-idle.png", 50, 50],
  "boss-hit": ["boss-hit.png", 50, 50],
  slash: ["slash.png", 26, 32],
  smoke: ["smoke.png", 32, 32],
  chest: ["chest.png", 16, 16],
};
const IMAGES = ["nabi-face", "dokkaebi-face", "oldman-face", "mob-face", "spirit-face", "dog-face", "toad-face", "donkey-face",
  "boss-face", "horse-face", "coin", "onigiri", "branch", "feather", "iron", "gem", "grass", "gourd", "button", "button-hover",
  "button-disabled", "cell", "bg-battle", "bg-map"];
const SOUNDS = ["hit", "slash", "block", "select", "move", "coin", "levelup", "heal"];
const MUSIC = ["village", "fight"];

export class Boot extends Phaser.Scene {
  constructor() {
    super("Boot");
  }

  preload() {
    const bar = this.add.graphics();
    const label = text(this, 480, 300, "불러오는 중…", 22, C.creamText).setOrigin(0.5);
    this.load.on("progress", (p) => {
      bar.clear().fillStyle(C.wood, 1).fillRect(330, 330, 300 * p, 12);
      label.setText(`불러오는 중… ${Math.round(p * 100)}%`);
    });
    for (const [key, [file, w, h]] of Object.entries(SHEETS)) this.load.spritesheet(key, url(file), { frameWidth: w, frameHeight: h });
    for (const key of IMAGES) this.load.image(key, url(`${key}.png`));
    for (const key of SOUNDS) this.load.audio(key, url(`${key}.wav`));
    for (const key of MUSIC) this.load.audio(key, url(`${key}.ogg`));
  }

  create() {
    const a = this.anims;
    // Character sheets: 4 columns (down, up, left, right) x 7 rows. Column 2 faces left.
    for (const key of ["dokkaebi", "oldman", "mob", "spirit"]) {
      a.create({ key: `${key}-idle`, frames: a.generateFrameNumbers(key, { frames: [2, 6, 10, 14] }), frameRate: 5, repeat: -1 });
    }
    for (const key of ["nabi", "dog", "toad", "donkey"]) {
      a.create({ key: `${key}-idle`, frames: a.generateFrameNumbers(key, { frames: [0, 1] }), frameRate: 3, repeat: -1 });
    }
    a.create({ key: "boss-idle-idle", frames: a.generateFrameNumbers("boss-idle", { start: 0, end: 4 }), frameRate: 6, repeat: -1 });
    a.create({ key: "boss-hit", frames: a.generateFrameNumbers("boss-hit", { start: 0, end: 2 }), frameRate: 10 });
    a.create({ key: "slash", frames: a.generateFrameNumbers("slash", { start: 0, end: 4 }), frameRate: 18 });
    a.create({ key: "smoke", frames: a.generateFrameNumbers("smoke", { start: 0, end: 5 }), frameRate: 14 });
    this.registry.set("muted", false);
    this.scene.start("Map", { fresh: true });
  }
}
