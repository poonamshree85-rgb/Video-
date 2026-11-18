export type HairStyle =
  | 'bacon'
  | 'messyFringe'
  | 'sidePart'
  | 'fluffySwept'
  | 'slickBack'
  | 'spikyAnime'
  | 'curly'
  | 'buzz'
  | 'bob'
  | 'wavyLong'
  | 'ponytail'
  | 'bun'
  | 'pigtails'
  | 'grandpa'
  | 'none';

export type HairColorName =
  | 'black'
  | 'darkBrown'
  | 'brown'
  | 'auburn'
  | 'ginger'
  | 'blonde'
  | 'goldenBlonde'
  | 'platinum'
  | 'gray'
  | 'white'
  | 'blue'
  | 'pink'
  | 'red';

export type TopStyle =
  | 'tshirt'
  | 'hoodie'
  | 'pullover'
  | 'plaid'
  | 'polo'
  | 'blouse'
  | 'sweater'
  | 'vest'
  | 'jacket'
  | 'uniform'
  | 'suit'
  | 'dress'
  | 'tank';

export type BottomStyle = 'pants' | 'jeans' | 'shorts' | 'skirt';
export type ShoeStyle = 'sneakers' | 'boots' | 'formal';
export type FacialHair = 'none' | 'stubble' | 'mustache' | 'beard';

export type AccessoryType =
  | 'cap'
  | 'backwardsCap'
  | 'beanie'
  | 'glasses'
  | 'sunglasses'
  | 'headphones'
  | 'bow'
  | 'crown';

export interface AccessorySpec {
  type: AccessoryType;
  color?: string;
  secondary?: string;
}

export interface CharacterLook {
  skin: string;
  hair: {
    style: HairStyle;
    color: HairColorName | string;
    highlight?: string;
    ombre?: string;
  };
  top: {
    style: TopStyle;
    color: string;
    secondary?: string;
    sleeves?: 'long' | 'short' | 'none';
  };
  bottom: {
    style: BottomStyle;
    color: string;
    legs?: string;
  };
  shoes: {
    style?: ShoeStyle;
    color: string;
    sole?: string;
  };
  accessories?: Array<AccessoryType | AccessorySpec>;
  facialHair?: FacialHair;
  facialHairColor?: string;
  freckles?: boolean;
  blush?: boolean;
  scale?: number;
}

export interface CharacterLookOverride {
  extends?: string;
  skin?: string;
  hair?: Partial<CharacterLook['hair']>;
  top?: Partial<CharacterLook['top']>;
  bottom?: Partial<CharacterLook['bottom']>;
  shoes?: Partial<CharacterLook['shoes']>;
  accessories?: Array<AccessoryType | AccessorySpec>;
  facialHair?: FacialHair;
  facialHairColor?: string;
  freckles?: boolean;
  blush?: boolean;
  scale?: number;
}

export const HAIR_COLORS: Record<HairColorName, { color: string; highlight: string; ombre?: string }> = {
  black: { color: '#18181B', highlight: '#3F3F46' },
  darkBrown: { color: '#3B2314', highlight: '#5C3A21' },
  brown: { color: '#6B3E26', highlight: '#8C583A' },
  auburn: { color: '#7C2D12', highlight: '#B45309' },
  ginger: { color: '#EA580C', highlight: '#FB923C' },
  blonde: { color: '#EAB308', highlight: '#FEF08A' },
  goldenBlonde: { color: '#F59E0B', highlight: '#FDE047' },
  platinum: { color: '#E2E8F0', highlight: '#FFFFFF' },
  gray: { color: '#94A3B8', highlight: '#CBD5E1' },
  white: { color: '#F1F5F9', highlight: '#FFFFFF' },
  blue: { color: '#2563EB', highlight: '#60A5FA' },
  pink: { color: '#EC4899', highlight: '#F9A8D4' },
  red: { color: '#DC2626', highlight: '#F87171' },
};

