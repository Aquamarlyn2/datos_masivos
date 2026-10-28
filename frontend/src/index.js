import './styles.css';

document.getElementById('btn-salud').addEventListener('click', async () => {
  const salida = document.getElementById('salida');
  salida.textContent = 'Consultando…';
  try {
    const r = await fetch('/api/health');
    salida.textContent = JSON.stringify(await r.json(), null, 2);
  } catch (e) {
    salida.textContent = 'Error al consultar la API: ' + e.message;
  }
});
