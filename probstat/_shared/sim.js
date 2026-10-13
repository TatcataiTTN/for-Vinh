/* Khởi tạo mọi <div class="sim" data-sim="tên"> bằng widget đã đăng ký trong window.SIM_W (nạp simlib.js và w_*.js trước file này). */
(function(){'use strict';
var W=window.SIM_W||{};
document.querySelectorAll('.sim[data-sim]').forEach(function(root){var n=root.getAttribute('data-sim');if(W[n]){try{W[n](root)}catch(e){root.innerHTML='<p class="no">Lỗi widget '+n+': '+String(e.message).replace(/</g,'&lt;')+'</p>'}}else{root.innerHTML='<p class="no">Chưa có widget '+n+'</p>'}});
})();