const SKIN_TONES: Record<string, string> = {
  fair: '#FDE2CC',
  light: '#F5D0B5',
  warm: '#E8B894',
  tan: '#D29B6E',
  medium: '#B97E52',
  brown: '#8D5524',
  dark: '#5C381C',
  classic: '#FACC15',
};

const NAMED_COLORS: Record<string, string> = {
  red: '#DC2626',
  darkRed: '#991B1B',
  orange: '#EA580C',
  yellow: '#FACC15',
  mustard: '#CA8A04',
  green: '#16A34A',
  teal: '#0D9488',
  sky: '#38BDF8',
  blue: '#2563EB',
  royal: '#1D4ED8',
  navy: '#1E3A8A',
  purple: '#7C3AED',
  pink: '#EC4899',
  white: '#F8FAFC',
  cream: '#FEF3C7',
  lightGray: '#CBD5E1',
  gray: '#64748B',
  charcoal: '#334155',
  black: '#111827',
  brown: '#78350F',
  darkBrown: '#451A03',
  denim: '#1E40AF',
  khaki: '#D6B48A',
  ginger: '#EA580C',
  blonde: '#EAB308',
};

export function resolveColor(value?: string, fallback = '#94A3B8'): string {
  if (!value) return fallback;
  if (value.startsWith('#') || value.startsWith('rgb')) return value;
  return NAMED_COLORS[value] ?? HAIR_COLORS[value as HairColorName]?.color ?? SKIN_TONES[value] ?? fallback;
}

export function resolveSkin(skin?: string): string {
  if (!skin) return SKIN_TONES.light;
  if (skin.startsWith('#') || skin.startsWith('rgb')) return skin;
  return SKIN_TONES[skin] ?? SKIN_TONES.light;
}

export function resolveHairColors(hair: CharacterLook['hair']): { color: string; highlight: string; ombre?: string } {
  const preset = HAIR_COLORS[hair.color as HairColorName];
  if (preset) {
    return {
      color: preset.color,
      highlight: hair.highlight ? resolveColor(hair.highlight, preset.highlight) : preset.highlight,
      ombre: hair.ombre ? resolveColor(hair.ombre) : preset.ombre,
    };
  }
  const color = resolveColor(hair.color, '#3B2314');
  return {
    color,
    highlight: hair.highlight ? resolveColor(hair.highlight, color) : color,
    ombre: hair.ombre ? resolveColor(hair.ombre) : undefined,
  };
}

export function normalizeAccessories(list?: Array<AccessoryType | AccessorySpec>): AccessorySpec[] {
  if (!list) return [];
  return list.map((item) => (typeof item === 'string' ? { type: item } : item));
}

