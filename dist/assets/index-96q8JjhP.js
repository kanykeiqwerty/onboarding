import{a as h}from"./index-DL7mrI6e.js";function u(){const s=document.createElement("div");s.className="min-h-screen bg-transparent";const e=document.createElement("div");e.className="container mx-auto px-4 py-8 max-w-4xl";const a=document.createElement("h1");a.className="text-2xl font-semibold text-slate-50 mb-6",a.textContent=h("sidebar.schedule"),e.appendChild(a);const d=document.createElement("p");d.className="text-sm text-slate-400 mb-6",d.textContent="Выберите нужный график, чтобы просмотреть смены и расписание сотрудников.",e.appendChild(d);const c=["График отдела продаж","График IT отдела","График HR отдела","График поддержки клиентов","Общий график компании"],t=document.createElement("div");t.className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6";let l=0;const r=()=>{t.innerHTML="",c.forEach((i,p)=>{const n=document.createElement("div");n.className=["p-4 rounded-2xl border transition cursor-pointer shadow-md","hover:shadow-indigo-500/50 hover:border-indigo-400",p===l?"bg-indigo-600 text-white border-indigo-500 shadow-indigo-500/40":"bg-slate-950/40 border-slate-800 text-slate-50"].join(" "),n.textContent=i,n.addEventListener("click",()=>{l=p,r(),m()}),t.appendChild(n)})};e.appendChild(t);const o=document.createElement("div");o.className="mt-8 bg-slate-950/40 border border-slate-800/70 rounded-2xl p-6 shadow-md shadow-slate-950/50",e.appendChild(o);const m=()=>{const i=c[l];o.innerHTML=`
      <h2 class="text-lg font-semibold text-slate-50 mb-2">${i}</h2>
      <p class="text-sm text-slate-400 mb-4">Здесь отображается подробное расписание выбранного графика.</p>
      <ul class="space-y-2 text-slate-100 text-sm">
        <li>Понедельник: 09:00 – 18:00</li>
        <li>Вторник: 09:00 – 18:00</li>
        <li>Среда: 09:00 – 18:00</li>
        <li>Четверг: 09:00 – 18:00</li>
        <li>Пятница: 09:00 – 18:00</li>
      </ul>
    `};return r(),m(),s.appendChild(e),s}export{u as SchedulePage};
