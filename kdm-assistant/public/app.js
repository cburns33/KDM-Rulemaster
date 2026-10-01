const $ = id => document.getElementById(id);
let library, chatId = null, chatContext = {}, selectedRecord = null, busy = false;
let browserChats = [];
const hosted = () => library?.hosting === 'vercel';
const browserChatKey = 'lantern-archive-chats';
const welcome = $('welcome').cloneNode(true);
let openPanel = null;
function closeDrawer() {
  if (!openPanel) return;
  const trigger = openPanel === $('history-panel') ? $('open-history') : $('open-sources');
  openPanel.hidden = true;
  $('drawer-scrim').hidden = true;
  document.querySelector('main').inert = false;
  trigger.setAttribute('aria-expanded', 'false');
  openPanel = null;
  trigger.focus();
}
function openDrawer(panel, trigger) {
  closeDrawer();
  $('settings-popover').hidden = true;
  $('open-settings').setAttribute('aria-expanded', 'false');
  panel.hidden = false;
  $('drawer-scrim').hidden = false;
  document.querySelector('main').inert = true;
  trigger.setAttribute('aria-expanded', 'true');
  openPanel = panel;
  panel.querySelector('.drawer-heading button').focus();
}
$('open-history').onclick = () => openDrawer($('history-panel'), $('open-history'));
$('open-sources').onclick = () => openDrawer($('source-panel'), $('open-sources'));
$('close-history').onclick = closeDrawer;
$('close-sources').onclick = closeDrawer;
$('drawer-scrim').onclick = closeDrawer;
document.onkeydown = e => {if (e.key === 'Escape') {closeDrawer(); $('settings-popover').hidden = true; $('open-settings').setAttribute('aria-expanded', 'false');}};
$('open-settings').onclick = () => {const panel = $('settings-popover'); panel.hidden = !panel.hidden; $('open-settings').setAttribute('aria-expanded', String(!panel.hidden));};
async function api(path, body) {
  const response = await fetch(path, body === undefined ? {} : {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'The app could not complete the request.');
  return data;
}
function error(message) { $('error').textContent = message; $('error').hidden = false; setTimeout(() => $('error').hidden = true, 8000); }
function sourceText(p) {return `Revised PDF ${p.revised} · Book ${p.printed ?? 'unnumbered'} · Original PDF ${p.original} · Edition ${p.edition}`;}
function shortSourceText(p) {return `PDF ${p.revised} · Book ${p.printed ?? 'unnumbered'}`;}
function showPage(number) {
  const p = library.pages.find(p => p.revised === Number(number));
  if (!p) return error('Choose a revised PDF page from 1 to 138.');
  $('page').value = p.revised;
  $('page-label').textContent = shortSourceText(p) + (p.reviewed ? ' · Reviewed' : ' · Page image');
  $('page-label').title = sourceText(p);
  $('page-image').src = `/pages/${p.revised}.jpg`;
  $('page-image').alt = p.title + ', ' + sourceText(p);
  $('image-link').href = `/pages/${p.revised}.jpg`;
  selectedRecord = library.records.find(r => r.id === p.record_id) || null;
  $('layout').hidden = !selectedRecord;
  $('layout-note').textContent = selectedRecord?.layout || '';
  $('correction-area').hidden = hosted() || !selectedRecord;
  $('correction-form').hidden = true;
  $('correction-status').textContent = '';
  $('table-details').hidden = !selectedRecord?.tables.length;
  $('table-records').replaceChildren();
  for (const table of selectedRecord?.tables || []) {
    const title = document.createElement('h3'); title.textContent = table.title; $('table-records').append(title);
    for (const row of table.rows) {
      const line = document.createElement('p'); const band = document.createElement('strong'); band.textContent = row.label + ': ';
      line.append(band, document.createTextNode(row.effects.join(' '))); $('table-records').append(line);
    }
  }
  for (const b of $('records').querySelectorAll('button')) b.classList.toggle('selected', b.dataset.id === selectedRecord?.id);
}
function recordList(records) {
  $('records').replaceChildren();
  if (!records.length) { $('records').textContent = 'No reviewed topic found.'; return; }
  for (const r of records) {
    const button = document.createElement('button'); button.dataset.id = r.id;
    button.append(document.createTextNode(r.title));
    const small = document.createElement('small'); small.textContent = shortSourceText(r.source);
    button.append(small); button.onclick = () => showPage(r.source.revised);
    $('records').append(button);
  }
}
function addMessage(role, text, payload) {
  $('welcome')?.remove();
  const block = document.createElement('article'); block.className = `message ${role}`;
  let tag;
  if (role === 'assistant') {
    tag = document.createElement('div'); tag.className = 'message-tag';
    tag.textContent = payload?.status === 'resolved' ? 'TABLE RESULT' : payload?.status === 'model-reference' ? 'SOL ANSWER' : payload?.status === 'unsupported' ? 'OUTSIDE REVIEWED COVERAGE' : payload?.status === 'source-needed' ? 'CARD TEXT NEEDED' : payload?.status === 'edition-check' ? 'EDITION CHECK' : payload?.status === 'clarify' ? 'NEEDS CLARIFICATION' : 'REVIEWED REFERENCE';
  }
  const answer = document.createElement('div'); answer.className = 'answer';
  for (const part of text.split(/(\*\*[^*]+\*\*)/g)) {
    if (part.startsWith('**') && part.endsWith('**')) {const strong=document.createElement('strong'); strong.textContent=part.slice(2,-2); answer.append(strong);}
    else answer.append(document.createTextNode(part));
  }
  block.append(answer);
  if (tag) block.append(tag);
  const cited = new Set();
  let sourceRow;
  for (const r of [payload?.record, ...(payload?.related_records || [])].filter(Boolean)) {
    for (const p of r.sources || [r.source]) {
      if (cited.has(p.original)) continue;
      cited.add(p.original);
      if (!sourceRow) {sourceRow = document.createElement('div'); sourceRow.className = 'source-row'; block.append(sourceRow);}
      const citation = document.createElement('button'); citation.className = 'citation';
      citation.textContent = `${r.title} · ${shortSourceText(p)} ↗`;
      citation.title = sourceText(p);
      citation.onclick = () => {showPage(p.revised); openDrawer($('source-panel'), $('open-sources'));}; sourceRow.append(citation);
    }
    for (const card of r.card_sources || []) {
      if (!sourceRow) {sourceRow = document.createElement('div'); sourceRow.className = 'source-row'; block.append(sourceRow);}
      const citation = document.createElement('a'); citation.className = 'citation';
      citation.textContent = `${card.title} · ${card.edition} card ↗`;
      citation.href = card.url; citation.target = '_blank'; citation.rel = 'noopener noreferrer'; sourceRow.append(citation);
    }
  }
  $('messages').append(block); $('messages').scrollTop = $('messages').scrollHeight;
}
async function loadChats() {
  if (hosted()) {
    $('chats').replaceChildren();
    for (const chat of browserChats) {
      const b = document.createElement('button'); b.textContent = chat.title; b.classList.toggle('active', chat.id === chatId);
      b.onclick = () => {if(busy)return; chatId=chat.id; chatContext=chat.context || {}; $('messages').replaceChildren(); for(const message of chat.messages || [])addMessage(message.role,message.content,message.payload); const last=[...(chat.messages || [])].reverse().find(message=>message.payload?.record); if(last)showPage(last.payload.record.source.revised); loadChats(); closeDrawer();};
      $('chats').append(b);
    }
    return;
  }
  const chats = await api('/api/chats'); $('chats').replaceChildren();
  for (const chat of chats) {
    const b = document.createElement('button'); b.textContent = chat.title; b.classList.toggle('active', chat.id === chatId);
    b.onclick = async () => {if(busy)return; try {chatId=chat.id; $('messages').replaceChildren(); const messages=await api('/api/chats/'+chat.id); for(const m of messages)addMessage(m.role,m.content,m.payload); const last=[...messages].reverse().find(m=>m.payload?.record); if(last)showPage(last.payload.record.source.revised); await loadChats(); closeDrawer();}catch(e){error(e.message);}};
    $('chats').append(b);
  }
}
function saveHostedChat(question, result) {
  if (!hosted()) return;
  let chat = browserChats.find(item => item.id === chatId);
  if (!chat) {chat = {id: chatId, title: question.slice(0, 64), messages: [], context: {}}; browserChats.unshift(chat);}
  chat.context = result.context || {};
  chat.messages.push({role: 'user', content: question}, {role: 'assistant', content: result.answer, payload: result});
  localStorage.setItem(browserChatKey, JSON.stringify(browserChats.slice(0, 30)));
}
async function ask(question, extra = {}) {
  if (busy) return;
  busy = true; $('send').disabled = true;
  addMessage('user', question);
  try {
    const body = {question, chat_id:chatId, use_model:$('use-model').checked, ...extra};
    if (hosted()) body.context = chatContext;
    const result = await api('/api/ask', body);
    if (hosted()) {if(!chatId)chatId='browser-'+Date.now(); chatContext=result.context || {}; saveHostedChat(question, result);} else chatId = result.chat_id;
    addMessage('assistant', result.answer, result);
    if (result.model?.message) error(result.model.message);
    if (result.record) showPage(result.record.source.revised);
    if (result.table) $('table').value = result.table.id;
    if (result.context?.oven) $('oven').value = result.context.oven;
    $('question').value = ''; await loadChats();
  } catch(e) {error(e.message); addMessage('assistant', 'The request failed. Please try again. No ruling was generated.', {status:'unsupported'});}
  finally {busy=false; $('send').disabled=false; $('question').focus();}
}
$('ask-form').onsubmit = e => {e.preventDefault(); const q=$('question').value.trim(); if(q)ask(q);};
$('question').onkeydown = e => {if(e.key==='Enter'&&!e.shiftKey){e.preventDefault(); $('ask-form').requestSubmit();}};
$('messages').onclick=e=>{const b=e.target.closest('[data-prompt]'); if(b)ask(b.dataset.prompt);};
function newChat(){if(busy)return; chatId=null; chatContext={}; $('table').value='experiment'; $('oven').value='unknown'; $('messages').replaceChildren(welcome.cloneNode(true)); closeDrawer(); loadChats().catch(e=>error(e.message)); $('question').focus();}
$('new-chat').onclick=newChat;
$('header-new-chat').onclick=newChat;
$('go').onclick=()=>showPage($('page').value);
$('page').onkeydown=e=>{if(e.key==='Enter')showPage($('page').value);};
$('previous').onclick=()=>showPage(Math.max(1,Number($('page').value)-1));
$('next').onclick=()=>showPage(Math.min(138,Number($('page').value)+1));
let searchGeneration=0;
$('search').oninput=async()=>{const generation=++searchGeneration;try{const q=$('search').value.trim(),records=q?await api('/api/search?q='+encodeURIComponent(q)):library.records;if(generation===searchGeneration)recordList(records);}catch(e){error(e.message);}};
$('oven').onchange=()=>{if($('oven').value==='yes')$('table').value='branding';if($('oven').value==='no')$('table').value='experiment';};
$('roll-form').onsubmit=e=>{e.preventDefault();const table=$('table').value,roll=Number($('roll').value);ask(`Hands of Heat: ${table==='experiment'?'Experiment with Lanterns':'Lantern Branding'}, roll ${roll}`,{record_id:'hands-of-heat',table_id:table,roll,oven:$('oven').value});};
$('report').onclick=()=>{$('correction-form').hidden=!$('correction-form').hidden;};
$('correction-form').onsubmit=async e=>{e.preventDefault();try{const r=await api('/api/corrections',{record_id:selectedRecord.id,note:$('correction').value});$('correction-status').textContent=r.message;$('correction').value='';$('correction-form').hidden=true;}catch(e){error(e.message);}};
async function init(){try{library=await api('/api/library');if(hosted()){try{browserChats=JSON.parse(localStorage.getItem(browserChatKey) || '[]');if(!Array.isArray(browserChats))browserChats=[];}catch{browserChats=[];}}$('coverage').textContent=`${library.records.length} reviewed topics from ${library.pages.filter(p=>p.reviewed).length} pages. All 138 retained pages are browsable in Sources.`;const model=library.model;$('use-model').disabled=!model.configured;$('provider-status').textContent=model.configured?'GPT-6 Sol available · Local lookup is the default':'Local lookup';$('provider-note').textContent=model.configured?'When enabled, Sol receives this question and selected reviewed records.':'No model connected. Your questions stay local.';recordList(library.records);showPage(library.records.find(r=>r.id==='hands-of-heat').source.revised);await loadChats();}catch(e){error('Could not load the source library. '+e.message);}}
init();
