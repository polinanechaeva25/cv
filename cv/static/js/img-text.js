let inputs = document.querySelectorAll('.input__file');
Array.prototype.forEach.call(inputs, function (input) {
  let label = input.parentElement.parentElement.nextElementSibling,
    labelVal = label.querySelector('.input__file-button-text').innerText;

  input.addEventListener('change', function (e) {
    let countFiles = '';
    if (this.files && this.files.length >= 1)
      countFiles = this.files.length;

    if (countFiles > 1)
      label.querySelector('.input__file-button-text').innerText = 'Выберете только 1 файл! ';
    else if (countFiles == 1)
      label.querySelector('.input__file-button-text').innerText = 'Файл выбран: ' + e.target.value.split( '\\' ).pop();
    else
      label.querySelector('.input__file-button-text').innerText = labelVal;
  });
});
