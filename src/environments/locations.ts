import { HouseVariantId, LocationId } from '../types/schema';

export type { HouseVariantId, LocationId };

export interface LocationInfo {
  label: string;
  exterior: boolean;
  camera: {
    pos: [number, number, number];
    target: [number, number, number];
    fov: number;
  };
}

export const LOCATION_INFO: Record<LocationId, LocationInfo> = {
  town_overview: {
    label: 'Town Overview',
    exterior: true,
    camera: { pos: [-10, 62, 74], target: [6, 2, -6], fov: 55 },
  },
  street: {
    label: 'Main Street',
    exterior: true,
    camera: { pos: [0, 6.2, 16], target: [0, 4.2, 0], fov: 52 },
  },
  crossroads: {
    label: 'Crossroads',
    exterior: true,
    camera: { pos: [0, 7.0, 18], target: [0, 4.2, 0], fov: 54 },
  },
  school_exterior: {
    label: 'Town School',
    exterior: true,
    camera: { pos: [0, 7.6, 22], target: [0, 4.8, 0], fov: 58 },
  },
  house: {
    label: 'House',
    exterior: true,
    camera: { pos: [0, 6.6, 16], target: [0, 4.4, -1.5], fov: 54 },
  },
  shop: {
    label: 'RoMART',
    exterior: true,
    camera: { pos: [0, 6.2, 16], target: [0, 4.4, 0], fov: 54 },
  },
  playground: {
    label: 'Town Park',
    exterior: true,
    camera: { pos: [0, 6.8, 17], target: [0, 4.2, 0], fov: 56 },
  },
  classroom: {
    label: 'Classroom',
    exterior: false,
    camera: { pos: [0, 7.2, 19], target: [0, 4.5, -2], fov: 56 },
  },
  hallway: {
    label: 'School Hallway',
    exterior: false,
    camera: { pos: [0, 7.0, 18], target: [0, 4.4, -1], fov: 56 },
  },
  living_room: {
    label: 'Living Room',
    exterior: false,
    camera: { pos: [0, 6.6, 16], target: [0, 4.2, -1], fov: 54 },
  },
  kitchen: {
    label: 'Kitchen',
    exterior: false,
    camera: { pos: [0, 6.6, 16], target: [0, 4.2, -1], fov: 54 },
  },
  bedroom: {
    label: 'Bedroom',
    exterior: false,
    camera: { pos: [0, 6.6, 16], target: [0, 4.2, -1], fov: 54 },
  },
};
