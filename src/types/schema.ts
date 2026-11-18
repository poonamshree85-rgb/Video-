export type LocationId =
  | 'town_overview'
  | 'street'
  | 'crossroads'
  | 'school_exterior'
  | 'house'
  | 'shop'
  | 'playground'
  | 'classroom'
  | 'hallway'
  | 'living_room'
  | 'kitchen'
  | 'bedroom';

export type HouseVariantId = 'blue' | 'yellow' | 'red' | 'white' | 'green';

export type CharacterId = string;

export type AnimationMode =
  | 'idle'
  | 'sleep'
  | 'walk'
  | 'sprint'
  | 'jump'
  | 'wave'
  | 'point'
  | 'panting'
  | 'knocked'
  | 'celebrate'
  | 'dance';

export type ExpressionId =
  | 'smile'
  | 'sleeping'
  | 'shocked'
  | 'panic'
  | 'angry'
  | 'cool'
  | 'laugh'
  | 'deadpan';

export type PropId =
  | 'none'
  | 'creepy_shadow'
  | 'backpack'
  | 'halo_gold'
  | 'halo_red'
  | 'mouth_tape'
  | 'bloxy_cola'
  | 'hammer'
  | 'binoculars'
  | 'pointer'
  | 'pan'
  | 'clipboard'
  | 'counter_high'
  | 'counter_mid'
  | 'counter_bully'
  | 'counter_3'
  | 'counter_2'
  | 'counter_1'
  | 'counter_0'
  | 'counter_100'
  | 'counter_99'
  | 'counter_98'
  | 'counter_50'
  | 'counter_12';

export interface CharacterKeyframe {
  frame: number;
  position: [number, number, number];
  rotationY: number;
  rotationX?: number;
  rotationZ?: number;
  anim: AnimationMode;
  expression: ExpressionId;
  prop?: PropId;
  chatBubble?: string;
}

export interface CameraShot {
  startFrame: number;
  endFrame: number;
  fromPos: [number, number, number];
  toPos: [number, number, number];
  fromTarget: [number, number, number];
  toTarget: [number, number, number];
  fov?: number;
  shake?: number;
}

export interface SceneSegment {
  id: string;
  location: LocationId;
  variant?: HouseVariantId;
  isNight?: boolean;
  skyColor?: string;
  boardText?: string[];
  schoolName?: string;
  startFrame: number;
  endFrame: number;
  cameraShots: CameraShot[];
  characters: Record<CharacterId, CharacterKeyframe[] | undefined>;
}

export interface CaptionCue {
  startFrame: number;
  endFrame: number;
  text: string;
}

export interface RobloxShortStory {
  title: string;
  fps: number;
  durationInFrames: number;
  width: number;
  height: number;
  cast?: Record<string, unknown>;
  scenes: SceneSegment[];
  captions: CaptionCue[];
}
