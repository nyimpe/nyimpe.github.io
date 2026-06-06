
import Phaser from "phaser";

export class Game extends Phaser.Scene {
  constructor() {
    super("Game");
    this.blocks = [];
    this.blockSize = 40; // Define a standard block size
    this.blockColors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF, 0x800080, 0xFFA500]; // Some base colors
  }

  create() {
    const { width, height } = this.scale;

    // Add a static ground
    this.matter.add.rectangle(width / 2, height - 20, width, 40, { isStatic: true, label: 'ground' });

    // Create some initial blocks
    for (let i = 0; i < 20; i++) { // Increase block count
      this.spawnRandomBlock();
    }

    // Add an event listener for pointer down to add new blocks (and handle removal)
    this.input.on('pointerdown', (pointer) => {
        // Check if a block was clicked for removal
        const bodiesAtPointer = this.matter.query.point(this.matter.world.bodies, { x: pointer.x, y: pointer.y });
        const clickedBlockBody = bodiesAtPointer.find(body => body.label === 'block');

        if (clickedBlockBody) {
            this.removeBlock(clickedBlockBody);
        } else {
            // Spawn a new block if no existing block was clicked
            this.spawnBlock(pointer.x, pointer.y);
        }
    });

    // Update graphics positions in update loop
    this.matter.world.on('afterUpdate', () => {
        this.blocks.forEach(blockData => {
            const { body, graphics } = blockData;
            graphics.setPosition(body.position.x, body.position.y);
            graphics.setRotation(body.angle);
        });
    });
  }

  spawnBlock(x, y) {
      const color = Phaser.Utils.Array.GetRandom(this.blockColors);
      const size = this.blockSize; // Use standard size for now

      // Create Matter.js body
      const body = this.matter.add.rectangle(x, y, size, size, { restitution: 0.2, friction: 0.8, density: 0.01, label: 'block' });

      // Create Phaser Graphics object
      const graphics = this.add.graphics({ fillStyle: { color: color } });
      graphics.fillRect(-size / 2, -size / 2, size, size); // Draw rectangle centered on its origin
      graphics.setPosition(body.position.x, body.position.y);
      graphics.setRotation(body.angle);

      const blockData = { body, graphics, color };
      this.blocks.push(blockData);
  }

  spawnRandomBlock() {
      const { width, height } = this.scale;
      const x = Phaser.Math.Between(50, width - 50);
      const y = Phaser.Math.Between(50, height / 4); // Spawn higher up
      this.spawnBlock(x, y);
  }

  removeBlock(matterBody) {
      const index = this.blocks.findIndex(blockData => blockData.body === matterBody);
      if (index > -1) {
          const blockData = this.blocks[index];
          // Remove from Matter.js world
          this.matter.world.remove(blockData.body);
          // Destroy Phaser Graphics object
          blockData.graphics.destroy();
          // Remove from our blocks array
          this.blocks.splice(index, 1);
      }
  }

  update() {
    // Game logic can go here
  }
}
