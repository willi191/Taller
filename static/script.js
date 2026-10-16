let lineChart, barChart, registrosActuales=[];
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
    document.getElementById('tabla').innerHTML=rows.map(r=>`<tr data-id="${r.id}"><td>${escapeHtml(r.mes)}</td><td>${cop(r.ventas)}</td><td>${cop(r.gastos)}</td><td>${cop(r.ganancia)}</td><td>${r.clientes}</td><td class="acciones"><button type="button" class="btn-sm" data-accion="editar" data-id="${r.id}">Editar</button><button type="button" class="btn-sm danger" data-accion="eliminar" data-id="${r.id}">Eliminar</button></td></tr>`).join('') || '<tr><td colspan="6">Todavía no hay datos. Agrégalos con el formulario de arriba.</td></tr>';
    registrosActuales=rows;
    const labels=rows.map(r=>r.mes);
    if(lineChart) lineChart.destroy();
    lineChart=new Chart(document.getElementById('lineChart'),{type:'line',data:{labels,datasets:[{label:'Ventas',data:rows.map(r=>r.ventas),borderColor:'#3157d5',backgroundColor:'#3157d520',fill:true,tension:.3},{label:'Gastos',data:rows.map(r=>r.gastos),borderColor:'#129b8a',backgroundColor:'#129b8a20',fill:false,tension:.3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom'}},scales:{y:{beginAtZero:true,ticks:{callback:v=>'$'+(v/1000000).toFixed(1)+' M'}}}}});
    if(barChart) barChart.destroy();
    barChart=new Chart(document.getElementById('barChart'),{type:'bar',data:{labels:['Ventas','Gastos','Ganancia'],datasets:[{label:'COP',data:[k.ventas,k.gastos,k.ganancia],backgroundColor:['#3157d5','#129b8a','#8b78df'],borderRadius:7}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{callback:v=>'$'+(v/1000000).toFixed(1)+' M'}}}}});
    estado.textContent=`${rows.length} periodo(s) cargado(s)`;
  }catch(e){estado.textContent='Error al cargar'; console.error(e)}
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}

/* ---------- Agregar / editar / eliminar ---------- */
const $=id=>document.getElementById(id);
const campos={mes:$('fMes'),ventas:$('fVentas'),gastos:$('fGastos'),clientes:$('fClientes')};

function mostrarMsg(texto,tipo){const m=$('msgForm');m.textContent=texto||'';m.className='msg'+(tipo?' '+tipo:'');}
function limpiarInvalidos(){Object.values(campos).forEach(c=>c.classList.remove('invalid'));}

function resetFormulario(){
  $('formRegistro').reset(); $('registroId').value='';
  $('formTitulo').textContent='Agregar registro';
  $('btnGuardar').textContent='Agregar';
  $('btnCancelar').hidden=true;
  document.querySelectorAll('tr.editando').forEach(tr=>tr.classList.remove('editando'));
  limpiarInvalidos();
}

function validarLocal(){
  limpiarInvalidos();
  const mes=campos.mes.value.trim();
  const v=campos.ventas.value, g=campos.gastos.value, c=campos.clientes.value;
  let err=null;
  if(!mes){campos.mes.classList.add('invalid');err='El periodo no puede estar vacío.';}
  else if(v===''||isNaN(v)||Number(v)<0){campos.ventas.classList.add('invalid');err='Las ventas deben ser un número no negativo.';}
  else if(g===''||isNaN(g)||Number(g)<0){campos.gastos.classList.add('invalid');err='Los gastos deben ser un número no negativo.';}
  else if(c===''||isNaN(c)||Number(c)<0||!Number.isInteger(Number(c))){campos.clientes.classList.add('invalid');err='Los clientes deben ser un entero no negativo.';}
  return err;
}

async function llamarApi(url,metodo,cuerpo){
  const res=await fetch(url,{method:metodo,headers:{'Content-Type':'application/json'},body:cuerpo?JSON.stringify(cuerpo):undefined});
  const data=await res.json().catch(()=>({}));
  if(!res.ok) throw new Error(data.error||'Error inesperado del servidor');
  return data;
}

$('formRegistro').addEventListener('submit',async e=>{
  e.preventDefault();
  const err=validarLocal(); if(err){mostrarMsg(err,'err');return;}
  const id=$('registroId').value, editando=id!=='';
  const cuerpo={mes:campos.mes.value.trim(),ventas:campos.ventas.value,gastos:campos.gastos.value,clientes:campos.clientes.value};
  $('btnGuardar').disabled=true;
  try{
    await llamarApi(editando?`/api/registros/${id}`:'/api/registros',editando?'PUT':'POST',cuerpo);
    resetFormulario(); await cargarDatos();
    mostrarMsg(editando?'Registro actualizado.':'Registro agregado.','ok');
  }catch(ex){mostrarMsg(ex.message,'err');}
  finally{$('btnGuardar').disabled=false;}
});

$('btnCancelar').addEventListener('click',()=>{resetFormulario();mostrarMsg('');});

$('tabla').addEventListener('click',async e=>{
  const btn=e.target.closest('button[data-accion]'); if(!btn) return;
  const id=Number(btn.dataset.id), r=registrosActuales.find(x=>x.id===id); if(!r) return;
  if(btn.dataset.accion==='editar'){
    resetFormulario(); mostrarMsg('');
    $('registroId').value=id;
    campos.mes.value=r.mes; campos.ventas.value=r.ventas; campos.gastos.value=r.gastos; campos.clientes.value=r.clientes;
    $('formTitulo').textContent=`Editando: ${r.mes}`;
    $('btnGuardar').textContent='Guardar cambios';
    $('btnCancelar').hidden=false;
    btn.closest('tr').classList.add('editando');
    $('panelForm').scrollIntoView({behavior:'smooth',block:'center'});
    campos.mes.focus();
  }else if(btn.dataset.accion==='eliminar'){
    if(!confirm(`¿Eliminar el registro de «${r.mes}»? Esta acción no se puede deshacer.`)) return;
    try{
      await llamarApi(`/api/registros/${id}`,'DELETE');
      if($('registroId').value===String(id)) resetFormulario();
      await cargarDatos(); mostrarMsg('Registro eliminado.','ok');
    }catch(ex){mostrarMsg(ex.message,'err'); await cargarDatos();}
  }
});

cargarDatos();