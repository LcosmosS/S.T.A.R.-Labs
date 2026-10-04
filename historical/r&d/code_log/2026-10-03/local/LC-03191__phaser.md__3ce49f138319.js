this.bullets = this.physics.add.group({
  classType: Bullet, maxSize: 64, runChildUpdate: true
});
// fire:
const b = this.bullets.get(x, y);        // reuse dead one or make new (up to maxSize)
if (!b) return;                          // pool exhausted → skip
b.enableBody(true, x, y, true, true);    // reactivate + show
// on expire/off-screen: DON'T destroy — recycle:
b.disableBody(true, true);               // deactivate + hide, returns to pool
