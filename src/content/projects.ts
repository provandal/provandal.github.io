export interface Project {
  slug: string;
  name: string;
  kind: string;          // eyebrow label, e.g. "Interactive curriculum"
  summary: string;       // one-liner for landing page cards
  description: string;   // longer blurb for the listing page
  tech: string[];
  year: string;
  // Action links. Render whichever ones exist.
  liveUrl?: string;
  repoUrl?: string;
  buildLogUrl?: string;  // internal URL like "/writing/inference-illustrated-build-log/"
  status?: string;       // optional, e.g. "In progress" — shown when no live link
}

// Edit this array when projects change. Order = display order.
// First three appear on the landing page.
export const projects: Project[] = [
  {
    slug: 'inference-illustrated',
    name: 'Inference Illustrated',
    kind: 'Interactive curriculum',
    summary:
      'A guided tour through LLM inference and the network underneath it, built for storage and networking professionals.',
    description:
      'Curriculum designed around strict pedagogical rules: no blind cliffs, correct terms defined on first use, math lives in animations rather than narration, and every stop explains WHY before HOW. The anchor sentence across the attention demonstrations is "The server crashed because the storage controller that the technician replaced last week was faulty." Later stops cover batching, continuous batching, PagedAttention, and preemption.',
    tech: ['HTML', 'Vanilla JS', 'SVG animation'],
    year: '2026',
    liveUrl: 'https://provandal.github.io/inference-illustrated/',
    repoUrl: 'https://github.com/provandal/inference-illustrated',
    buildLogUrl: '/writing/inference-illustrated-build-log/',
  },
  {
    slug: 'protoviz',
    name: 'ProtoViz',
    kind: 'Open-source platform',
    summary:
      'An interactive protocol visualization platform covering sixteen-plus network and storage protocols. MIT and CC BY 4.0.',
    description:
      'Built to do for protocols what Wireshark does for packets but aimed at learning rather than debugging. The first release includes visualizations of TCP, HTTP, and NVMe, with more on the way. The platform is designed to be extensible, with a simple API for adding new protocol visualizations.',
    tech: ['TypeScript', 'React', 'MDX'],
    year: '2026',
    liveUrl: 'https://provandal.github.io/protoviz/',
    repoUrl: 'https://github.com/provandal/protoviz',
  },
  {
    slug: 'binary-digit-trainer',
    name: 'Binary Digit Trainer',
    kind: 'Educational app',
    summary:
      'A browser-based neural network learning app. Reposted by SNIA. The simplest useful thing I have ever built.',
    description:
      'A single-page app that lets the learner watch a tiny network learn to classify binary digits in real time, with every weight and gradient visible. No install, no framework, no magic.',
    tech: ['HTML', 'JavaScript'],
    year: '2025',
    liveUrl: 'https://provandal.github.io/binarydigittrainer/',
    repoUrl: 'https://github.com/provandal/binarydigittrainer',
  },
  {
    slug: 'post-training-explorer',
    name: 'Post-Training Explorer',
    kind: 'Interactive tool',
    summary:
      'A visual walkthrough of the post-training pipeline, from SFT through preference optimization.',
    description:
      'Companion piece to the SNIA Digital Storage Networks Technical Work Group post-training webinar series.',
    tech: ['HTML', 'JavaScript'],
    year: '2025',
    liveUrl: 'https://provandal.github.io/post-training-explorer/',
    repoUrl: 'https://github.com/provandal/post-training-explorer',
  },
  {
    slug: 'neural-architecture-tour',
    name: 'Neural Architecture Tour',
    kind: 'Interactive curriculum',
    summary:
      'A guided walkthrough of neural network architectures, from the perceptron forward.',
    description:
      'In active development. Aimed at engineers who want to understand model architectures as design choices, not as folklore.',
    tech: ['HTML', 'JavaScript'],
    year: '2026',
    repoUrl: 'https://github.com/provandal/neural-architecture-tour',
    status: 'In progress',
  },
  {
    slug: 'geolingua',
    name: 'GeoLingua',
    kind: 'npm package',
    summary: 'A globe-style internationalization selector. Published on npm.',
    description:
      'A small, focused UI primitive for language selection that uses geography as the organizing metaphor instead of a flat list.',
    tech: ['TypeScript', 'React'],
    year: '2025',
    repoUrl: 'https://github.com/provandal/geolingua',
  },
];
