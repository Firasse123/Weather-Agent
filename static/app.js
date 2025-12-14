document.addEventListener('DOMContentLoaded', ()=>{
  const messagesEl = document.getElementById('messages');
  const inputEl = document.getElementById('input');
  const sendBtn = document.getElementById('send');

  function appendMessage(text, who='bot'){
    const div = document.createElement('div');
    div.className = 'msg ' + (who === 'user' ? 'user' : 'bot');
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  async function sendMessage(text){
    appendMessage(text, 'user');
    inputEl.value = '';
    appendMessage('…thinking…', 'bot');
    try{
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({message: text})
      });
      const data = await res.json();
      // remove the thinking bubble
      const last = messagesEl.querySelector('.msg.bot:last-child');
      if(last && last.textContent === '…thinking…') last.remove();

      if(!res.ok){
        appendMessage(data.error || 'Error from server', 'bot');
        return;
      }
      appendMessage(data.message || '[no response]', 'bot');
    }catch(err){
      const last = messagesEl.querySelector('.msg.bot:last-child');
      if(last && last.textContent === '…thinking…') last.remove();
      appendMessage('Network error: ' + err.message, 'bot');
    }
  }

  sendBtn.addEventListener('click', ()=>{
    const text = inputEl.value.trim();
    if(text) sendMessage(text);
  });

  inputEl.addEventListener('keydown', (e)=>{ if(e.key === 'Enter'){ sendBtn.click(); } });

  // add a welcome message
  appendMessage('Hello! Ask me about the weather for any city.', 'bot');
});
