let cnpj = document.querySelector('#cnpj')
let labelCnpj = document.querySelector('#labelCnpj')

let senha = document.querySelector('#senha')
let labelSenha = document.querySelector('#labelSenha')
let validSenha = false

let btn = document.querySelector('.fa-eye')

cnpj.addEventListener('keyup', () => {
  if(cnpj.value.length <= 4){
    labelCnpj.setAttribute('style', 'color: red')
    labelCnpj.innerHTML = 'cnpj *Insira no minimo 5 caracteres'
    cnpj.setAttribute('style', 'border-color: red')
    validUsuario = false
  } else {
    labelCnpj.setAttribute('style', 'color: green')
    labelCnpj.innerHTML = 'cnpj'
    cnpj.setAttribute('style', 'border-color: green')
    validCnpj = true
  }
})

senha.addEventListener('keyup', () => {
  if(senha.value.length <= 2){
    labelSenha.setAttribute('style', 'color: red')
    labelSenha.innerHTML = 'Senha *Insira no minimo 3 caracteres'
    senha.setAttribute('style', 'border-color: red')
    validSenha = false
  } else {
    labelSenha.setAttribute('style', 'color: green')
    labelSenha.innerHTML = 'Senha'
    senha.setAttribute('style', 'border-color: green')
    validSenha = true
  }
})

btn.addEventListener('click', ()=>{
  let inputSenha = document.querySelector('#senha')

  if(inputSenha.getAttribute('type') == 'password'){
    inputSenha.setAttribute('type', 'text')
  } else {
    inputSenha.setAttribute('type', 'password')
  }
})