const btnEnviar = document.querySelector("#btn-enviar")
const btnEnviarLoader = document.querySelector("#btn-enviar-loader")

btnEnviar.addEventListener("click",()=>{
    btnEnviarLoader.style.display="block";
    btnEnviar.style.display="none"
})
setTimeout(() => {
    document.querySelector("#alerta").style.display='none';
},5000)