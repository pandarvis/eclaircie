import { defineConfig } from 'astro/config';

export default defineConfig({
  // Statique : chaque texte est une page HTML complete, servie telle quelle.
  output: 'static',
  build: { format: 'directory' },
});
