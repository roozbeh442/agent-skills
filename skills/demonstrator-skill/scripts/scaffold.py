#!/usr/bin/env python3
import argparse, json, re, shutil, sys, textwrap
from pathlib import Path

PALETTES = {'navy': ('#173E5C','#D5DCE3'), 'teal': ('#087E83','#D9E7E7'), 'graphite': ('#343A46','#6B68D9')}
def write(root, path, content):
    p=root/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(textwrap.dedent(content).lstrip(),encoding='utf-8')
def main():
    p=argparse.ArgumentParser(); p.add_argument('--name',required=True);p.add_argument('--destination',required=True);p.add_argument('--menus',required=True);p.add_argument('--theme',choices=[*PALETTES,'custom'],default='navy');p.add_argument('--primary');p.add_argument('--accent');p.add_argument('--logo');p.add_argument('--database',choices=['none','postgres','later'],default='none');a=p.parse_args()
    root=Path(a.destination).expanduser().resolve()
    if root.exists(): sys.exit(f'Refusing existing destination: {root}')
    menus=list(dict.fromkeys(x.strip() for x in a.menus.split(',') if x.strip()))
    if not menus: sys.exit('At least one menu required')
    if 'Home' not in menus: menus.insert(0,'Home')
    if any(not re.fullmatch(r'[\w -]{1,40}',m) for m in menus): sys.exit('Menu names must be 1-40 characters (letters/numbers/spaces/-/_)')
    if a.theme=='custom':
        if not all(x and re.fullmatch('#[0-9a-fA-F]{6}',x) for x in (a.primary,a.accent)): sys.exit('Custom theme needs two hex colors')
        primary,accent=a.primary,a.accent
    else: primary,accent=PALETTES[a.theme]
    if a.logo and not Path(a.logo).is_file(): sys.exit('Logo file not found')
    root.mkdir(parents=True)
    write(root,'frontend/package.json',json.dumps({'name':re.sub('[^a-z0-9-]','-',a.name.lower()),'version':'0.1.0','private':True,'type':'module','scripts':{'dev':'vite --host 127.0.0.1','build':'tsc -b && vite build','test:e2e':'playwright test'},'dependencies':{'react':'^19.0.0','react-dom':'^19.0.0'},'devDependencies':{'@playwright/test':'^1.56.0','@types/react':'^19.0.0','@types/react-dom':'^19.0.0','typescript':'~5.9.0','vite':'^7.0.0'}},indent=2)+'\n')
    write(root,'frontend/index.html','<html><head><meta name="viewport" content="width=device-width,initial-scale=1" /></head><body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>')
    write(root,'frontend/tsconfig.json',json.dumps({'compilerOptions':{'target':'ES2022','lib':['ES2022','DOM','DOM.Iterable'],'module':'ESNext','moduleResolution':'Bundler','jsx':'react-jsx','strict':True,'skipLibCheck':True,'noEmit':True,'allowImportingTsExtensions':True},'include':['src']},indent=2))
    write(root,'frontend/src/config.ts',f'export const appName = {json.dumps(a.name)};\nexport const menus = {json.dumps(menus)};\nexport const theme = {{primary: {json.dumps(primary)}, accent: {json.dumps(accent)}}};\n')
    write(root,'frontend/src/main.tsx', '''
    import React, {useState} from 'react';
    import {createRoot} from 'react-dom/client';
    import {appName,menus,theme} from './config';
    import './style.css';
    const slug=(s:string)=>s.toLowerCase().trim().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
    function App(){
      const current=()=>menus.find(m=>location.pathname==='/'+slug(m))|| (location.pathname==='/'?'Home':menus[0]);
      const [page,setPage]=useState(current); const [open,setOpen]=useState(true);
      React.useEffect(()=>{const onPop=()=>setPage(current());window.addEventListener('popstate',onPop);return()=>window.removeEventListener('popstate',onPop)},[]);
      const go=(m:string)=>{history.pushState({},'', '/'+slug(m));setPage(m)};
      return <div className="layout" style={{'--primary':theme.primary,'--accent':theme.accent} as React.CSSProperties}>
        <aside className={open?'sidebar':'sidebar collapsed'}><nav aria-label="Main navigation">{menus.map(m=><button key={m} data-testid={'menu-'+slug(m)} className={page===m?'active':''} onClick={()=>go(m)}>{m}</button>)}</nav></aside>
        <main><header><button aria-label="Toggle sidebar" onClick={()=>setOpen(!open)}>☰</button><img src="/logo.png" alt="" onError={e=>e.currentTarget.style.display='none'}/><strong>{appName}</strong></header><section><h1 data-testid="page-title">{page}</h1><p>This is the {page} placeholder page.</p></section></main>
      </div>
    }
    createRoot(document.getElementById('root')!).render(<App/>);
    ''')
    write(root,'frontend/src/style.css','''
    *{box-sizing:border-box}body{margin:0;font-family:system-ui,Arial;color:#263340;background:#f6f8fa}.layout{display:flex;min-height:100vh}.sidebar{width:220px;background:var(--primary);padding:18px 10px;transition:width .2s}.sidebar.collapsed{width:0;padding:0;overflow:hidden}.sidebar nav{display:grid;gap:8px}.sidebar button{color:white;background:transparent;border:0;text-align:left;padding:12px;border-radius:7px;cursor:pointer;white-space:nowrap}.sidebar button.active,.sidebar button:hover{background:#ffffff30}main{flex:1;min-width:0}header{height:70px;background:white;display:flex;align-items:center;gap:16px;padding:0 24px;border-bottom:1px solid #ddd}header button{cursor:pointer;background:var(--accent);border:0;border-radius:5px;padding:8px 12px}header img{max-height:38px;max-width:120px}section{padding:28px}@media(max-width:650px){.sidebar{width:150px}.sidebar.collapsed{width:0}section{padding:16px}}
    ''')
    write(root,'frontend/vite.config.ts',"import {defineConfig} from 'vite';\nexport default defineConfig({server:{proxy:{'/api':'http://127.0.0.1:8000'}}});\n")
    write(root,'frontend/playwright.config.ts',"import {defineConfig} from '@playwright/test';\nexport default defineConfig({testDir:'./tests',use:{baseURL:'http://127.0.0.1:5173'},webServer:{command:'npm run dev',url:'http://127.0.0.1:5173',reuseExistingServer:!process.env.CI,timeout:30000}});\n")
    write(root,'frontend/tests/navigation.spec.ts',f'''import {{test,expect}} from '@playwright/test';
    const menus={json.dumps(menus)};
    const slug=(s:string)=>s.toLowerCase().trim().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
    test('every menu navigates and survives refresh',async ({{page}})=>{{
      await page.goto('/');
      for(const m of menus){{await page.getByTestId('menu-'+slug(m)).click();await expect(page.getByTestId('page-title')).toHaveText(m);await expect(page).toHaveURL(new RegExp('/'+slug(m)+'$'));await page.reload();await expect(page.getByTestId('page-title')).toHaveText(m);}}
      await page.getByRole('button',{{name:'Toggle sidebar'}}).click();await expect(page.locator('aside')).toHaveClass(/collapsed/);
    }});
    ''')
    write(root,'backend/main.py', '''from fastapi import FastAPI
    app = FastAPI(title="Demonstrator API")
    @app.get("/api/health")
    def health():
        return {"status": "ok"}
    ''')
    deps=['fastapi>=0.115','uvicorn>=0.30']
    if a.database=='postgres': deps+=['sqlalchemy>=2.0','psycopg[binary]>=3.2','alembic>=1.14']
    write(root,'backend/pyproject.toml','[project]\nname = "demonstrator-backend"\nversion = "0.1.0"\nrequires-python = ">=3.11"\ndependencies = '+json.dumps(deps)+'\n')
    write(root,'dev.sh','''#!/usr/bin/env bash
    set -euo pipefail
    cd "$(dirname "$0")"
    (cd backend && uv run uvicorn main:app --host 127.0.0.1 --port 8000) & BACK=$!
    trap 'kill "$BACK" 2>/dev/null || true' EXIT
    cd frontend && npm run dev
    ''')
    write(root,'test.sh','''#!/usr/bin/env bash
    set -euo pipefail
    cd "$(dirname "$0")"
    python3 -m py_compile backend/main.py
    (cd frontend && npm run build)
    (cd backend && uv run uvicorn main:app --host 127.0.0.1 --port 8000 >/tmp/demonstrator-api-$$.log 2>&1) & BACK=$!
    trap 'kill "$BACK" 2>/dev/null || true; rm -f /tmp/demonstrator-api-$$.log' EXIT
    for i in $(seq 1 40); do if curl -fsS http://127.0.0.1:8000/api/health | grep -q '"ok"'; then break; fi; sleep 0.25; done
    curl -fsS http://127.0.0.1:8000/api/health | grep -q '"ok"'
    (cd frontend && npx playwright test)
    ''')
    for f in ['dev.sh','test.sh']: (root/f).chmod(0o755)
    write(root,'.gitignore','frontend/node_modules/\nfrontend/dist/\nfrontend/test-results/\nfrontend/playwright-report/\nbackend/.venv/\n__pycache__/\n*.pyc\n.env\n')
    write(root,'.env.example','DATABASE_URL=postgresql+psycopg://demo:demo@127.0.0.1:5432/demo\n' if a.database=='postgres' else '# Add environment variables here as needed.\n')
    write(root,'README.md',f'# {a.name}\n\nMinimal React + FastAPI demonstrator.\n\nRun: `npm install --prefix frontend`, `cd backend && uv sync`, then `./dev.sh`.\n\nTest: `cd frontend && npx playwright install chromium`, then `./test.sh`.\n\nSee GETTING_STARTED.md.\n')
    write(root,'ARCHITECTURE.md',f'# Architecture\n\nReact/Vite TypeScript frontend communicates with single-file FastAPI backend over REST.\nMenus: {", ".join(menus)}. Database choice: {a.database}.\nPorts: frontend 5173, backend 8000. Vite proxies `/api` to FastAPI.\n')
    write(root,'AGENTS.md','''# Agent guidance
    Keep this demonstrator minimal. Do not introduce layers or directories without a concrete need. Maintain one backend/main.py until complexity justifies splitting. Keep navigation in frontend/src/config.ts and colors there. Use REST endpoints under /api. Update docs when architecture changes. Run ./test.sh after changes; never claim unrun tests passed. Never overwrite or rewrite Git history without permission.
    ''')
    write(root,'CLAUDE.md','''# Claude Code guidance
    @AGENTS.md
    ''')
    write(root,'GETTING_STARTED.md','''# Getting started (beginner)
    
    ## What each part does
    - `frontend/`: React user interface, powered by Vite and TypeScript.
    - `frontend/src/main.tsx`: sidebar, header, placeholder page and navigation.
    - `frontend/src/config.ts`: app name, menu names and theme colors.
    - `frontend/src/style.css`: layout and appearance.
    - `frontend/tests/`: browser navigation checks with Playwright.
    - `backend/main.py`: the Python FastAPI server and REST endpoints.
    - `backend/pyproject.toml`: Python dependencies managed by uv.
    - `dev.sh`: runs both servers; `test.sh`: checks build, health and menus.
    - `AGENTS.md`: shared agent guidance; `CLAUDE.md`: Claude Code bridge to that guidance.
    - `ARCHITECTURE.md`: technical overview.
    - `.env.example`: sample environment variables; `.gitignore`: files Git should not track.
    
    ## Run on Linux / VS Code Remote SSH
    Install Node.js/npm, Python 3.11+, uv and Git. In `frontend`, run `npm install`; in `backend`, run `uv sync`. At repository root run `./dev.sh`. Forward port 5173 in VS Code and open it in your local browser. Port 8000 is only needed for direct API access. Stop with Ctrl+C.
    
    ## Add a menu
    Edit `menus` in `frontend/src/config.ts`. A placeholder page is generated automatically for each menu. Run `./test.sh`.
    
    ## Add a Python API endpoint
    Add to `backend/main.py`:
    ```python
    @app.get('/api/example')
    def example():
        return {'message': 'Hello from Python'}
    ```
    From React, call `fetch('/api/example').then(r => r.json())`. Vite forwards `/api` to FastAPI. For example, inside a React event handler:
    ```tsx
    const result = await fetch('/api/example');
    if (!result.ok) throw new Error('API request failed');
    const data = await result.json();
    console.log(data.message);
    ```
    FastAPI interactive API docs are at `http://127.0.0.1:8000/docs` on the remote host (forward port 8000 if needed).
    
    ## Test and troubleshoot
    First run `cd frontend && npx playwright install chromium` (Linux system browser libraries may also be required). Run `./test.sh` from the repo root. If `npm` is missing install Node.js; if `uv` is missing install uv; if Playwright cannot launch Chromium install required Linux browser dependencies. If a port is occupied stop the conflicting process. If the UI loads but APIs fail, check the FastAPI server and Vite proxy. Do not claim tests passed until all commands complete successfully.
    ''')
    if a.logo: shutil.copyfile(a.logo,root/'frontend'/'public'/'logo.png')
    if a.database=='postgres':
        write(root,'compose.yaml','''services:
          db:
            image: postgres:17
            environment:
              POSTGRES_USER: demo
              POSTGRES_PASSWORD: demo
              POSTGRES_DB: demo
            ports: ["127.0.0.1:5432:5432"]
            volumes: ["pgdata:/var/lib/postgresql/data"]
        volumes:
          pgdata:
        ''')
        write(root,'backend/alembic.ini','[alembic]\nscript_location = migrations\n')
        write(root,'backend/migrations/env.py','''import os
        from alembic import context
        from sqlalchemy import engine_from_config, pool
        from logging.config import fileConfig
        config=context.config
        config.set_main_option('sqlalchemy.url',os.environ['DATABASE_URL'])
        target_metadata=None
        def run_migrations_online():
            engine=engine_from_config(config.get_section(config.config_ini_section),prefix='sqlalchemy.',poolclass=pool.NullPool)
            with engine.connect() as connection:
                context.configure(connection=connection,target_metadata=target_metadata)
                with context.begin_transaction(): context.run_migrations()
        run_migrations_online()
        ''')
        write(root,'backend/migrations/script.py.mako','"""${message}"""\nrevision = ${repr(up_revision)}\ndown_revision = ${repr(down_revision)}\nbranch_labels = ${repr(branch_labels)}\ndepends_on = ${repr(depends_on)}\ndef upgrade():\n    pass\ndef downgrade():\n    pass\n')
        write(root,'backend/migrations/versions/.gitkeep','')
        with (root/'GETTING_STARTED.md').open('a') as f:f.write('\n## PostgreSQL\nRun `docker compose up -d db`, export `DATABASE_URL` from `.env.example`, and `cd backend && uv run alembic upgrade head`. Create revisions with `uv run alembic revision -m "change"`; fill upgrade/downgrade functions before applying. This starts with an empty schema. Do not commit real credentials.\n')
    print(f'Created {root}; menu count {len(menus)}; database={a.database}. Dependencies and browser tests NOT run.')
if __name__=='__main__':main()
