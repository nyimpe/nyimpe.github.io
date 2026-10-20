// Shared drawing helpers. Colours come from the Ninja Adventure wood theme.
export const C = {
  ink: 0x131b1b,
  inkText: "#131b1b",
  wood: 0xf06733,
  woodLight: 0xffad55,
  woodDark: 0x9b513c,
  olive: 0x46402e,
  cream: 0xfff3dc,
  creamText: "#fff3dc",
  paper: 0xf6e7c8,
  red: 0xe0503c,
  green: 0x6cc04a,
  blue: 0x4a8ad6,
  gold: 0xffc43a,
  muted: "#8a7a64",
};

export const FONT = '"Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", sans-serif';

export function text(scene, x, y, str, size = 20, color = C.inkText, style = {}) {
  return scene.add.text(x, y, str, {
    fontFamily: FONT,
    fontSize: `${size}px`,
    color,
    resolution: 2,
    ...style,
  });
}

// Wood-framed box drawn with graphics so it scales to any size.
export function box(scene, x, y, w, h, { fill = C.olive, frame = C.wood, alpha = 1 } = {}) {
  const g = scene.add.graphics();
  g.fillStyle(C.ink, alpha);
  g.fillRoundedRect(x, y, w, h, 8);
  g.fillStyle(frame, alpha);
  g.fillRoundedRect(x + 3, y + 3, w - 6, h - 6, 6);
  g.fillStyle(fill, alpha);
  g.fillRoundedRect(x + 9, y + 9, w - 18, h - 18, 4);
  return g;
}

export function button(scene, x, y, w, h, label, onClick, { size = 22, sub = null, disabled = false, key = null } = {}) {
  const c = scene.add.container(x, y);
  const bg = scene.add.nineslice(0, 0, disabled ? "button-disabled" : "button", null, w / 3, h / 3, 3, 3, 2, 3).setScale(3).setOrigin(0);
  const label1 = text(scene, w / 2, sub ? h / 2 - 12 : h / 2, label, size, disabled ? "#d8c8b0" : C.creamText, { fontStyle: "bold" }).setOrigin(0.5);
  c.add([bg, label1]);
  if (sub) c.add(text(scene, w / 2, h / 2 + 16, sub, 16, disabled ? "#d8c8b0" : "#ffe6c4").setOrigin(0.5));
  if (key) c.add(text(scene, 10, 6, key, 14, "#ffe6c4"));
  c.setSize(w, h);
  if (!disabled) {
    const zone = scene.add.zone(0, 0, w, h).setOrigin(0).setInteractive({ useHandCursor: true });
    zone.on("pointerover", () => bg.setTexture("button-hover"));
    zone.on("pointerout", () => bg.setTexture("button"));
    zone.on("pointerdown", () => {
      sfx(scene, "select");
      onClick();
    });
    c.add(zone);
  }
  c.bg = bg;
  return c;
}

export function hpBar(scene, x, y, w, ratio, color) {
  const g = scene.add.graphics();
  g.fillStyle(C.ink, 1).fillRect(x, y, w, 10);
  g.fillStyle(0x5a4a44, 1).fillRect(x + 2, y + 2, w - 4, 6);
  g.fillStyle(color, 1).fillRect(x + 2, y + 2, Math.max(0, Math.round((w - 4) * ratio)), 6);
  return g;
}

export function floatText(scene, x, y, str, color = "#ffffff", size = 28) {
  const t = text(scene, x, y, str, size, color, { fontStyle: "bold", stroke: "#131b1b", strokeThickness: 5 }).setOrigin(0.5);
  scene.tweens.add({ targets: t, y: y - 46, alpha: 0, duration: 900, ease: "Cubic.easeOut", onComplete: () => t.destroy() });
  return t;
}

export function sfx(scene, key, volume = 0.5) {
  if (scene.registry.get("muted")) return;
  if (scene.cache.audio.exists(key)) scene.sound.play(key, { volume });
}

function stopMusic(scene) {
  const old = scene.registry.get("musicSound");
  if (old) {
    old.stop();
    old.destroy();
  }
  scene.registry.set("musicSound", null);
}

// One looping track at a time, tracked in the registry so scenes can swap it.
export function music(scene, key) {
  const playing = scene.registry.get("musicSound");
  if (scene.registry.get("musicKey") === key && playing) return;
  stopMusic(scene);
  scene.registry.set("musicKey", key);
  if (scene.registry.get("muted") || !scene.cache.audio.exists(key)) return;
  const sound = scene.sound.add(key, { loop: true, volume: 0.28 });
  sound.play();
  scene.registry.set("musicSound", sound);
}

export function muteToggle(scene, x, y) {
  const label = () => (scene.registry.get("muted") ? "소리 끔" : "소리 켬");
  const t = text(scene, x, y, label(), 16, C.creamText).setOrigin(1, 0.5).setInteractive({ useHandCursor: true });
  t.on("pointerdown", () => {
    const muted = !scene.registry.get("muted");
    scene.registry.set("muted", muted);
    if (muted) stopMusic(scene);
    else music(scene, scene.registry.get("musicKey"));
    t.setText(label());
  });
  return t;
}

// Dim the screen and show a centred wood panel. Returns the container.
export function modal(scene, w, h) {
  const layer = scene.add.container(0, 0).setDepth(100);
  const shade = scene.add.rectangle(0, 0, 960, 640, 0x000000, 0.55).setOrigin(0).setInteractive();
  const x = (960 - w) / 2;
  const y = (640 - h) / 2;
  layer.add([shade, box(scene, x, y, w, h, { fill: C.paper, frame: C.wood })]);
  layer.inner = { x, y, w, h };
  return layer;
}
