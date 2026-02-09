import{f as j,t as K,s as A,S as z,u as G,a as l,g as P,o as q}from"./index-DL7mrI6e.js";const M=[{id:"news-1",title:"Запуск новой программы онбординга",description:"Мы полностью обновили маршрут для стажёров: короткие модули, менторы и живые созвоны.",text:"Мы запускаем обновлённую программу онбординга для всех новых сотрудников. Теперь первые две недели будут состоять из bite-size модулей, ежедневных синков с ментором и практических задач на реальных сценариях компании. Цель программы — сократить время адаптации и помочь быстрее почувствовать себя частью команды.",image:"https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1200&q=80",date:j("2024-02-10"),author:"HR команда"},{id:"news-2",title:"Открытие внутреннего портала знаний",description:"Все гайды, регламенты и чек-листы переехали в единое пространство.",text:"Мы запустили внутренний портал знаний, где собрали все актуальные регламенты, инструкции и FAQ. Теперь вам не нужно спрашивать коллег, где лежит тот или иной документ — всё доступно в пару кликов. Портал будет постоянно пополняться материалами от экспертов из разных команд.",image:"https://images.unsplash.com/photo-1522202195461-41a532ee39dd?auto=format&fit=crop&w=1200&q=80",date:j("2024-02-05"),author:"Команда обучения"},{id:"news-3",title:"Встреча с основателем компании",description:"Ежемесячный open talk: задайте любой вопрос о стратегии и культуре.",text:"В следующую среду пройдёт открытая встреча с основателем компании. Мы поговорим о том, куда движется продукт, какие ценности для нас ключевые и чего мы ждём от стажёров. У вас будет возможность задать свои вопросы в прямом эфире или анонимно через форму.",image:"https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",date:j("2024-01-28"),author:"PR отдел"}];function I(){const i=document.createElement("section");i.className="mt-10 space-y-4 card-appear";const c=document.createElement("div");c.className="flex items-center justify-between gap-3",c.innerHTML=`
    <div>
      <h2 class="text-lg font-semibold text-slate-50 tracking-tight">
        Актуальные новости компании
      </h2>
      <p class="text-xs text-slate-400 mt-1">
        Будьте в курсе важных событий и изменений — всё в одном месте.
      </p>
    </div>
  `;const s=document.createElement("div");s.className="relative group rounded-2xl border border-slate-800/80 bg-slate-950/60 shadow-xl shadow-slate-950/70 overflow-hidden";const p=document.createElement("div");p.className="relative w-full h-72 md:h-80";const v=document.createElement("div");v.className="absolute bottom-4 inset-x-0 flex items-center justify-center gap-2 z-20";let o=0,m=null;const u=[],y=[],h=(e,t)=>{const d=document.createElement("article");return d.className="absolute inset-0 opacity-0 pointer-events-none transition-opacity duration-500 ease-out",d.innerHTML=`
      <div class="flex flex-col md:flex-row h-full">
        <div class="relative md:w-7/12 h-40 md:h-full overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-tr from-indigo-500/10 via-slate-900/40 to-emerald-400/10"></div>
          <img
            src="${e.image}"
            alt="${e.title}"
            class="w-full h-full object-cover transform scale-[1.02] transition-transform duration-700 group-hover:scale-105"
            loading="lazy"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-950/20 to-transparent"></div>
          <div class="absolute left-4 bottom-4 flex items-center gap-2 text-xs text-slate-200">
            <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-slate-950/70 border border-slate-700/80">
              <span class="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow shadow-emerald-500/60"></span>
              <span>${e.date}</span>
            </span>
            <span class="text-slate-500">·</span>
            <span class="text-slate-300">${e.author}</span>
          </div>
        </div>
        <div class="md:w-5/12 p-5 md:p-6 flex flex-col justify-between">
          <div class="space-y-3">
            <h3 class="text-base md:text-lg font-semibold text-slate-50 line-clamp-2">
              ${e.title}
            </h3>
            <p class="text-sm text-slate-400 line-clamp-4 md:line-clamp-5">
              ${K(e.description,160)}
            </p>
          </div>
          <div class="mt-4 flex items-center justify-between text-xs text-slate-400">
            <span>Нажмите на карточку, чтобы прочитать полностью</span>
            <span class="inline-flex items-center gap-1 text-indigo-300">
              <span>Подробнее</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </span>
          </div>
        </div>
      </div>
    `,d.addEventListener("click",()=>{H(t)}),d},C=()=>{u.forEach((e,t)=>{t===o?(e.classList.remove("opacity-0","pointer-events-none"),e.classList.add("opacity-100")):(e.classList.add("opacity-0","pointer-events-none"),e.classList.remove("opacity-100"))}),y.forEach((e,t)=>{t===o?(e.classList.add("bg-slate-50","w-6"),e.classList.remove("bg-slate-600","w-2.5")):(e.classList.add("bg-slate-600","w-2.5"),e.classList.remove("bg-slate-50","w-6"))})},n=e=>{const t=M.length;o=(e+t)%t,C(),w&&N(o)},r=()=>n(o+1),f=()=>n(o-1),$=()=>{m||(m=setInterval(r,5e3))},B=()=>{m&&(clearInterval(m),m=null)};M.forEach((e,t)=>{const d=h(e,t);u.push(d),p.appendChild(d);const x=document.createElement("button");x.type="button",x.className="h-1.5 rounded-full bg-slate-600 transition-all duration-200 hover:bg-slate-200 focus:outline-none",x.addEventListener("click",L=>{L.stopPropagation(),n(t)}),y.push(x),v.appendChild(x)});const g=document.createElement("button");g.type="button",g.className="absolute inset-y-0 left-0 w-1/2 flex items-center justify-start text-slate-50/0 bg-gradient-to-r from-slate-950/0 via-slate-950/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300",g.innerHTML=`
    <div class="ml-3 inline-flex h-9 w-9 items-center justify-center rounded-full border border-slate-700/70 bg-slate-950/80 text-slate-300 shadow-sm shadow-slate-900/80">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </div>
  `,g.addEventListener("click",e=>{e.stopPropagation(),f()});const b=document.createElement("button");b.type="button",b.className="absolute inset-y-0 right-0 w-1/2 flex items-center justify-end text-slate-50/0 bg-gradient-to-l from-slate-950/0 via-slate-950/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300",b.innerHTML=`
    <div class="mr-3 inline-flex h-9 w-9 items-center justify-center rounded-full border border-slate-700/70 bg-slate-950/80 text-slate-300 shadow-sm shadow-slate-900/80">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </div>
  `,b.addEventListener("click",e=>{e.stopPropagation(),r()}),s.appendChild(p),s.appendChild(g),s.appendChild(b),s.appendChild(v),s.addEventListener("mouseenter",B),s.addEventListener("mouseleave",$),i.appendChild(c),i.appendChild(s);let w=!1,a=null;const E=()=>{a&&(w=!1,a.classList.add("opacity-0","pointer-events-none"),setTimeout(()=>{a&&!w&&(a.remove(),a=null)},200))},N=e=>{const t=M[e];a||(a=document.createElement("div"),a.className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-xl transition-opacity duration-200",document.body.appendChild(a)),a.innerHTML=`
      <div class="absolute inset-0" data-news-backdrop></div>
      <div class="relative w-full max-w-3xl mx-4 md:mx-0 rounded-2xl border border-slate-700/80 bg-slate-950/95 shadow-2xl shadow-slate-950/80 overflow-hidden card-appear">
        <div class="relative h-56 md:h-64 overflow-hidden">
          <img
            src="${t.image}"
            alt="${t.title}"
            class="w-full h-full object-cover transform scale-[1.03]"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent"></div>
          <button
            type="button"
            class="absolute top-3 right-3 inline-flex h-8 w-8 items-center justify-center rounded-full bg-slate-950/80 border border-slate-700 text-slate-300 hover:text-slate-50 hover:border-slate-500 transition-colors"
            data-news-close
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <div class="absolute left-4 bottom-3 flex flex-wrap items-center gap-2 text-xs text-slate-200">
            <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-slate-950/80 border border-slate-700/80">
              <span class="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow shadow-emerald-500/60"></span>
              <span>${t.date}</span>
            </span>
            <span class="text-slate-500 hidden sm:inline">·</span>
            <span class="text-slate-300 hidden sm:inline">${t.author}</span>
          </div>
        </div>
        <div class="p-5 md:p-6 space-y-3 max-h-[60vh] overflow-y-auto">
          <h3 class="text-lg md:text-xl font-semibold text-slate-50">${t.title}</h3>
          <p class="text-sm md:text-base text-slate-300 whitespace-pre-line leading-relaxed">
            ${t.text}
          </p>
        </div>
        <div class="flex items-center justify-between px-5 md:px-6 pb-4 text-xs text-slate-500">
          <span>Используйте стрелки или свайп для переключения новостей</span>
          <button
            type="button"
            class="hidden sm:inline-flex items-center gap-1 text-slate-300 hover:text-slate-50 transition-colors"
            data-news-close
          >
            <span>Закрыть</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <!-- Стрелки внутри лайтбокса -->
        <button
          type="button"
          class="absolute inset-y-0 left-0 w-1/2 flex items-center justify-start text-slate-50/0
                 bg-gradient-to-r from-slate-950/0 via-slate-950/40 to-transparent"
          data-news-prev
        >
          <div class="ml-3 inline-flex h-9 w-9 items-center justify-center rounded-full border border-slate-700/70 bg-slate-950/90 text-slate-300 shadow-sm shadow-slate-900/80">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </div>
        </button>
        <button
          type="button"
          class="absolute inset-y-0 right-0 w-1/2 flex items-center justify-end text-slate-50/0
                 bg-gradient-to-l from-slate-950/0 via-slate-950/40 to-transparent"
          data-news-next
        >
          <div class="mr-3 inline-flex h-9 w-9 items-center justify-center rounded-full border border-slate-700/70 bg-slate-950/90 text-slate-300 shadow-sm shadow-slate-900/80">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </button>
      </div>
    `;const d=a.querySelector("[data-news-backdrop]"),x=a.querySelectorAll("[data-news-close]"),L=a.querySelector("[data-news-prev]"),S=a.querySelector("[data-news-next]");d&&d.addEventListener("click",E),x.forEach(k=>{k.addEventListener("click",E)}),L&&L.addEventListener("click",k=>{k.stopPropagation(),f()}),S&&S.addEventListener("click",k=>{k.stopPropagation(),r()})},H=e=>{w=!0,o=e,N(o)};return document.addEventListener("keydown",e=>{w&&(e.key==="Escape"&&E(),e.key==="ArrowRight"&&r(),e.key==="ArrowLeft"&&f())}),C(),$(),i}const T={title:"Добро пожаловать на платформу онбординга",subtitle:"С этой страницы вы быстро поймёте, что делать в первые дни: от заполнения профиля до первых задач.",ctaLabel:"Перейти к инструкции"},O=z.WELCOME_CONFIG;function F(){const i=A.get(O);return i?{...T,...i}:T}function W(){const i=document.createElement("div");i.className="min-h-screen bg-transparent";const c=G.getUser(),s=document.createElement("div");s.className="container mx-auto px-4 py-10";const p=document.createElement("div");p.className="mb-10 card-appear";const v=()=>{c?p.innerHTML=`
        <h1 class="text-4xl font-semibold text-slate-50 mb-3 tracking-tight">
          ${l("main.welcomeUserTitle",{name:c.firstName})}
        </h1>
        <p class="text-base text-slate-400 flex items-center gap-2">
          <span class="inline-flex items-center gap-1 rounded-full bg-slate-900/60 border border-slate-700 px-2 py-0.5 text-xs uppercase tracking-wide text-slate-300">
            <span class="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow shadow-emerald-500/60"></span>
            ${P(c.role)}
          </span>
          <span class="text-slate-500">·</span>
          <span>${l("main.welcomeGuestSubtitle")}</span>
        </p>
      `:p.innerHTML=`
        <h1 class="text-4xl font-semibold text-slate-50 mb-4 tracking-tight">
          ${l("main.welcomeGuestTitle")}
        </h1>
        <p class="text-base text-slate-400 mb-6 max-w-xl">
          ${l("main.welcomeGuestSubtitle")}
        </p>
        <a
          href="/auth"
          class="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-indigo-500 via-violet-500 to-emerald-400 px-6 py-2.5 text-sm font-semibold text-slate-950 shadow-md shadow-indigo-500/40 hover:shadow-lg hover:shadow-emerald-400/40 transition-all"
        >
          <span>${l("main.welcomeGuestCta")}</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </a>
      `},o=document.createElement("div");o.className="card-appear";const m=()=>{const{title:n,subtitle:r,ctaLabel:f}=F();o.innerHTML=`
      <div class="mt-4 rounded-2xl border border-slate-800/80 bg-slate-950/60 shadow-lg shadow-slate-950/70 p-4 md:p-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div class="flex items-start gap-3 md:gap-4">
          <div class="mt-1 inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 via-violet-500 to-emerald-400 text-slate-950 shadow-md shadow-indigo-500/40">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h2 class="text-sm md:text-base font-semibold text-slate-50 mb-1">
              ${n}
            </h2>
            <p class="text-xs md:text-sm text-slate-400 max-w-xl">
              ${r}
            </p>
          </div>
        </div>
        <div class="flex items-center justify-end md:justify-center">
          <a
            href="/instructions"
            class="inline-flex items-center gap-2 rounded-full bg-slate-900/80 border border-slate-700/80 px-4 py-2 text-xs md:text-sm font-medium text-slate-100 hover:border-indigo-400 hover:text-slate-50 hover:bg-slate-900 transition-colors"
          >
            <span>${f}</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </a>
        </div>
      </div>
    `},u=document.createElement("div");u.className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6";const y=[{icon:`<svg class="w-12 h-12 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
      </svg>`,titleKey:"main.features.courses.title",descriptionKey:"main.features.courses.description"},{icon:`<svg class="w-12 h-12 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>`,titleKey:"main.features.progress.title",descriptionKey:"main.features.progress.description"},{icon:`<svg class="w-12 h-12 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
      </svg>`,titleKey:"main.features.certificates.title",descriptionKey:"main.features.certificates.description"}],h=()=>{u.innerHTML="",y.forEach(n=>{const r=document.createElement("div");r.className="card-appear bg-slate-950/40 border border-slate-800/80 p-6 rounded-2xl shadow-lg shadow-slate-950/60 hover:border-indigo-500/60 hover:shadow-indigo-500/30 transition-all duration-200",r.innerHTML=`
        <div class="mb-4">${n.icon}</div>
        <h3 class="text-lg font-semibold mb-2 text-slate-50">${l(n.titleKey)}</h3>
        <p class="text-sm text-slate-400">${l(n.descriptionKey)}</p>
      `,u.appendChild(r)})};if(h(),c){const n=document.createElement("div");n.className="mt-10 card-appear bg-slate-950/40 border border-slate-800/80 rounded-2xl shadow-lg shadow-slate-950/60 p-6",n.innerHTML=`
        <h2 class="text-xl font-semibold mb-4 text-slate-50">${l("main.stats.title")}</h2>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="text-center rounded-xl bg-slate-900/80 border border-slate-800/80 px-4 py-5">
            <div class="text-3xl font-semibold text-indigo-400 mb-1">0</div>
            <div class="text-xs text-slate-400 uppercase tracking-wide">${l("main.stats.activeCourses")}</div>
          </div>
          <div class="text-center rounded-xl bg-slate-900/80 border border-slate-800/80 px-4 py-5">
            <div class="text-3xl font-semibold text-emerald-400 mb-1">0</div>
            <div class="text-xs text-slate-400 uppercase tracking-wide">${l("main.stats.completedLessons")}</div>
          </div>
          <div class="text-center rounded-xl bg-slate-900/80 border border-slate-800/80 px-4 py-5">
            <div class="text-3xl font-semibold text-violet-400 mb-1">0</div>
            <div class="text-xs text-slate-400 uppercase tracking-wide">${l("main.stats.certificates")}</div>
          </div>
          <div class="text-center rounded-xl bg-slate-900/80 border border-slate-800/80 px-4 py-5">
            <div class="text-3xl font-semibold text-amber-300 mb-1">0%</div>
            <div class="text-xs text-slate-400 uppercase tracking-wide">${l("main.stats.totalProgress")}</div>
          </div>
        </div>
      `,s.appendChild(n)}v(),m(),h(),s.appendChild(p),s.appendChild(o),s.appendChild(u);const C=I();return s.appendChild(C),i.appendChild(s),q(()=>{v(),renderStats(),h(),m()}),i}export{W as MainPage};
