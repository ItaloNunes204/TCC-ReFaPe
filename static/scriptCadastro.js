
let btn = document.querySelector('#olho')

let btnConfirm = document.querySelector('#verConfirmSenha')

let nome = document.querySelector('#nome')
let labelNome = document.querySelector('#labelNome')
let validNome = false

let email = document.querySelector('#email')
let labelEmail = document.querySelector('#labelEmail')
let validEmail= false

let nomeResponsavel = document.querySelector('#nomeResponsavel')
let labelNomeResponsavel = document.querySelector('#labelNomeResponsavel')
let validNomeResponsavel= false

let cnpj = document.querySelector('#cnpj')
let labelCnpj = document.querySelector('#labelCnpj')
let validCnpj = false

let cpf = document.querySelector('#cpf')
let labelCpf = document.querySelector('#labelCpf')
let validCpf = false

let senha = document.querySelector('#senha')
let labelSenha = document.querySelector('#labelSenha')
let validSenha = false

let confirmSenha = document.querySelector('#confirmSenha')
let labelConfirmSenha = document.querySelector('#labelConfirmSenha')
let validConfirmSenha = false

nome.addEventListener('keyup', () => {
  if(nome.value.length <= 2){
    labelNome.setAttribute('style', 'color: red')
    labelNome.innerHTML = 'Nome *Insira no minimo 3 caracteres'
    nome.setAttribute('style', 'border-color: red')
    validNome = false
  } else {
    labelNome.setAttribute('style', 'color: green')
    labelNome.innerHTML = 'Nome'
    nome.setAttribute('style', 'border-color: green')
    validNome = true
  }
})

email.addEventListener('keyup', () => {
  if(email.value.length <= 4){
    labelEmail.setAttribute('style', 'color: red')
    labelEmail.innerHTML = 'Email *Insira no minimo 5 caracteres'
    email.setAttribute('style', 'border-color: red')
    validEmail = false
  } else {
    labelEmail.setAttribute('style', 'color: green')
    labelEmail.innerHTML = 'Email'
    email.setAttribute('style', 'border-color: green')
    validEmail = true
  }
})

nomeResponsavel.addEventListener('keyup', () => {
  if(nomeResponsavel.value.length <= 4){
    labelNomeResponsavel.setAttribute('style', 'color: red')
    labelNomeResponsavel.innerHTML = 'Nome Responsavel *Insira no minimo 5 caracteres'
    nomeResponsavel.setAttribute('style', 'border-color: red')
    validNomeResponsavel = false
  } else {
    labelNomeResponsavel.setAttribute('style', 'color: green')
    labelNomeResponsavel.innerHTML = 'Nome Responsavel'
    nomeResponsavel.setAttribute('style', 'border-color: green')
    validNomeResponsavel = true
  }
})

cnpj.addEventListener('keyup', () => {
  if(cnpj.value.length <= 4){
    labelCnpj.setAttribute('style', 'color: red')
    labelCnpj.innerHTML = 'cnpj *Insira no minimo 5 caracteres'
    cnpj.setAttribute('style', 'border-color: red')
    validCnpj = false
  } else {
    labelCnpj.setAttribute('style', 'color: green')
    labelCnpj.innerHTML = 'cnpj'
    cnpj.setAttribute('style', 'border-color: green')
    validCnpj = true
  }
})

cpf.addEventListener('keyup', () => {
  if(cpf.value.length <= 4){
    labelCpf.setAttribute('style', 'color: red')
    labelCpf.innerHTML = 'cpf *Insira no minimo 5 caracteres'
    cpf.setAttribute('style', 'border-color: red')
    validCpf = false
  } else {
    labelCpf.setAttribute('style', 'color: green')
    labelCpf.innerHTML = 'cpf'
    cpf.setAttribute('style', 'border-color: green')
    validCpf = true
  }
})

/*
senha.addEventListener('keyup', () => {
  if(senha.value.length <= 5){
    labelSenha.setAttribute('style', 'color: red')
    labelSenha.innerHTML = 'Senha *Insira no minimo 6 caracteres'
    senha.setAttribute('style', 'border-color: red')
    validSenha = false
  } else {
    labelSenha.setAttribute('style', 'color: green')
    labelSenha.innerHTML = 'Senha'
    senha.setAttribute('style', 'border-color: green')
    validSenha = true
  }
})

confirmSenha.addEventListener('keyup', () => {
  if(senha.value != confirmSenha.value){
    labelConfirmSenha.setAttribute('style', 'color: red')
    labelConfirmSenha.innerHTML = 'Confirmar Senha *As senhas não conferem'
    confirmSenha.setAttribute('style', 'border-color: red')
    validConfirmSenha = false
  } else {
    labelConfirmSenha.setAttribute('style', 'color: green')
    labelConfirmSenha.innerHTML = 'Confirmar Senha'
    confirmSenha.setAttribute('style', 'border-color: green')
    validConfirmSenha = true
  }
})
*/

btn.addEventListener('click', () => {
  let inputSenha = document.querySelector('#senha')

  if(inputSenha.getAttribute('type') == 'password'){
    inputSenha.setAttribute('type', 'text')
  } else {
    inputSenha.setAttribute('type', 'password')
  }
})




