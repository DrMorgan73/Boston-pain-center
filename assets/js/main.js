/* Boston Pain Center — site interactions v1.0 */
(function(){
"use strict";

/* ---------- mobile menu ---------- */
var menuBtn=document.querySelector('.menu-btn'), mainNav=document.getElementById('mainNav');
if(menuBtn&&mainNav){menuBtn.addEventListener('click',function(){mainNav.classList.toggle('open');});}

/* ---------- language toggle (EN/ES) ---------- */
var LANG_KEY='bpc-lang';
function currentLang(){
  var saved=null;
  try{saved=localStorage.getItem(LANG_KEY);}catch(e){}
  if(saved==='en'||saved==='es')return saved;
  return document.documentElement.getAttribute('data-default-lang')||'es';
}
function applyLang(l){
  document.querySelectorAll('[data-en]').forEach(function(el){
    var v=el.getAttribute('data-'+l);
    if(v!==null)el.textContent=v;
  });
  document.querySelectorAll('[data-en-ph]').forEach(function(el){
    var v=el.getAttribute('data-'+l+'-ph');
    if(v!==null)el.setAttribute('placeholder',v);
  });
  document.querySelectorAll('[data-en-aria]').forEach(function(el){
    var v=el.getAttribute('data-'+l+'-aria');
    if(v!==null)el.setAttribute('aria-label',v);
  });
  document.documentElement.setAttribute('lang',l);
  document.querySelectorAll('.lang-toggle button').forEach(function(b){
    b.classList.toggle('on',b.getAttribute('data-lang')===l);
  });
  try{localStorage.setItem(LANG_KEY,l);}catch(e){}
  document.dispatchEvent(new CustomEvent('bpc-lang',{detail:l}));
}
document.querySelectorAll('.lang-toggle button').forEach(function(b){
  b.addEventListener('click',function(){applyLang(b.getAttribute('data-lang'));});
});
applyLang(currentLang());

/* ---------- FAQ accordions ---------- */
document.querySelectorAll('.faq-q').forEach(function(q){
  q.addEventListener('click',function(){q.closest('.faq').classList.toggle('open');});
});

/* ---------- footer year ---------- */
document.querySelectorAll('[data-year]').forEach(function(el){el.textContent=new Date().getFullYear();});

/* ---------- generic form validation + reference numbers ---------- */
function validEmail(v){return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);}
function makeRef(prefix){
  var d=new Date(),p=function(n){return String(n).padStart(2,'0');};
  var rnd=Math.floor(1000+Math.random()*9000);
  return (prefix||'BPC')+'-'+d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+'-'+rnd;
}
document.querySelectorAll('form.bpc-form').forEach(function(form){
  form.addEventListener('submit',function(ev){
    ev.preventDefault();
    var ok=true,firstBad=null;
    form.querySelectorAll('[data-required]').forEach(function(inp){
      var wrap=inp.closest('.field');if(wrap)wrap.classList.remove('invalid');
      var val=(inp.value||'').trim(),bad=false;
      if(inp.type==='checkbox'){bad=!inp.checked;}
      else if(!val){bad=true;}
      else if(inp.type==='email'&&!validEmail(val)){bad=true;}
      else if(inp.getAttribute('data-validate')==='phone'&&val.replace(/\D/g,'').length<7){bad=true;}
      if(bad){ok=false;if(wrap)wrap.classList.add('invalid');if(!firstBad)firstBad=inp;}
    });
    if(!ok){if(firstBad)firstBad.focus();return;}
    var ref=makeRef(form.getAttribute('data-ref-prefix')||'BPC');
    var panel=form.parentElement.querySelector('.form-confirm');
    var refEl=form.parentElement.querySelector('.ref-number');
    if(refEl)refEl.textContent=ref;
    form.style.display='none';
    if(panel)panel.classList.add('show');
    try{form.reset();}catch(e){}
  });
});

/* ---------- JSON-driven media (podcast / video tips) ---------- */
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function langNow(){return document.documentElement.getAttribute('lang')==='en'?'en':'es';}
function pick(o){var l=langNow();return o[l]||o.en||o.es||'';}
function loadMedia(cfg){
  var list=document.getElementById(cfg.listId),empty=document.getElementById(cfg.emptyId),
      filters=document.getElementById(cfg.filterId),featured=document.getElementById(cfg.featuredId||'');
  if(!list)return;
  fetch(cfg.json).then(function(r){if(!r.ok)throw 0;return r.json();}).then(function(data){
    var items=(data.items||[]).filter(function(i){return !i.sample;});
    var cats={};items.forEach(function(i){(i.categories||[]).forEach(function(c){cats[c]=1;});});
    var active='all',q='';
    function t(key){var l=langNow();return (cfg.strings[key]&&cfg.strings[key][l])||cfg.strings[key].en;}
    function render(){
      var shown=items.filter(function(i){
        var okC=active==='all'||(i.categories||[]).indexOf(active)>=0;
        var okQ=!q||(pick(i.title)+' '+pick(i.description)).toLowerCase().indexOf(q)>=0;
        return okC&&okQ;
      });
      if(featured){
        if(shown.length){var f=shown[0];
          featured.innerHTML='<div class="card"><span class="eyebrow">'+esc(t('latest'))+'</span><h3>'+esc(pick(f.title))+'</h3>'+
          '<p class="media-meta">'+esc(f.date||'')+(f.duration?' · '+esc(f.duration):'')+'</p><p>'+esc(pick(f.description))+'</p>'+
          (f.youtubeId?'<div style="margin:1rem 0"><a class="btn btn-teal btn-sm" target="_blank" rel="noopener" href="https://www.youtube.com/watch?v='+esc(f.youtubeId)+'">'+esc(t('watch'))+'</a></div>':'')+
          (f.audioUrl?'<div style="margin:1rem 0"><audio controls preload="none" src="'+esc(f.audioUrl)+'" style="width:100%"></audio></div>':'')+
          '</div>';
          featured.style.display='';
        }else{featured.style.display='none';}
      }
      var rest=featured?shown.slice(1):shown;
      if(!rest.length){list.innerHTML='';if(empty)empty.style.display='';return;}
      if(empty)empty.style.display='none';
      list.innerHTML=rest.map(function(i){
        var badge=i.sample?'<span class="badge-sample">SAMPLE</span>':'';
        var media='';
        if(i.youtubeId)media='<a class="btn btn-outline btn-sm" target="_blank" rel="noopener" href="https://www.youtube.com/watch?v='+esc(i.youtubeId)+'">'+esc(t('watch'))+'</a>';
        else if(i.audioUrl)media='<audio controls preload="none" src="'+esc(i.audioUrl)+'" style="width:100%;margin-top:.6rem"></audio>';
        return '<article class="card media-card"><div class="media-thumb" aria-hidden="true">'+esc(cfg.icon)+'</div>'+
        '<div><p class="media-meta">'+esc(i.date||'')+(i.duration?' · '+esc(i.duration):'')+badge+'</p>'+
        '<h3>'+esc(pick(i.title))+'</h3><p>'+esc(pick(i.description))+'</p><div style="margin-top:.8rem">'+media+'</div></div></article>';
      }).join('');
    }
    function renderFilters(){
      if(!filters)return;
      var keys=Object.keys(cats).sort();
      var html='<button class="filter-btn'+(active==='all'?' on':'')+'" data-cat="all">'+esc(t('all'))+'</button>'+
        keys.map(function(c){return '<button class="filter-btn'+(active===c?' on':'')+'" data-cat="'+esc(c)+'">'+esc(c)+'</button>';}).join('');
      filters.innerHTML=html;
      filters.querySelectorAll('.filter-btn').forEach(function(b){
        b.addEventListener('click',function(){active=b.getAttribute('data-cat');renderFilters();render();});
      });
    }
    renderFilters();render();
    document.addEventListener('bpc-lang',function(){renderFilters();render();});
    var search=document.getElementById(cfg.searchId||'');
    if(search)search.addEventListener('input',function(){q=search.value.toLowerCase();render();});
  }).catch(function(){if(empty)empty.style.display='';});
}

/* podcast archive */
loadMedia({listId:'podcastList',emptyId:'podcastEmpty',filterId:'podcastFilters',searchId:'podcastSearch',
  featuredId:'podcastFeatured',json:'content/podcast.json',icon:'🎙️',
  strings:{latest:{en:'Latest episode',es:'Último episodio'},watch:{en:'Watch on YouTube',es:'Ver en YouTube'},
    all:{en:'All topics',es:'Todos los temas'}}});
/* daily video tips */
loadMedia({listId:'tipsList',emptyId:'tipsEmpty',filterId:'tipsFilters',searchId:'tipsSearch',
  featuredId:'tipsFeatured',json:'content/video-tips.json',icon:'▶',
  strings:{latest:{en:"Today's tip",es:'Consejo de hoy'},watch:{en:'Watch on YouTube',es:'Ver en YouTube'},
    all:{en:'All topics',es:'Todos los temas'}}});

/* ---------- booking flow ---------- */
var bookingRoot=document.getElementById('bookingApp');
if(bookingRoot){
  var svcGrid=document.getElementById('svcGrid'),stepsEl=document.getElementById('bookSteps'),
      step2=document.getElementById('bookStep2'),step3=document.getElementById('bookStep3'),
      chosen=null,pricing=null;
  function setStep(n){
    stepsEl.querySelectorAll('.step').forEach(function(s,i){s.classList.toggle('on',i<n);});
  }
  function svcName(s){return esc(langNow()==='es'?s.name_es:s.name_en);}
  function svcDesc(s){return esc(langNow()==='es'?s.desc_es:s.desc_en);}
  fetch('content/pricing.json').then(function(r){return r.json();}).then(function(p){
    pricing=p;
    function renderGrid(){
      svcGrid.innerHTML=p.services.map(function(s){
        return '<div class="service-opt'+(chosen&&chosen.id===s.id?' selected':'')+'" data-svc="'+esc(s.id)+'" role="button" tabindex="0">'+
        '<h4>'+svcName(s)+'</h4><p style="font-size:.88rem;color:var(--muted)">'+svcDesc(s)+'</p></div>';
      }).join('');
      svcGrid.querySelectorAll('.service-opt').forEach(function(el){
        function pick(){chosen=p.services.filter(function(s){return s.id===el.getAttribute('data-svc');})[0];
          renderGrid();showStep2();}
        el.addEventListener('click',pick);
        el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();pick();}});
      });
    }
    function showStep2(){
      setStep(2);
      document.getElementById('chosenSvcName').textContent=svcName(chosen);
      step2.style.display='';step3.style.display='none';
      step2.scrollIntoView({behavior:'smooth',block:'start'});
    }
    renderGrid();setStep(1);
    document.addEventListener('bpc-lang',function(){renderGrid();if(chosen&&step2.style.display!=='none')showStep2();});
    var form=document.getElementById('bookingForm');
    form.addEventListener('submit',function(ev){
      ev.preventDefault();
      var ok=true,firstBad=null;
      form.querySelectorAll('[data-required]').forEach(function(inp){
        var wrap=inp.closest('.field');if(wrap)wrap.classList.remove('invalid');
        var val=(inp.value||'').trim(),bad=false;
        if(inp.type==='checkbox')bad=!inp.checked;
        else if(!val)bad=true;
        else if(inp.type==='email'&&!validEmail(val))bad=true;
        if(bad){ok=false;if(wrap)wrap.classList.add('invalid');if(!firstBad)firstBad=inp;}
      });
      if(!ok){if(firstBad)firstBad.focus();return;}
      var ref=makeRef('BPC-BOOK');
      setStep(3);
      document.getElementById('bookRef').textContent=ref;
      document.getElementById('bookSvcEcho').textContent=svcName(chosen);
      form.style.display='none';step2.style.display='none';step3.style.display='';
      step3.scrollIntoView({behavior:'smooth',block:'start'});
    });
  }).catch(function(){
    svcGrid.innerHTML='<div class="notice notice-demo">Service information is temporarily unavailable. Please contact us to request a consultation.</div>';
  });
}

/* ---------- portal demo login ---------- */
var demoLogin=document.getElementById('demoLoginForm');
if(demoLogin){
  demoLogin.addEventListener('submit',function(ev){
    ev.preventDefault();
    document.getElementById('demoLoginWrap').style.display='none';
    document.getElementById('demoDash').style.display='';
  });
}
})();