export const CHARACTER_PRESETS: Record<string, CharacterLook> = {
  kid_boy: {
    skin: 'light',
    hair: { style: 'messyFringe', color: 'brown' },
    top: { style: 'hoodie', color: 'blue', secondary: 'white' },
    bottom: { style: 'jeans', color: 'denim' },
    shoes: { style: 'sneakers', color: 'white', sole: 'white' },
  },
  kid_girl: {
    skin: 'fair',
    hair: { style: 'wavyLong', color: 'blonde' },
    top: { style: 'dress', color: 'pink', secondary: 'white' },
    bottom: { style: 'skirt', color: 'pink', legs: 'fair' },
    shoes: { style: 'sneakers', color: 'white', sole: 'white' },
  },
  teen_girl: {
    skin: 'light',
    hair: { style: 'ponytail', color: 'darkBrown' },
    top: { style: 'sweater', color: 'purple', secondary: 'white' },
    bottom: { style: 'jeans', color: 'denim' },
    shoes: { style: 'sneakers', color: 'white', sole: 'white' },
  },
  schoolboy: {
    skin: 'light',
    hair: { style: 'sidePart', color: 'black' },
    top: { style: 'polo', color: 'sky', secondary: 'white' },
    bottom: { style: 'pants', color: 'navy' },
    shoes: { style: 'sneakers', color: 'black', sole: 'white' },
  },
  schoolgirl: {
    skin: 'fair',
    hair: { style: 'ponytail', color: 'brown' },
    top: { style: 'blouse', color: 'white', secondary: 'navy' },
    bottom: { style: 'skirt', color: 'navy', legs: 'fair' },
    shoes: { style: 'formal', color: 'black', sole: 'black' },
  },
  cool_kid: {
    skin: 'warm',
    hair: { style: 'fluffySwept', color: 'goldenBlonde' },
    top: { style: 'jacket', color: 'red', secondary: 'black' },
    bottom: { style: 'jeans', color: 'black' },
    shoes: { style: 'sneakers', color: 'red', sole: 'white' },
    accessories: ['sunglasses'],
  },
  bully: {
    skin: 'warm',
    hair: { style: 'spikyAnime', color: 'darkBrown' },
    top: { style: 'jacket', color: 'black', secondary: 'red' },
    bottom: { style: 'jeans', color: 'charcoal' },
    shoes: { style: 'boots', color: 'black' },
  },
  dad: {
    skin: 'light',
    hair: { style: 'sidePart', color: 'darkBrown' },
    top: { style: 'polo', color: 'green', secondary: 'white' },
    bottom: { style: 'pants', color: 'khaki' },
    shoes: { style: 'formal', color: 'brown' },
    facialHair: 'stubble',
  },
  real_mom: {
    skin: 'fair',
    hair: { style: 'bob', color: 'brown' },
    top: { style: 'sweater', color: 'teal', secondary: 'cream' },
    bottom: { style: 'jeans', color: 'denim' },
    shoes: { style: 'sneakers', color: 'white', sole: 'white' },
  },
  teacher_woman: {
    skin: 'fair',
    hair: { style: 'bun', color: 'blonde' },
    top: { style: 'blouse', color: 'cream', secondary: 'navy' },
    bottom: { style: 'skirt', color: 'charcoal', legs: 'fair' },
    shoes: { style: 'formal', color: 'black' },
    accessories: ['glasses'],
  },
  principal: {
    skin: 'medium',
    hair: { style: 'grandpa', color: 'gray' },
    top: { style: 'suit', color: 'charcoal', secondary: 'red' },
    bottom: { style: 'pants', color: 'charcoal' },
    shoes: { style: 'formal', color: 'black' },
    accessories: ['glasses'],
    facialHair: 'mustache',
  },
  little_brother: {
    skin: 'fair',
    hair: { style: 'curly', color: 'brown' },
    top: { style: 'tshirt', color: 'sky', secondary: 'white' },
    bottom: { style: 'shorts', color: 'navy' },
    shoes: { style: 'sneakers', color: 'blue', sole: 'white' },
    freckles: true,
    scale: 0.72,
  },
};

export const PRESET_NAMES = Object.keys(CHARACTER_PRESETS);

export function buildLook(override: CharacterLookOverride): CharacterLook {
  const base =
    (override.extends ? CHARACTER_PRESETS[override.extends] : undefined) ?? CHARACTER_PRESETS.kid_boy;
  return {
    ...base,
    ...override,
    skin: override.skin ?? base.skin,
    hair: {
      ...base.hair,
      ...(override.hair ?? {}),
    },
    top: {
      ...base.top,
      ...(override.top ?? {}),
    },
    bottom: {
      ...base.bottom,
      ...(override.bottom ?? {}),
    },
    shoes: {
      ...base.shoes,
      ...(override.shoes ?? {}),
    },
    accessories: override.accessories ?? base.accessories,
  };
}

export function lookForActor(charId: string, cast?: Record<string, unknown>): CharacterLook {
  const entry = cast?.[charId];
  if (typeof entry === 'string') {
    return CHARACTER_PRESETS[entry] ?? CHARACTER_PRESETS.kid_boy;
  }
  if (entry && typeof entry === 'object') {
    return buildLook(entry as CharacterLookOverride);
  }
  return CHARACTER_PRESETS[charId] ?? CHARACTER_PRESETS.kid_boy;
}
