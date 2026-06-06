
import Phaser from "phaser";

export class Game extends Phaser.Scene {
  constructor() {
    super("Game");
    this.blocks = [];
  }

  create() {
    const { width, height } = this.scale;

    // Add a static ground
    this.matter.add.rectangle(width / 2, height - 20, width, 40, { isStatic: true, label: 'ground' });

    // Create some initial blocks (circles for simplicity first)
    for (let i = 0; i < 10; i++) {
      const x = Phaser.Math.Between(50, width - 50);
      const y = Phaser.Math.Between(50, height / 2);
      const radius = 20;
      const block = this.matter.add.circle(x, y, radius, { restitution: 0.5, friction: 0.8, density: 0.01 });

      this.blocks.push(block);
    }

    // Add an event listener for pointer down to add new blocks
    this.input.on('pointerdown', (pointer) => {
        const x = pointer.x;
        const y = pointer.y;
        const radius = Phaser.Math.Between(15, 30);
        const block = this.matter.add.circle(x, y, radius, { restitution: 0.5, friction: 0.8, density: 0.01 });
  
        this.blocks.push(block);
    });
  }

  update() {
    // Game logic can go here
  }
}
