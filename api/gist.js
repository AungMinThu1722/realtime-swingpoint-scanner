export default async function handler(req, res) {
  const GIST_ID = process.env.GIST_ID || "9d1d74c2c9b868f2c6c0653b43c344dc";
  const GIST_TOKEN = process.env.GIST_TOKEN || "";

  const headers = { 'Accept': 'application/vnd.github+json' };
  if (GIST_TOKEN) {
    headers['Authorization'] = `token ${GIST_TOKEN}`;
  }

  try {
    const resp = await fetch(`https://api.github.com/gists/${GIST_ID}`, { headers });
    const data = await resp.json();
    const content = JSON.parse(data.files['scanner_data.json'].content);

    res.setHeader('Cache-Control', 'public, max-age=0, s-maxage=900, stale-while-revalidate=60');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.status(200).json(content);
  } catch (error) {
    console.error('Gist proxy error:', error);
    res.status(500).json({ error: 'Failed to fetch gist', message: error.message });
  }
}
