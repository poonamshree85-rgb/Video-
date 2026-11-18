import * as THREE from 'three';
import type { TopStyle } from './look';

export function shade(hex: string, factor: number): string {
  const c = new THREE.Color(hex);
  c.multiplyScalar(factor);
  return `#${c.getHexString()}`;
}

export function sleeveColorFor(topStyle: TopStyle, topColor: string, topSecondary: string): string {
  if (topStyle === 'vest' || topStyle === 'jacket' || topStyle === 'uniform') {
    return topSecondary;
  }
  return topColor;
}

export function createTopTexture(
  topStyle: TopStyle,
  topColor: string,
  topSecondary: string,
  skin: string,
  face: 'front' | 'back' | 'side'
): THREE.CanvasTexture {
  const w = 256;
  const h = 256;
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = topColor;
  ctx.fillRect(0, 0, w, h);

  // Subtle fabric shading at edges
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, 'rgba(255,255,255,0.08)');
  grad.addColorStop(1, 'rgba(0,0,0,0.14)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  if (topStyle === 'plaid') {
    ctx.fillStyle = topSecondary;
    ctx.globalAlpha = 0.45;
    for (let x = 16; x < w; x += 48) ctx.fillRect(x, 0, 14, h);
    for (let y = 16; y < h; y += 48) ctx.fillRect(0, y, w, 14);
    ctx.globalAlpha = 1;
  } else if (topStyle === 'hoodie') {
    if (face === 'front') {
      // Pocket
      ctx.fillStyle = shade(topColor, 0.85);
      ctx.beginPath();
      ctx.roundRect(44, 160, w - 88, 70, 16);
      ctx.fill();
      // Drawstrings
      ctx.fillStyle = topSecondary;
      ctx.fillRect(102, 24, 8, 66);
      ctx.fillRect(146, 24, 8, 66);
    }
    // Neckline
    ctx.fillStyle = skin;
    ctx.beginPath();
    ctx.arc(w / 2, 0, 32, 0, Math.PI);
    ctx.fill();
  } else if (topStyle === 'suit' || topStyle === 'jacket' || topStyle === 'vest') {
    if (face === 'front') {
      ctx.fillStyle = topSecondary;
      ctx.beginPath();
      ctx.moveTo(w * 0.34, 0);
      ctx.lineTo(w * 0.66, 0);
      ctx.lineTo(w * 0.5, 130);
      ctx.closePath();
      ctx.fill();

      if (topStyle === 'suit') {
        ctx.fillStyle = '#DC2626';
        ctx.fillRect(w * 0.48, 12, 10, 96);
      }
      if (topStyle === 'jacket') {
        ctx.fillStyle = '#CBD5E1';
        ctx.fillRect(w * 0.49, 120, 6, h - 120);
      }
    }
  } else if (topStyle === 'polo' || topStyle === 'blouse' || topStyle === 'uniform') {
    if (face === 'front') {
      ctx.fillStyle = topSecondary;
      ctx.beginPath();
      ctx.moveTo(w * 0.32, 0);
      ctx.lineTo(w * 0.5, 36);
      ctx.lineTo(w * 0.68, 0);
      ctx.closePath();
      ctx.fill();
      ctx.fillStyle = skin;
      ctx.beginPath();
      ctx.arc(w / 2, 0, 22, 0, Math.PI);
      ctx.fill();
    }
  } else {
    // Crew neckline
    if (face === 'front') {
      ctx.fillStyle = skin;
      ctx.beginPath();
      ctx.arc(w / 2, 0, 34, 0, Math.PI);
      ctx.fill();
      ctx.strokeStyle = topSecondary;
      ctx.lineWidth = 8;
      ctx.stroke();
    }
  }

  // Hem line
  ctx.fillStyle = shade(topColor, 0.8);
  ctx.fillRect(0, h - 14, w, 14);

  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.needsUpdate = true;
  return tex;
}

export function createSleeveTexture(topStyle: TopStyle, topColor: string, topSecondary: string): THREE.CanvasTexture {
  const w = 128;
  const h = 128;
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d')!;

  const base = sleeveColorFor(topStyle, topColor, topSecondary);
  ctx.fillStyle = base;
  ctx.fillRect(0, 0, w, h);

  if (topStyle === 'plaid') {
    ctx.fillStyle = topSecondary;
    ctx.globalAlpha = 0.4;
    ctx.fillRect(24, 0, 16, h);
    ctx.fillRect(80, 0, 16, h);
    ctx.fillRect(0, 32, w, 16);
    ctx.globalAlpha = 1;
  }

  ctx.fillStyle = shade(base, 0.78);
  ctx.fillRect(0, h - 14, w, 14);

  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.needsUpdate = true;
  return tex;
}

export function createJeansTexture(bottomColor: string): THREE.CanvasTexture {
  const w = 128;
  const h = 128;
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = bottomColor;
  ctx.fillRect(0, 0, w, h);

  ctx.strokeStyle = '#F59E0B';
  ctx.lineWidth = 3;
  ctx.setLineDash([6, 4]);
  ctx.beginPath();
  ctx.moveTo(10, 0);
  ctx.lineTo(10, h);
  ctx.moveTo(w - 10, 0);
  ctx.lineTo(w - 10, h);
  ctx.stroke();

  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.needsUpdate = true;
  return tex;
}
