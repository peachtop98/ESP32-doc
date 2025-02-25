(function() {
  if (typeof jQuery == 'undefined') {
      var script = document.createElement('script');
      script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
      document.head.appendChild(script);
  }
})();

$(document).ready(function() {
  // 选择所有带有子节点的目录项
  $('.toctree-l1 > ul').show();
  $('.toctree-l2 > ul').show();
  // 可以根据需要继续添加更多层级，如 .toctree-l3 等
});