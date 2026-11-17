const money = value => Number(value).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
let products = [], cart = [], category = 'Todos';
const $ = id => document.getElementById(id);
async function loadProducts(){
  try { const response = await fetch('/api/products'); if(!response.ok) throw new Error(); products = await response.json(); renderProducts(); }
  catch { $('products').innerHTML = '<p>Não foi possível carregar o cardápio. Verifique se o servidor está ativo.</p>'; }
}
function renderProducts(){
  const visible = category === 'Todos' ? products : products.filter(p=>p.category===category);
  $('products').innerHTML = visible.map(p=>`<article class="product"><div class="product-art">${p.image || '🧁'}</div><div class="product-info"><h3>${escapeHtml(p.name)}</h3><p>${escapeHtml(p.description)}</p><div class="product-bottom"><span class="price">${money(p.price)}</span><button class="add" data-add="${p.id}">+ Adicionar</button></div></div></article>`).join('') || '<p>Nenhum produto nesta categoria.</p>';
}
function escapeHtml(value){return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function add(id){const item=cart.find(i=>i.id===id);if(item)item.quantity++;else cart.push({id,quantity:1});renderCart();}
function change(id,delta){const item=cart.find(i=>i.id===id);if(!item)return;item.quantity+=delta;if(item.quantity<=0)cart=cart.filter(i=>i.id!==id);renderCart();}
function renderCart(){
  const count=cart.reduce((s,i)=>s+i.quantity,0);$('cart-count').textContent=count;
  $('cart-items').innerHTML=cart.length?cart.map(i=>{const p=products.find(x=>x.id===i.id);return `<div class="cart-row"><div><strong>${escapeHtml(p.name)}</strong><small>${money(p.price)} cada · ${money(p.price*i.quantity)}</small></div><div class="qty"><button data-change="${p.id}" data-delta="-1">−</button><span>${i.quantity}</span><button data-change="${p.id}" data-delta="1">+</button></div></div>`}).join(''):'<p class="empty">Sua sacola está vazia. 🧁</p>';
  $('cart-total').textContent=money(cart.reduce((s,i)=>s+products.find(p=>p.id===i.id).price*i.quantity,0));
}
function toggleCart(open){$('cart').classList.toggle('open',open);$('overlay').classList.toggle('show',open);}
$('products').addEventListener('click',e=>{const b=e.target.closest('[data-add]');if(b)add(Number(b.dataset.add));});
$('cart-items').addEventListener('click',e=>{const b=e.target.closest('[data-change]');if(b)change(Number(b.dataset.change),Number(b.dataset.delta));});
$('filters').addEventListener('click',e=>{const b=e.target.closest('[data-category]');if(!b)return;category=b.dataset.category;document.querySelectorAll('.filter').forEach(x=>x.classList.toggle('active',x===b));renderProducts();});
$('open-cart').onclick=()=>toggleCart(true);$('close-cart').onclick=()=>toggleCart(false);$('overlay').onclick=()=>toggleCart(false);
$('checkout').onclick=()=>{if(!cart.length){alert('Adicione produtos antes de finalizar.');return;}toggleCart(false);$('checkout-dialog').showModal();};
$('close-dialog').onclick=()=>$('checkout-dialog').close();
$('checkout-form').addEventListener('submit',async e=>{
  e.preventDefault();const form=new FormData(e.target);const payload=Object.fromEntries(form.entries());payload.items=cart.map(i=>({product_id:i.id,quantity:i.quantity}));
  const button=e.target.querySelector('button[type=submit]');button.disabled=true;button.textContent='Enviando...';
  try{const response=await fetch('/api/orders',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const result=await response.json();if(!response.ok)throw new Error(result.error||'Não foi possível registrar o pedido.');
    $('form-message').textContent=`Pedido #${result.order_id} registrado! Total: ${money(result.total)}. Pagamento escolhido: ${escapeHtml(result.payment_method)}. Status: ${escapeHtml(result.status)}.`;cart=[];renderCart();e.target.reset();setTimeout(()=>$('checkout-dialog').close(),2500);
  }catch(err){$('form-message').textContent=err.message;}finally{button.disabled=false;button.textContent='Confirmar pedido';}
});
loadProducts();renderCart();
