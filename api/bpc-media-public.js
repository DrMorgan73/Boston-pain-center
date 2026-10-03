// BPC public media feed — Vercel Node Serverless Function.
// No authentication: returns only the public fields of uploaded media
// (title, description, URL, date, duration, category) for the public site's
// podcast / video-tips / resources pages. Never exposes record internals.
//
//   GET ?type=podcast|video|other -> { items: [...] } newest first
// Items match the shape the site's loadMedia() renderer expects:
//   { title:{en,es}, description:{en,es}, date, duration, categories:[],
//     audioUrl } for podcast, { ..., videoUrl } for video.

import { list } from '@vercel/blob';

const PREFIX = 'bpc-media/';
const TYPES = ['podcast', 'video', 'other'];

// Curated YouTube items (e.g. chosen by DrMorgan) merged after uploaded files.
// Shape matches what the site's loadMedia() renderer expects.
const YOUTUBE_FEATURES = {
  video: [
    {
      youtubeId: 'tAOv9hthD9U',
      title: { en: 'Why Coronavirus (COVID-19) Attacks the Body', es: 'Porque el Coronavirus (COVID-19) ataca el Cuerpo' },
      description: {
        en: 'Dr. Roberto Feliz explains how COVID-19 affects the body.',
        es: 'El Dr. Roberto Feliz explica cómo el COVID-19 afecta el cuerpo.',
      },
      date: '',
      duration: '',
      categories: [],
    },
  ],
  podcast: [],
  other: [],
};

const json = (res, obj, status = 200) => {
  res.status(status).setHeader('content-type', 'application/json');
  res.setHeader('cache-control', 'public, s-maxage=300, stale-while-revalidate=600');
  res.end(JSON.stringify(obj));
};

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
function fmtDate(iso) {
  try {
    const d = new Date(iso + 'T12:00:00');
    return `${MONTHS[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
  } catch { return iso || ''; }
}

export default async function handler(req, res) {
  const type = String(req.query.type || '');
  if (!TYPES.includes(type)) return json(res, { ok: false, error: 'bad_type' }, 400);
  if (!process.env.BLOB_READ_WRITE_TOKEN) return json(res, { ok: true, items: [] });

  try {
    const { blobs } = await list({ prefix: PREFIX, limit: 500 });
    const records = [];
    for (const b of blobs) {
      if (!b.pathname.endsWith('.json')) continue;
      let r;
      try { r = await fetch(b.url).then((x) => x.json()); } catch { continue; }
      if (!r || r.type !== type || !r.url) continue;
      records.push(r);
    }
    records.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    const items = records.map((r) => {
      const item = {
        title: r.title || { en: '', es: '' },
        description: r.description || { en: '', es: '' },
        date: fmtDate(r.date || (r.createdAt || '').slice(0, 10)),
        duration: r.duration || '',
        categories: r.category ? [r.category] : [],
      };
      if (type === 'podcast') item.audioUrl = r.url;
      else if (type === 'video') item.videoUrl = r.url;
      else item.fileUrl = r.url;
      return item;
    });
    for (const yt of YOUTUBE_FEATURES[type] || []) items.push(yt);
    return json(res, { ok: true, items });
  } catch {
    return json(res, { ok: true, items: [] });
  }
}
