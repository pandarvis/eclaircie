/* La porte de la phase privee.
   Vercel Routing Middleware : un fichier a la racine du projet, valable pour
   tous les frameworks, y compris un site entierement statique.

   Sans la variable d'environnement PHRASE_DE_PASSE, le site est ouvert :
   c'est ainsi qu'on publiera, le jour venu, sans rien reecrire.

   C'est un rideau, pas une serrure. Assez pour « pas public », pas pour
   « secret » : la phrase voyage en clair dans un cookie. */
import { next } from '@vercel/functions';

export const config = { matcher: '/((?!_astro/).*)' };

const COOKIE = 'eclaircie';

const PAGE = `<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>L'Éclaircie</title>
<style>
  body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0A0E13;
       color:#E6EBF0;font-family:Constantia,"Palatino Linotype",Georgia,serif}
  form{display:flex;flex-direction:column;gap:1.1rem;width:min(22rem,80vw)}
  p{margin:0 0 .4rem;color:#A7B5C2;font-style:italic;text-align:center;line-height:1.5}
  input{font:inherit;padding:.7rem .9rem;background:#161F2A;color:inherit;
        border:1px solid #35495D;border-radius:3px}
  input:focus{outline:2px solid #D9A441;outline-offset:2px}
  button{font-family:Corbel,"Segoe UI",sans-serif;font-size:.72rem;letter-spacing:.19em;
         text-transform:uppercase;padding:.75rem;background:#E6EBF0;color:#0A0E13;
         border:0;border-radius:3px;cursor:pointer}
  button:hover{background:#D9A441}
</style></head><body>
<form method="GET">
<p>L'irréparable est condamné, le réparable est pardonné,<br>le meurtri est gracié.</p>
<input type="password" name="phrase" placeholder="la phrase de passe" autofocus>
<button type="submit">Entrer</button>
</form>
</body></html>`;

export default function middleware(request: Request): Response {
  const attendue = process.env.PHRASE_DE_PASSE;
  if (!attendue) return next();

  const url = new URL(request.url);
  const cookie = request.headers.get('cookie') ?? '';

  if (cookie.split(';').some((c) => c.trim() === `${COOKIE}=${attendue}`)) return next();

  if (url.searchParams.get('phrase') === attendue) {
    return new Response(null, {
      status: 302,
      headers: {
        location: url.pathname,
        'set-cookie': `${COOKIE}=${attendue}; Path=/; HttpOnly; Secure;`
                    + ` SameSite=Lax; Max-Age=31536000`,
      },
    });
  }

  return new Response(PAGE, {
    status: 401,
    headers: {
      'content-type': 'text/html; charset=utf-8',
      'x-robots-tag': 'noindex, nofollow',
    },
  });
}
