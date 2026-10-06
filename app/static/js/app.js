function toggleSidebar(){document.getElementById('sidebar').classList.toggle('open')}
setTimeout(()=>document.querySelectorAll('.flash').forEach(el=>{el.style.opacity='0';setTimeout(()=>el.remove(),300)}),5000);
