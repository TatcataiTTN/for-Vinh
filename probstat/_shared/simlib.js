/* Tiện ích chung cho các widget mô phỏng. */
(function(){'use strict';
var PS=window.PS;
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function frame(root,title,body){root.innerHTML='<div class="simh">🧪 '+title+'</div>'+body}
function $(root,sel){return root.querySelector(sel)}
function nums(s){return s.split(/[\s,;]+/).filter(Boolean).map(function(t){return Number(t.replace(',','.').replace('−','-'))})}
function F(x,d){return PS.fmt(x,d===undefined?4:d)}
function tbl(head,rows){return '<table class="t"><tr>'+head.map(function(h){return '<th>'+h+'</th>'}).join('')+'</tr>'+rows.map(function(r){return '<tr>'+r.map(function(x){return '<td>'+x+'</td>'}).join('')+'</tr>'}).join('')+'</table>'}
var SVGNS='http://www.w3.org/2000/svg';
function css(n,d){var v=getComputedStyle(document.documentElement).getPropertyValue(n).trim();return v||d}

window.SL={PS:PS,esc:esc,frame:frame,$:$,nums:nums,F:F,tbl:tbl,css:css};window.SIM_W=window.SIM_W||{};
})();
