import{a as o}from"./index-DL7mrI6e.js";function p(){const t=document.createElement("div");t.className="min-h-screen bg-transparent";const e=document.createElement("div");e.className="container mx-auto px-4 py-8 max-w-4xl";const s=document.createElement("h1");s.className="text-2xl font-semibold text-slate-50 mb-6",s.textContent=o("sidebar.onboarding"),e.appendChild(s);const a=document.createElement("div");a.className="mb-8",a.innerHTML=`
    <p class="text-sm text-slate-400 mb-2">Прогресс онбординга</p>
    <div class="w-full bg-slate-800 rounded-full h-3">
      <div class="bg-indigo-500 h-3 rounded-full" style="width: 45%"></div>
    </div>
    <p class="text-xs text-slate-500 mt-1">Шаг 2 из 5</p>
  `,e.appendChild(a);const i=[{title:"Ознакомление с компанией",desc:"Прочитайте правила, миссию и ценности компании."},{title:"Настройка аккаунтов",desc:"Создайте учетные записи для почты, Jira и Slack."},{title:"Тренинг по продукту",desc:"Посмотрите обучающие видео о продукте и его функционале."},{title:"Знакомство с командой",desc:"Познакомьтесь с коллегами и руководителем отдела."},{title:"Первое задание",desc:"Выполните тестовое задание, чтобы закрепить знания."}],l=document.createElement("div");l.className="grid grid-cols-1 md:grid-cols-2 gap-6",i.forEach((c,r)=>{const n=document.createElement("div");n.className="bg-slate-950/40 border border-slate-800/70 rounded-2xl p-4 shadow-md shadow-slate-950/50 hover:shadow-indigo-500/40 transition cursor-pointer",n.innerHTML=`
      <h3 class="text-lg font-semibold text-slate-50 mb-1">${r+1}. ${c.title}</h3>
      <p class="text-sm text-slate-400">${c.desc}</p>
    `,l.appendChild(n)}),e.appendChild(l);const d=document.createElement("div");return d.className="mt-8",d.innerHTML=`
    <p class="text-sm text-slate-400 mb-2">Обучающее видео</p>
    <div class="w-full h-56 md:h-96 bg-slate-800 rounded-xl flex items-center justify-center text-slate-500">
      Видео пока не подключено
    </div>
  `,e.appendChild(d),t.appendChild(e),t}export{p as OnboardingPage};
