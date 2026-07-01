let pasos = [];
let torres = { A: [], B: [], C: [] };
let intervalo = null;
let paso = 0;
let n = 3;

function anchoDiscos(num) {
    const min = 40, max = 150;
    return min + ((max - min) * (num - 1) / (n - 1 || 1));
}

function renderizar() {
    ['A', 'B', 'C'].forEach(t => {
        const cont = document.getElementById(`discos${t}`);
        cont.innerHTML = '';
        torres[t].forEach(num => {
            const d = document.createElement('div');
            d.className = 'disco';
            d.style.width = anchoDiscos(num) + 'px';
            cont.appendChild(d);
        });
    });
}

function generarPasos(n, origen, destino, aux) {
    if (n === 1) { pasos.push([origen, destino]); return; }
    generarPasos(n - 1, origen, aux, destino);
    pasos.push([origen, destino]);
    generarPasos(n - 1, aux, destino, origen);
}

function iniciar() {
    clearInterval(intervalo);
    n = parseInt(document.getElementById('numDiscos').value);
    torres = { A: [], B: [], C: [] };
    for (let i = n; i >= 1; i--) torres.A.push(i);
    pasos = [];
    paso = 0;
    generarPasos(n, 'A', 'C', 'B');
    document.getElementById('movTotal').textContent = pasos.length;
    document.getElementById('movActual').textContent = 0;
    renderizar();

    intervalo = setInterval(() => {
        if (paso >= pasos.length) { clearInterval(intervalo); return; }
        const [de, a] = pasos[paso];
        torres[a].push(torres[de].pop());
        paso++;
        document.getElementById('movActual').textContent = paso;
        renderizar();
    }, 700);
}

function reiniciar() {
    clearInterval(intervalo);
    n = parseInt(document.getElementById('numDiscos').value);
    torres = { A: [], B: [], C: [] };
    for (let i = n; i >= 1; i--) torres.A.push(i);
    pasos = [];
    paso = 0;
    document.getElementById('movActual').textContent = 0;
    document.getElementById('movTotal').textContent = 0;
    renderizar();
}

reiniciar();
