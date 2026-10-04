import { P2PRoom } from "@/lib/multiplayer";

const p2p = new P2PRoom({
  room: "doc-42",
  selfId: myId,
  name: "ani",
  onPeersChanged: (peers) => render(peers),
  onMessage: (from, data, channel) => apply(from, data, channel),
});
await p2p.join();
p2p.broadcast(state); // unreliable "state" channel — game-rate, stale drops
p2p.send(event, to); // reliable channel — exactly-once events (to optional)
p2p.close();
