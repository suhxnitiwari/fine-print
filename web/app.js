// Fine Print in the browser: Pyodide runs the same fineprint package the command line uses.
(() => {
    const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/';
    const FILES = ['__init__.py', 'parse.py', 'catalog.py', 'knowledge.py', 'base.py', 'decode.py', 'web.py', 'data/cosing.json'];
    const SAMPLES = [
        ['Niacinamide serum', 'niacinamide-serum'], ['Glow toner', 'glow-toner'], ['Retinol night cream', 'retinol-night-cream'],
        ['Vitamin C serum', 'vitamin-c-serum'], ['Hero-dusting cream', 'hero-dusting-cream'],
        ['Long-wear foundation', 'long-wear-foundation'], ['Skin tint', 'skin-tint'], ['Balm foundation', 'balm-foundation'],
    ];
    const SAVED = 'fineprint-labels';
    const $ = s => document.querySelector(s);
    const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
    const pct = n => n >= 10 ? Math.round(n) + '%' : (+n.toFixed(1)) + '%';

    let py = null, decodeJson = null;

    // ---------- tabs ----------
    document.querySelectorAll('nav button').forEach(b => b.addEventListener('click', () => {
        document.querySelectorAll('nav button').forEach(x => x.setAttribute('aria-selected', x === b));
        $('#decode').hidden = b.dataset.tab !== 'decode';
        $('#how').hidden = b.dataset.tab !== 'how';
    }));

    // ---------- the labels you paste ----------
    const labels = $('#labels');

    function addLabel(name = '', text = '', foundation = false) {
        const card = document.createElement('div');
        card.className = 'label-card';
        card.innerHTML = `
            <div class="label-top">
                <input type="text" aria-label="Product name" placeholder="Product name">
                <button class="remove" type="button" aria-label="Remove this product">Remove</button>
            </div>
            <textarea aria-label="Ingredient list" placeholder="Ingredients: Aqua, Niacinamide, Glycerin, …"></textarea>
            <label class="check"><input type="checkbox"> This is a foundation or tint</label>`;
        card.querySelector('input[type=text]').value = name;
        card.querySelector('textarea').value = text;
        card.querySelector('input[type=checkbox]').checked = foundation;
        card.querySelector('.remove').addEventListener('click', () => { card.remove(); refreshRemove(); save(); });
        card.addEventListener('input', save);
        labels.appendChild(card);
        refreshRemove();
        return card;
    }

    function refreshRemove() {
        const cards = labels.querySelectorAll('.label-card');
        cards.forEach(c => { c.querySelector('.remove').hidden = cards.length < 2; });
        labels.style.display = 'grid';
        labels.style.gap = '14px';
    }

    function read() {
        return [...labels.querySelectorAll('.label-card')].map((c, n) => ({
            name: c.querySelector('input[type=text]').value.trim() || `Product ${n + 1}`,
            text: c.querySelector('textarea').value,
            foundation: c.querySelector('input[type=checkbox]').checked,
        }));
    }

    function save() {
        try { localStorage.setItem(SAVED, JSON.stringify(read())); } catch (e) { /* private mode: fine */ }
    }

    async function sample(file) {
        const r = await fetch(`examples/${file}.txt`);
        return (await r.text()).trim();
    }

    $('#add').addEventListener('click', () => { addLabel().querySelector('textarea').focus(); save(); });

    SAMPLES.forEach(([title, file]) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.textContent = title;
        b.addEventListener('click', async () => {
            // fill the first empty label, or the last one
            const cards = [...labels.querySelectorAll('.label-card')];
            const card = cards.find(c => !c.querySelector('textarea').value.trim()) || cards[cards.length - 1];
            card.querySelector('input[type=text]').value = title;
            card.querySelector('textarea').value = await sample(file);
            card.querySelector('input[type=checkbox]').checked = /foundation|tint/.test(file);
            save();
            if (decodeJson) run();
        });
        $('#samples').appendChild(b);
    });

    // ---------- the answers ----------
    function render(data) {
        const out = [];
        if (data.products.length > 1) {
            out.push(`<section class="together"><p class="eyebrow">Your routine</p><h2>Can I use these together?</h2>`);
            if (!data.clashes.length) out.push(`<p class="all-clear">Yes. Nothing in this routine fights.</p>`);
            data.clashes.forEach(c => out.push(`
                <div class="clash">
                    <strong>${esc(c.a)}'s ${esc(c.aIngredient)} + ${esc(c.b)}'s ${esc(c.bIngredient)}</strong>
                    <p>${esc(c.why)}</p>
                    <p class="instead">${esc(c.instead)}</p>
                </div>`));
            out.push(`</section>`);
        }
        data.products.forEach(p => out.push(product(p)));
        $('#results').innerHTML = out.join('') ||
            `<div class="placeholder">Paste an ingredient list, or try one of the examples.</div>`;
    }

    function product(p) {
        const f = p.fragrance;
        const tiles = [`
            <div class="tile"><div class="q">Fragrance-free?</div>
                <div class="a ${f.free ? 'yes' : 'no'}">${f.free ? 'Yes' : 'No'}</div>
                <p>${esc(f.verdict.replace(/^Yes[.,]?\s*/, ''))}</p>
                ${f.culprits.length && !f.free ? `<ul class="culprits">${f.culprits.map(c => `<li>${esc(c)}</li>`).join('')}</ul>` : ''}
            </div>`, `
            <div class="tile"><div class="q">The 1% line</div>
                ${p.line ? `<div class="a small">at #${p.line}</div>
                    <p>${esc(p.lineName)}. The ${p.aboveCount} ingredients above it make up at least ${p.aboveShare}% of the bottle.</p>`
                         : `<div class="a small">Not shown</div><p>No preservative or thickener marks it, so the caps come from order alone.</p>`}
            </div>`];
        if (p.base) tiles.push(`
            <div class="tile"><div class="q">Base</div>
                <div class="a small" style="text-transform:capitalize">${esc(p.base.kind)}</div>
                <p>${esc(p.base.emulsion)}, ${esc(p.base.confidence)} confidence</p>
            </div>`);

        const heroes = p.heroes.length ? `<h3>What's doing the work</h3><div class="heroes">${p.heroes.map(h => `
            <div class="hero">
                <span class="mark ${h.verdict === 'too little' ? 'bad' : 'ok'}" aria-label="${esc(h.verdict)}">${h.verdict === 'too little' ? '✗' : '✓'}</span>
                <div><b>${esc(h.name[0].toUpperCase() + h.name.slice(1))}</b><p>${esc(h.note)}</p></div>
            </div>`).join('')}</div>` : '';

        const rows = [];
        let lineDrawn = false, mayDrawn = false;
        p.items.forEach(i => {
            if (i.mayContain && !mayDrawn) { rows.push(`<div class="may">May contain: shade colorants, outside the order</div>`); mayDrawn = true; }
            if (i.below && !lineDrawn) { rows.push(`<div class="line-rule">The 1% line</div>`); lineDrawn = true; }
            const cls = ['ing'];
            if (i.below) cls.push('below');
            if (i.hero) cls.push(i.hero === 'too little' ? 'hero-bad' : 'hero-ok');
            else if (i.scent) cls.push('scent');
            else if (i.how === 'fuzzy') cls.push('guess');
            if (!i.known) cls.push('unknown');
            const width = i.atMost == null ? 0 : Math.max(1.5, i.atMost);
            rows.push(`
                <div class="${cls.join(' ')}">
                    <span class="pos">${i.mayContain ? '+/-' : '#' + i.pos}</span>
                    <span class="nm"><span>${esc(i.known ? i.name : i.printed)}</span>
                        <span class="jobs">${i.known ? esc(i.jobs.join(' · ') || '—') : 'not in the EU database'}${i.how === 'fuzzy' ? ` · printed "${esc(i.printed)}"` : ''}</span></span>
                    <span class="bar">${i.atMost == null ? '' : `<i style="width:${width}%"></i>`}</span>
                    <span class="cap">${i.atMost == null ? '' : '≤' + pct(i.atMost)}</span>
                </div>`);
        });

        const base = p.base ? `
            <div class="base">
                <h3>What base is this?</h3>
                <div class="kind">${esc(p.base.kind)} <small>${esc(p.base.emulsion)} · ${esc(p.base.confidence)} confidence</small></div>
                <p>${esc(p.base.rule)}</p>
                ${p.base.heat ? `<p class="heat">In heat: ${esc(p.base.heat)}</p>` : ''}
                ${p.base.evidence.length ? `<ol>${p.base.evidence.slice(0, 6).map(e => `<li>${esc(e)}</li>`).join('')}</ol>` : ''}
            </div>` : '';

        return `
            <section>
                <p class="eyebrow">Decoded</p>
                <h2>${esc(p.name)}<small>${p.count} ingredients${p.colorants ? ` + ${p.colorants} shade colorants` : ''}</small></h2>
                <div class="verdicts">${tiles.join('')}</div>
                ${heroes}
                <h3>The label, decoded</h3>
                <div class="label">${rows.join('')}</div>
                <p class="note">Bars show the most each ingredient can be, from its place on the list.</p>
                ${base}
            </section>`;
    }

    // ---------- Python ----------
    const go = $('#go'), status = $('#status');

    function run() {
        if (!decodeJson) return;
        try {
            render(JSON.parse(decodeJson(JSON.stringify(read()))));
        } catch (e) {
            console.error(e);
            status.textContent = "Something on that label tripped me up. Check it's one list, separated by commas.";
        }
    }
    go.addEventListener('click', run);

    function loadScript(src) {
        return new Promise((resolve, reject) => {
            const s = document.createElement('script');
            s.src = src; s.onload = resolve; s.onerror = reject;
            document.head.appendChild(s);
        });
    }

    async function boot() {
        try {
            await loadScript(PYODIDE + 'pyodide.js');
            py = await loadPyodide({ indexURL: PYODIDE });
            py.FS.mkdirTree('/home/pyodide/fineprint/data');
            await Promise.all(FILES.map(async f => {
                const r = await fetch('fineprint/' + f, { cache: 'no-cache' });  // never mix old and new files after an update
                if (!r.ok) throw new Error(f);
                py.FS.writeFile('/home/pyodide/fineprint/' + f, await r.text());
            }));
            py.runPython('import sys; sys.path.insert(0, "/home/pyodide")\nfrom fineprint.web import decode_json, stats');
            decodeJson = py.globals.get('decode_json');
            const n = JSON.parse(py.globals.get('stats')()).ingredients;
            go.disabled = false;
            status.textContent = `Ready. ${n.toLocaleString()} EU ingredients loaded, and nothing you paste leaves your device.`;
            run();
        } catch (e) {
            console.error(e);
            status.textContent = "Python couldn't start. Check your connection and reload.";
        }
    }

    // ---------- start ----------
    (async () => {
        let saved = null;
        try { saved = JSON.parse(localStorage.getItem(SAVED) || 'null'); } catch (e) { /* ignore */ }
        if (saved && saved.some(s => s.text && s.text.trim())) {
            saved.forEach(s => addLabel(s.name, s.text, s.foundation));
        } else {
            addLabel('Hero-dusting cream', await sample('hero-dusting-cream').catch(() => ''));
        }
        boot();
    })();

    if ('serviceWorker' in navigator && location.protocol === 'https:') navigator.serviceWorker.register('sw.js').catch(() => {});
})();
