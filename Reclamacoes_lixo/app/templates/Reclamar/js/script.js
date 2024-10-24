// Exibir o popup e o fundo preto ao clicar no ícone
document.getElementById('notification-icon').addEventListener('click', function(event) {
  event.preventDefault(); // Prevenir o comportamento padrão do link

  // Exibir o overlay com o popup
  document.getElementById('notification-overlay').style.display = 'flex';
});

// Fechar o popup ao clicar no botão "Fechar"
document.getElementById('close-popup').addEventListener('click', function() {
  document.getElementById('notification-overlay').style.display = 'none';
});

// Função para limpar o conteúdo do div contenteditable
const clearButton = document.getElementById("clearButton");
const complaintContent = document.getElementById("complaintContent");

clearButton.addEventListener("click", function () {
  complaintContent.innerHTML = ""; 
});

// Função para selecionar a imagem ao clicar no ícone de anexar
const attachButton = document.getElementById("attachButton");
const fileInput = document.getElementById("fileInput");

// Abrir a pasta de imagens ao clicar no ícone de anexar
attachButton.addEventListener("click", function () {
  fileInput.click();
});

// Adicionar a imagem no div contenteditable quando o usuário selecionar uma imagem
fileInput.addEventListener("change", function () {
  const file = fileInput.files[0]; 
  const reader = new FileReader(); 

  reader.onload = function (e) {
    const image = document.createElement("img"); 
    image.src = e.target.result; 
    image.style.maxWidth = "100%"; 
    image.style.height = "auto"; 

    complaintContent.appendChild(image); 
  };

  if (file) {
    reader.readAsDataURL(file); 
  }
});




document.getElementById("publishButton").addEventListener("click", function() {
  // Captura os dados do formulário
  const sector = document.getElementById("sector").value;
  const city = document.getElementById("city").value;
  const neighborhood = document.getElementById("neighborhood").value;
  const complaintContent = document.getElementById("complaintContent").value; 
  if (sector && city && neighborhood && complaintContent) {
      // Cria um objeto para armazenar os dados
      const complaint = {
          sector: sector,
          city: city,
          neighborhood: neighborhood,
          content: complaintContent,
          user: "Nann Cardoso",  // Exemplo, você pode personalizar
          role: "Professor"  // Exemplo, você pode personalizar
      };

      // Recupera as reclamações existentes no localStorage
      let complaints = JSON.parse(localStorage.getItem("complaints")) || [];

      // Adiciona a nova reclamação à lista
      complaints.push(complaint);

      // Armazena a lista de reclamações no localStorage
      localStorage.setItem("complaints", JSON.stringify(complaints));

      // Redireciona para a página Home
      window.location.href = "../Home_page/index.html";
  } else {
      alert("Por favor, preencha todos os campos.");
  }
});

