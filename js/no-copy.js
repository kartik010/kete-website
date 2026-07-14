(function () {
  'use strict';

  function isEditable(el) {
    if (!el || el === document || el === document.documentElement || el === document.body) return false;
    var node = el.nodeType === 3 ? el.parentElement : el;
    if (!node || !node.closest) return false;
    if (node.closest('input, textarea, select, [contenteditable="true"]')) return true;
    return !!node.isContentEditable;
  }

  function block(e) {
    if (isEditable(e.target)) return;
    e.preventDefault();
    return false;
  }

  document.addEventListener('contextmenu', block, true);
  document.addEventListener('copy', block, true);
  document.addEventListener('cut', block, true);
  document.addEventListener('dragstart', block, true);
  document.addEventListener('selectstart', block, true);

  document.addEventListener('keydown', function (e) {
    if (isEditable(e.target)) return;

    var key = (e.key || '').toLowerCase();
    var ctrl = e.ctrlKey || e.metaKey;

    if (ctrl && (key === 'c' || key === 'x' || key === 'a' || key === 'u' || key === 's' || key === 'p')) {
      e.preventDefault();
      return;
    }
    if (ctrl && e.shiftKey && (key === 'i' || key === 'j' || key === 'c')) {
      e.preventDefault();
      return;
    }
    if (key === 'f12') {
      e.preventDefault();
    }
  }, true);
})();
