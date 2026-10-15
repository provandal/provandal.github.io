import { defineCollection, z } from 'astro:content';

const writing = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

// Posts recovered from the Brass Tacks Typepad blog via the Wayback Machine.
// Written by scripts/brasstacks_import.py; the body is the original HTML.
const brasstacks = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
    postedAt: z.string().optional(),
    description: z.string(),
    originalUrl: z.string().url(),
    sources: z.array(z.object({ label: z.string(), url: z.string().url() })),
    pdf: z.string().optional(),
    comments: z
      .array(z.object({ author: z.string(), date: z.string(), html: z.string() }))
      .default([]),
  }),
});

export const collections = { writing, brasstacks };
