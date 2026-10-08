const form = document.querySelector('[data-campaign-form]');
if (form) {
  const preview = document.querySelector('[data-preview]');
  const update = () => {
    const select = form.elements.creative_path;
    const option = select.selectedOptions[0];
    preview.className = 'creative-card ' + (option.dataset.theme || 'forest');
    const image = preview.querySelector('[data-preview-image]');
    image.hidden = !select.value;
    if (select.value) image.src = select.value;
    preview.querySelector('[data-preview-title]').textContent = form.elements.title.value || option.textContent;
    preview.querySelector('[data-preview-body]').textContent = form.elements.body.value || '당신의 소식을 마을에 전하세요.';
  };
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  update();
}
