// e.g. src/game/controlsTest.ts — dev/QA only is fine
export type ControlsProbe = {
  getYaw: () => number;       // radians; or getHeading()
  getSpeed: () => number;
  /** Inject held actions instead of real keys; both stay applied until you
   *  change them, so §5c can hold a key across frames and clear at the end. */
  setSteer?: (v: number) => void; // -1..1, same sign as production
  setKeys?: (codes: string[]) => void; // held until the next call; `[]` clears
};

declare global {
  interface Window {
    __controlsTest?: ControlsProbe;
  }
}
