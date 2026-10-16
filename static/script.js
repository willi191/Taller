let lineChart, barChart;
const cop = n => new Intl.NumberFormat('es-CO',{style:'currency',currency:'COP',maximumFractionDigits:0}).format(n||0);
async function cargarDatos(){
  const estado=document.getElementById('estado'); estado.textContent='Actualizando…';
  try{
    const res=await fetch('/api/dashboard'); if(!res.ok) throw new Error('No se pudo consultar la API');
    const data=await res.json(), k=data.kpis, rows=data.registros;
    document.getElementById('ventas').textContent=cop(k.ventas);
    document.getElementById('gastos').textContent=cop(k.gastos);
    document.getElementById('ganancia').textContent=cop(k.ganancia);
    document.getElementById('clientes').textContent=new Intl.NumberFormat('es-CO').format(k.clientes);
    document.getElementById('margen').textContent=`Margen: ${k.margen.toFixed(1)}%`;
    document.getElementById('cambio').textContent=k.cambio_ventas===null?'Variación: requiere dos periodos':`Variación último periodo: ${k.cambio_ventas.toFixed(1)}%`;
    document.getElementById('analisis').innerHTML='';
    data.analisis.forEach(t=>{const li=document.createElement('li');li.textContent=t;document.getElementById('analisis').appendChild(li)});
    document.getElementById('tabla').innerHTML=rows.map(r=>`<tr><td>${escapeHtml(r.mes)}</td><td>${cop(r.ventas)}</td><td>${cop(r.gastos)}</td><td>${cop(r.ganancia)}</td><td>${r.clientes}</td></tr>`).join('') || '<tr><td colspan="5">Todavía no hay datos. Regístralos desde la consola.</td></tr>';
    const labels=rows.map(r=>r.mes);
    if(lineChart) lineChart.destroy();
    lineChart=new Chart(document.getElementById('lineChart'),{type:'line',data:{labels,datasets:[{label:'Ventas',data:rows.map(r=>r.ventas),borderColor:'#3157d5',backgroundColor:'#3157d520',fill:true,tension:.3},{label:'Gastos',data:rows.map(r=>r.gastos),borderColor:'#129b8a',backgroundColor:'#129b8a20',fill:false,tension:.3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom'}},scales:{y:{beginAtZero:true,ticks:{callback:v=>'$'+(v/1000000).toFixed(1)+' M'}}}}});
    if(barChart) barChart.destroy();
    barChart=new Chart(document.getElementById('barChart'),{type:'bar',data:{labels:['Ventas','Gastos','Ganancia'],datasets:[{label:'COP',data:[k.ventas,k.gastos,k.ganancia],backgroundColor:['#3157d5','#129b8a','#8b78df'],borderRadius:7}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{callback:v=>'$'+(v/1000000).toFixed(1)+' M'}}}}});
    estado.textContent=`${rows.length} periodo(s) cargado(s)`;
  }catch(e){estado.textContent='Error al cargar'; console.error(e)}
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
cargarDatos();